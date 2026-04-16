/**
 * Shared Slack Watcher — listens for messages via Socket Mode, routes to the right agent.
 *
 * Architecture:
 *   One process watches all configured channels. When a message arrives,
 *   it looks up which agent owns that channel and spawns a short-lived
 *   Claude Code session in that agent's working directory.
 *
 * Add a new agent: add a channel entry to config.json. No code changes.
 *
 * Usage: node watcher.mjs
 * Stop: Ctrl+C
 */

import { SocketModeClient } from "@slack/socket-mode";
import { WebClient } from "@slack/web-api";
import { spawn } from "child_process";
import { readFileSync, writeFileSync, mkdirSync, existsSync, appendFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load .env file
const envPath = join(__dirname, ".env");
if (existsSync(envPath)) {
  for (const line of readFileSync(envPath, "utf-8").split("\n")) {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith("#")) {
      const eqIdx = trimmed.indexOf("=");
      if (eqIdx > 0) {
        process.env[trimmed.slice(0, eqIdx)] = trimmed.slice(eqIdx + 1);
      }
    }
  }
}

const config = JSON.parse(readFileSync(join(__dirname, "config.json"), "utf-8"));

const SLACK_APP_TOKEN = process.env.SLACK_APP_TOKEN;
const SLACK_BOT_TOKEN = process.env.SLACK_BOT_TOKEN;
const OWNER_SLACK_ID = process.env.OWNER_SLACK_ID;

if (!SLACK_APP_TOKEN || !SLACK_BOT_TOKEN) {
  console.error("Missing SLACK_APP_TOKEN or SLACK_BOT_TOKEN in .env");
  process.exit(1);
}

const socketClient = new SocketModeClient({ appToken: SLACK_APP_TOKEN });
const webClient = new WebClient(SLACK_BOT_TOKEN);

const SESSIONS_DIR = join(__dirname, "sessions");
const LOG_FILE = join(__dirname, "watcher.log");
const MAX_HISTORY = config.maxHistory || 20;
const SESSION_TTL = (config.sessionTtlMinutes || 30) * 60 * 1000;
const TIMEOUT_MS = config.timeoutMs || 120000;

// Map channel IDs to agent configs
const channelMap = new Map(Object.entries(config.agents));

// Track processing state per channel (allows parallel across agents)
const processing = new Map();

// Resolve bot's own user ID on startup (to ignore own messages)
let botUserId = null;

function log(msg) {
  const ts = new Date().toISOString().replace("T", " ").slice(0, 19);
  const line = `[${ts}] ${msg}`;
  console.log(line);
  try {
    appendFileSync(LOG_FILE, line + "\n");
  } catch { /* ignore */ }
}

// --- Session persistence (per channel, same pattern as Discord watcher) ---

function loadSession(channelId) {
  mkdirSync(SESSIONS_DIR, { recursive: true });
  const path = join(SESSIONS_DIR, `${channelId}.json`);
  if (existsSync(path)) {
    try {
      const session = JSON.parse(readFileSync(path, "utf-8"));
      if (Date.now() - session.lastActivity > SESSION_TTL) {
        return { channelId, messages: [], lastActivity: Date.now() };
      }
      return session;
    } catch {
      return { channelId, messages: [], lastActivity: Date.now() };
    }
  }
  return { channelId, messages: [], lastActivity: Date.now() };
}

function saveSession(session) {
  mkdirSync(SESSIONS_DIR, { recursive: true });
  if (session.messages.length > MAX_HISTORY) {
    session.messages = session.messages.slice(-MAX_HISTORY);
  }
  session.lastActivity = Date.now();
  writeFileSync(join(SESSIONS_DIR, `${session.channelId}.json`), JSON.stringify(session, null, 2));
}

function formatHistory(session, agentLabel) {
  if (session.messages.length === 0) return "";
  const lines = session.messages.map((m) => {
    const who = m.role === "user" ? "Dina" : m.role === "agent" ? agentLabel : m.role;
    return `${who}: ${m.content}`;
  });
  return `\n\nCONVERSATION HISTORY (most recent messages):\n${lines.join("\n")}\n\n`;
}

// --- Resolve user display name ---

const userNameCache = new Map();

async function getUserName(userId) {
  if (userNameCache.has(userId)) return userNameCache.get(userId);
  try {
    const result = await webClient.users.info({ user: userId });
    const name = result.user.real_name || result.user.name || userId;
    userNameCache.set(userId, name);
    return name;
  } catch {
    return userId;
  }
}

// --- Identify message source ---

function getMessageSource(event) {
  // Check if message is from another agent's bot
  for (const [chId, agentCfg] of channelMap) {
    if (event.bot_profile?.name?.toLowerCase() === agentCfg.name) {
      return { type: "agent", name: agentCfg.label };
    }
  }
  if (event.user === OWNER_SLACK_ID) {
    return { type: "owner", name: "Dina" };
  }
  return { type: "other", name: event.user };
}

// --- Build prompt for Claude session ---

function buildPrompt(agentCfg, message, senderName, history) {
  const now = new Date();
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const dayName = days[now.getDay()];
  const dateStr = now.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
  const timeStr = now.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", hour12: true, timeZone: "America/Los_Angeles" });

  return `You are ${agentCfg.label}. ${senderName} just sent a message in your Slack channel (#${agentCfg.name}).

CURRENT DATE/TIME: ${dayName}, ${dateStr} at ${timeStr} PT.
${history}${senderName}'s message: ${message}

Rules:
- Read the wiki at C:\\Workspace\\agents\\wiki\\index.md if the question involves people, projects, or past work
- Your entire stdout will be sent as the Slack reply — output ONLY the reply text
- No tool result summaries, no "I used X tool", no markdown headers — just the response
- Keep it under 500 chars unless the question requires detail
- Be direct, no AI slop
- If told something new, acknowledge and update wiki/memory if relevant
- If asked to do something, do it with tools and confirm
- If history shows prior discussion, build on it — don't start over`;
}

// --- Spawn Claude session ---

function spawnClaude(agentCfg, prompt) {
  return new Promise((resolve) => {
    const proc = spawn("claude", ["-p", prompt, "--dangerously-skip-permissions"], {
      cwd: agentCfg.cwd,
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";

    proc.stdout.on("data", (data) => { stdout += data.toString(); });
    proc.stderr.on("data", (data) => { stderr += data.toString(); });

    proc.on("close", (code) => {
      if (code === 0 && stdout.trim()) {
        const cleaned = stdout.trim().split("\n")
          .filter(l => l.trim())
          .filter(l => !l.startsWith("\u256D") && !l.startsWith("\u2502") && !l.startsWith("\u2570"))
          .filter(l => !l.startsWith(">"))
          .filter(l => !l.includes("tool_use") && !l.includes("content_block"))
          .join("\n")
          .trim();
        resolve(cleaned);
      } else {
        log(`Claude session failed (exit ${code}): ${stderr.slice(0, 200)}`);
        resolve(null);
      }
    });

    setTimeout(() => {
      if (!proc.killed) {
        proc.kill();
        log(`Session timed out for ${agentCfg.label}`);
        resolve(null);
      }
    }, TIMEOUT_MS);
  });
}

// --- Message handler ---

async function handleMessage(event) {
  const channelId = event.channel;
  const agentCfg = channelMap.get(channelId);

  if (!agentCfg) return; // not a watched channel

  // Ignore bot's own messages
  if (event.bot_id || event.user === botUserId) return;

  // Ignore message subtypes (edits, joins, etc.) except bot_message from other agents
  if (event.subtype && event.subtype !== "bot_message") return;

  // If this is a bot_message, check if it's from a known agent
  if (event.subtype === "bot_message") {
    const source = getMessageSource(event);
    if (source.type !== "agent") return; // unknown bot, ignore
  }

  // Skip if already processing for this channel
  if (processing.get(channelId)) {
    log(`Skipping message in ${agentCfg.name} (already processing)`);
    return;
  }

  processing.set(channelId, true);

  const source = getMessageSource(event);
  const senderName = source.type === "owner" ? "Dina" :
                     source.type === "agent" ? source.name :
                     await getUserName(event.user);

  const messageText = event.text || "";
  log(`[${agentCfg.name}] ${senderName}: ${messageText.slice(0, 100)}`);

  // Load session and add message
  const session = loadSession(channelId);
  const history = formatHistory(session, agentCfg.label);
  session.messages.push({ role: source.type === "agent" ? "agent" : "user", content: messageText, timestamp: Date.now() });

  // Build prompt and spawn Claude
  const prompt = buildPrompt(agentCfg, messageText, senderName, history);
  const reply = await spawnClaude(agentCfg, prompt);

  if (reply) {
    try {
      await webClient.chat.postMessage({
        channel: channelId,
        text: reply.slice(0, 4000),
        thread_ts: event.thread_ts || undefined,
      });
      session.messages.push({ role: "agent", content: reply.slice(0, 500), timestamp: Date.now() });
      saveSession(session);
      log(`[${agentCfg.name}] ${agentCfg.label} replied (${reply.length} chars)`);
    } catch (err) {
      log(`Failed to send reply in ${agentCfg.name}: ${err.message}`);
      saveSession(session);
    }
  } else {
    saveSession(session);
  }

  processing.set(channelId, false);
}

// --- Socket Mode event listener ---

socketClient.on("message", async ({ event, body, ack }) => {
  await ack();
  try {
    await handleMessage(event);
  } catch (err) {
    log(`Error handling message: ${err.message}`);
    // Reset processing state for the channel
    if (event?.channel) processing.set(event.channel, false);
  }
});

// --- Start ---

(async () => {
  try {
    const authResult = await webClient.auth.test();
    botUserId = authResult.user_id;
    log(`Bot identity: ${authResult.user} (${botUserId}) in ${authResult.team}`);
  } catch (err) {
    log(`Failed to get bot identity: ${err.message}`);
  }

  await socketClient.start();
  log(`Socket Mode connected. Watching ${channelMap.size} channel(s):`);
  for (const [chId, cfg] of channelMap) {
    log(`  ${cfg.name} (${chId}) -> ${cfg.cwd}`);
  }
})();
