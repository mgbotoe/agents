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
import { spawn, execFileSync } from "child_process";
import { readFileSync, writeFileSync, unlinkSync, openSync, closeSync, mkdirSync, existsSync, appendFileSync } from "fs";
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
// Default webClient uses the Socket Mode app's bot token — used for auth.test
// (bot identity on startup) and user lookups.
const webClient = new WebClient(SLACK_BOT_TOKEN);

// Per-agent WebClient so replies post as the correct agent (Atlas vs Polaris
// have separate Slack apps / bot users in DaFudge). Falls back to the default
// token if an agent's botTokenEnv is missing or unset.
const agentWebClients = new Map();
for (const [chId, agentCfg] of Object.entries(config.agents)) {
  const token = agentCfg.botTokenEnv ? process.env[agentCfg.botTokenEnv] : null;
  agentWebClients.set(chId, token ? new WebClient(token) : webClient);
}

const SESSIONS_DIR = join(__dirname, "sessions");
const LOG_FILE = join(__dirname, "watcher.log");
const PID_FILE = join(__dirname, "watcher.pid");
const MAX_HISTORY = config.maxHistory || 20;
const SESSION_TTL = (config.sessionTtlMinutes || 30) * 60 * 1000;
const TIMEOUT_MS = config.timeoutMs || 120000;

// Map channel IDs to agent configs
const channelMap = new Map(Object.entries(config.agents));

// Track processing state per channel (allows parallel across agents)
const processing = new Map();

// Resolve bot's own user ID on startup (to ignore own messages)
let botUserId = null;

// --- Single-instance guard via PID file ---
// Uses two-layer protection:
//   Layer 1: atomic exclusive-create lock file (wx flag) — prevents concurrent startup race
//   Layer 2: PID file with wmic/tasklist verification — handles stale PIDs from crashes

const LOCK_FILE = PID_FILE + ".lock";

function isLiveWatcher(pid) {
  if (process.platform !== "win32") {
    try { process.kill(pid, 0); return true; } catch { return false; }
  }
  // Windows: wmic is deprecated on Win11; use PowerShell Get-WmiObject to verify
  // the PID is actually running watcher.mjs (process.kill is unreliable on Windows).
  try {
    const out = execFileSync(
      "powershell.exe",
      ["-NonInteractive", "-NoProfile", "-Command",
        `(Get-WmiObject Win32_Process -Filter 'ProcessId=${pid}').CommandLine`],
      { encoding: "utf8", timeout: 5000, windowsHide: true }
    );
    return out.toLowerCase().includes("watcher.mjs");
  } catch { return false; }
}

function checkSingleInstance() {
  // Layer 1: atomic lock — only one process can create this file (O_EXCL).
  // Concurrent starts all race here; exactly one wins, the rest get EEXIST.
  let lockFd = null;
  try {
    lockFd = openSync(LOCK_FILE, "wx");
  } catch (err) {
    if (err.code === "EEXIST") {
      // Another instance is in the middle of starting up right now. Exit.
      console.error("[watcher] Startup lock held by concurrent process. Exiting.");
      process.exit(0);
    }
    // Any other error (permissions, disk full) — log and continue without lock
    console.warn(`[watcher] Could not create lock file: ${err.message}. Proceeding without lock.`);
  }
  if (lockFd !== null) closeSync(lockFd);

  // Layer 2: PID file check — handles restarts after crash (lock file gone, PID file stale).
  if (existsSync(PID_FILE)) {
    try {
      const existingPid = parseInt(readFileSync(PID_FILE, "utf-8").trim(), 10);
      if (!isNaN(existingPid) && isLiveWatcher(existingPid)) {
        console.error(`[watcher] Already running as PID ${existingPid}. Exiting to prevent duplicate.`);
        try { unlinkSync(LOCK_FILE); } catch { /* ok */ }
        process.exit(0);
      }
      console.log(`[watcher] Stale PID file (PID ${existingPid} not a live watcher). Starting fresh.`);
    } catch {
      // Unreadable PID file — ignore and continue
    }
  }

  writeFileSync(PID_FILE, String(process.pid));
  try { unlinkSync(LOCK_FILE); } catch { /* ok */ }
}

function removePidFile() {
  try {
    if (existsSync(PID_FILE)) {
      const stored = parseInt(readFileSync(PID_FILE, "utf-8").trim(), 10);
      if (stored === process.pid) unlinkSync(PID_FILE);
    }
  } catch { /* ignore */ }
  try { unlinkSync(LOCK_FILE); } catch { /* ignore */ }
}

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

// On Windows, Node's spawn() doesn't resolve PATHEXT — "claude" is `claude.cmd`
// which also must be run with `shell: true` per Node 20+ security policy
// (see https://nodejs.org/api/child_process.html#spawning-bat-and-cmd-files-on-windows).
// Without these, the watcher dies with ENOENT / EINVAL when launched from a
// detached cmd.exe (Startup folder / Task Scheduler).
const IS_WIN = process.platform === "win32";
const CLAUDE_BIN = "claude"; // claude.exe on Windows, claude on Unix — both resolved via shell/PATH

function spawnClaude(agentCfg, prompt) {
  return new Promise((resolve) => {
    // Pipe prompt via stdin rather than argv. With `shell: true` on Windows,
    // Node joins argv with spaces into a raw command string without quoting
    // individual args — cmd.exe then word-splits the prompt, making `-p`
    // grab only the first whitespace-delimited token ("You" from "You are
    // Polaris…"). stdin-piping sidesteps the quoting problem entirely.
    const proc = spawn(CLAUDE_BIN, ["-p", "--dangerously-skip-permissions"], {
      cwd: agentCfg.cwd,
      stdio: ["pipe", "pipe", "pipe"],
      shell: IS_WIN,
      windowsHide: true,
    });

    let stdout = "";
    let stderr = "";

    proc.stdout.on("data", (data) => { stdout += data.toString(); });
    proc.stderr.on("data", (data) => { stderr += data.toString(); });

    // Write prompt to stdin then close so Claude exits after processing
    proc.stdin.write(prompt);
    proc.stdin.end();

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

  // Self-loop protection handled at the agent-identity layer below
  // (`source.name === agentCfg.label` inside the bot_message block).
  // A user-ID check here over-filters: the listening bot IS one of the posting
  // agents (Polaris), so filtering by botUserId blocks cross-channel agent
  // traffic (Polaris posting to #atlas-cos to notify Atlas).

  // Ignore message subtypes (edits, joins, etc.) except bot_message from other agents
  if (event.subtype && event.subtype !== "bot_message") return;

  // If this is a bot_message, check if it's from a known agent
  if (event.subtype === "bot_message") {
    const source = getMessageSource(event);
    if (source.type !== "agent") return; // unknown bot, ignore
    if (source.name === agentCfg.label) return; // own channel's agent reply — skip (per-agent tokens break user-id self-filter)
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
      // Post as the spawned agent (their own bot token), not as the watcher's
      // listening bot — otherwise Atlas replies appear from Polaris's avatar.
      const agentClient = agentWebClients.get(channelId) || webClient;
      await agentClient.chat.postMessage({
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

// Socket lifecycle logging — surface connection issues instead of drowning
// in ping/pong timeout warnings from the default logger
socketClient.on("error", (err) => {
  log(`[socket error] ${err?.message || err}`);
});
socketClient.on("disconnected", (err) => {
  log(`[socket disconnected] ${err?.message || "no reason"}; auto-reconnect will retry`);
});
socketClient.on("reconnecting", () => {
  log("[socket reconnecting]");
});
socketClient.on("connected", () => {
  log("[socket connected]");
});

// Process-level resilience — exit with code 1 so the supervisor restart loop
// picks us back up. Without this, unhandled errors kill the process silently
// and the watcher stays dead until manual restart.
process.on("uncaughtException", (err) => {
  log(`[FATAL uncaughtException] ${err?.stack || err}`);
  removePidFile();
  process.exit(1);
});
process.on("unhandledRejection", (reason) => {
  log(`[FATAL unhandledRejection] ${reason?.stack || reason}`);
  removePidFile();
  process.exit(1);
});
process.on("SIGINT", () => {
  log("[SIGINT] shutting down");
  removePidFile();
  process.exit(0);
});
process.on("SIGTERM", () => {
  log("[SIGTERM] shutting down");
  removePidFile();
  process.exit(0);
});

// --- Start ---

(async () => {
  checkSingleInstance();

  try {
    const authResult = await webClient.auth.test();
    botUserId = authResult.user_id;
    log(`Bot identity: ${authResult.user} (${botUserId}) in ${authResult.team}`);
  } catch (err) {
    log(`Failed to get bot identity: ${err.message}`);
  }

  // Keep the event loop alive even when all sessions have resolved and the
  // WebSocket is mid-reconnect (brief gap where no active handles remain).
  setInterval(() => {}, 60000);

  await socketClient.start();
  log(`Socket Mode connected. Watching ${channelMap.size} channel(s):`);
  for (const [chId, cfg] of channelMap) {
    log(`  ${cfg.name} (${chId}) -> ${cfg.cwd}`);
  }
})();
