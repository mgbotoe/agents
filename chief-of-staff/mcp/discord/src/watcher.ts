/**
 * Discord Watcher — runs independently, triggers Claude Code when a message arrives.
 *
 * Session persistence: maintains a rolling conversation history per channel
 * so Claude has context from recent messages, not just the latest one.
 *
 * Usage: bun run mcp/discord/src/watcher.ts
 * Stop: Ctrl+C or close the window
 */

import { Client, Events, GatewayIntentBits, Partials, type Message } from "discord.js";
import { spawn } from "child_process";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { join } from "path";

// Load config from .mcp.json
const PROJECT_DIR = "C:\\Workspace\\agents\\chief-of-staff";
const mcpConfig = JSON.parse(readFileSync(join(PROJECT_DIR, ".mcp.json"), "utf-8"));
const DISCORD_TOKEN = mcpConfig.mcpServers["atlas-discord"].env.DISCORD_BOT_TOKEN;
const OWNER_ID = mcpConfig.mcpServers["atlas-discord"].env.DISCORD_OWNER_ID;

if (!DISCORD_TOKEN) {
  console.error("No DISCORD_BOT_TOKEN found in .mcp.json");
  process.exit(1);
}

// --- Session persistence ---
const SESSIONS_DIR = join(PROJECT_DIR, ".claude", "runtime", "discord-sessions");
const MAX_HISTORY = 20; // keep last 20 messages per channel
const SESSION_TTL = 30 * 60 * 1000; // 30 min — after this, start fresh context

interface SessionMessage {
  role: "user" | "atlas";
  content: string;
  timestamp: number;
}

interface Session {
  channelId: string;
  messages: SessionMessage[];
  lastActivity: number;
}

function getSessionPath(channelId: string): string {
  return join(SESSIONS_DIR, `${channelId}.json`);
}

function loadSession(channelId: string): Session {
  const path = getSessionPath(channelId);
  if (existsSync(path)) {
    try {
      const session: Session = JSON.parse(readFileSync(path, "utf-8"));
      // Check if session is stale (30 min inactivity = fresh start)
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

function saveSession(session: Session): void {
  mkdirSync(SESSIONS_DIR, { recursive: true });
  // Trim to max history
  if (session.messages.length > MAX_HISTORY) {
    session.messages = session.messages.slice(-MAX_HISTORY);
  }
  session.lastActivity = Date.now();
  writeFileSync(getSessionPath(session.channelId), JSON.stringify(session, null, 2));
}

function formatHistory(session: Session): string {
  if (session.messages.length === 0) return "";

  const lines = session.messages.map((m) => {
    const who = m.role === "user" ? "Dina" : "Atlas";
    return `${who}: ${m.content}`;
  });

  return `\n\nCONVERSATION HISTORY (most recent messages):\n${lines.join("\n")}\n\n`;
}

// Track active sessions to prevent overlapping responses
let isProcessing = false;
const LOG_FILE = join(PROJECT_DIR, ".claude", "runtime", "discord-watcher.log");

function log(msg: string) {
  const timestamp = new Date().toISOString().replace("T", " ").slice(0, 19);
  const line = `[${timestamp}] watcher: ${msg}`;
  console.log(line);
  try {
    mkdirSync(join(PROJECT_DIR, ".claude", "runtime"), { recursive: true });
    const fs = require("fs");
    fs.appendFileSync(LOG_FILE, line + "\n");
  } catch { /* ignore log failures */ }
}

// Discord client
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.DirectMessages,
    GatewayIntentBits.MessageContent,
  ],
  partials: [Partials.Channel, Partials.Message],
});

client.once(Events.ClientReady, (c) => {
  log(`Connected as ${c.user.tag}. Watching for messages from owner ${OWNER_ID}.`);
});

client.on(Events.MessageCreate, async (msg: Message) => {
  if (msg.author.bot) return;
  if (msg.author.id !== OWNER_ID) return;

  if (isProcessing) {
    log(`Skipping message (already processing): ${msg.content.slice(0, 50)}`);
    return;
  }

  isProcessing = true;
  const content = msg.content;
  const channelId = msg.channelId;
  const isDM = !msg.guild;

  log(`Message from owner${isDM ? " (DM)" : ""}: ${content.slice(0, 100)}`);

  // Show typing indicator
  try {
    if ("sendTyping" in msg.channel) {
      await msg.channel.sendTyping();
    }
  } catch { /* ignore */ }

  // Load session history
  const session = loadSession(channelId);
  const history = formatHistory(session);

  // Add this message to session
  session.messages.push({ role: "user", content, timestamp: Date.now() });

  // Build prompt with history
  const promptDir = join(PROJECT_DIR, ".claude", "runtime");
  mkdirSync(promptDir, { recursive: true });
  const promptFile = join(promptDir, "discord-prompt.txt");

  // Get current date/time for the prompt
  const now = new Date();
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const dayName = days[now.getDay()];
  const dateStr = now.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
  const timeStr = now.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", hour12: true, timeZone: "America/Los_Angeles" });

  const prompt = `You are Atlas, Dina's Chief of Staff. Dina is messaging you on Discord.

CURRENT DATE/TIME: ${dayName}, ${dateStr} at ${timeStr} PT. Use this as the source of truth for today's date and day of the week.
${history}Dina's latest message: ${content}

You MUST respond to what she said. Read the conversation history for context — don't repeat yourself or ask things she already answered.

Rules:
- Read the wiki at C:\\Workspace\\agents\\wiki\\index.md if the question involves people, projects, or past work
- Use MCP tools (gcal, gmail, gdrive) as needed — but NEVER use discord tools
- Your entire stdout output will be sent as the Discord reply, so output ONLY the reply text
- No tool result summaries, no "I used X tool", no markdown headers — just the response
- Keep it under 500 chars unless the question requires detail
- Be casual, direct, no AI slop. You're a chief of staff, not a chatbot.
- If she tells you something new, acknowledge it and update the wiki if relevant
- If she asks you to do something, do it with tools and confirm what you did
- If the conversation history shows you already discussed something, build on it — don't start over`;

  writeFileSync(promptFile, prompt, "utf-8");

  try {
    const proc = spawn("claude", ["-p", readFileSync(promptFile, "utf-8"), "--dangerously-skip-permissions"], {
      cwd: PROJECT_DIR,
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";

    proc.stdout.on("data", (data: Buffer) => { stdout += data.toString(); });
    proc.stderr.on("data", (data: Buffer) => { stderr += data.toString(); });

    proc.on("close", async (code: number) => {
      if (code === 0 && stdout.trim()) {
        const lines = stdout.trim().split("\n");
        const cleaned = lines
          .filter(l => l.trim())
          .filter(l => !l.startsWith("╭") && !l.startsWith("│") && !l.startsWith("╰"))
          .filter(l => !l.startsWith(">"))
          .filter(l => !l.includes("tool_use") && !l.includes("content_block"))
          .join("\n")
          .trim();

        const reply = cleaned.slice(0, 2000);

        if (reply) {
          try {
            await msg.reply(reply);
            // Save Atlas's reply to session history
            session.messages.push({ role: "atlas", content: reply, timestamp: Date.now() });
            saveSession(session);
            log(`Reply sent for: ${content.slice(0, 50)}`);
          } catch (sendErr) {
            log(`Failed to send reply: ${sendErr}`);
          }
        } else {
          log(`Empty reply after filtering for: ${content.slice(0, 50)}`);
        }
      } else {
        log(`Claude session failed (exit ${code}): ${stderr.slice(0, 200)}`);
        // Still save the user message so next attempt has context
        saveSession(session);
      }
      isProcessing = false;
    });

    // Timeout after 2 minutes
    setTimeout(() => {
      if (isProcessing) {
        proc.kill();
        isProcessing = false;
        saveSession(session);
        log(`Session timed out for: ${content.slice(0, 50)}`);
      }
    }, 120000);

  } catch (err) {
    isProcessing = false;
    saveSession(session);
    log(`Failed to spawn Claude: ${err}`);
  }
});

// Start
client.login(DISCORD_TOKEN);
log("Watcher starting...");
