/**
 * OAuth helper — run this to authenticate each Google account for Drive.
 * Usage: bun run src/auth.ts <label>
 * Example: bun run src/auth.ts personal
 */

import { google } from "googleapis";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { join, dirname } from "path";
import { createServer } from "http";

const SCOPES = [
  "https://www.googleapis.com/auth/drive",
  "https://www.googleapis.com/auth/drive.file",
  "https://www.googleapis.com/auth/spreadsheets",
];
const BASE_DIR = dirname(import.meta.dir);
const TOKENS_DIR = join(BASE_DIR, "tokens");
const CREDS_PATH = join(BASE_DIR, "credentials.json");

const label = process.argv[2];
if (!label) {
  console.error("Usage: bun run src/auth.ts <label>");
  console.error("Example: bun run src/auth.ts personal");
  process.exit(1);
}

if (!existsSync(CREDS_PATH)) {
  console.error(`credentials.json not found at ${CREDS_PATH}`);
  console.error("Copy it from mcp/google-calendar/credentials.json or download from Google Cloud Console.");
  process.exit(1);
}

mkdirSync(TOKENS_DIR, { recursive: true });

const creds = JSON.parse(readFileSync(CREDS_PATH, "utf-8"));
const { client_id, client_secret } = creds.installed || creds.web;

const oauth2 = new google.auth.OAuth2(client_id, client_secret, "http://localhost:3335/callback");

const authUrl = oauth2.generateAuthUrl({
  access_type: "offline",
  scope: SCOPES,
  prompt: "consent",
});

console.log(`\nAuthenticating Google Drive account: "${label}"`);
console.log(`\nOpen this URL in your browser:\n\n${authUrl}\n`);
console.log("Waiting for callback on http://localhost:3335/callback ...\n");

const server = createServer(async (req, res) => {
  if (!req.url?.startsWith("/callback")) {
    res.writeHead(404);
    res.end();
    return;
  }

  const url = new URL(req.url, "http://localhost:3335");
  const code = url.searchParams.get("code");

  if (!code) {
    res.writeHead(400);
    res.end("No code received");
    return;
  }

  try {
    const { tokens } = await oauth2.getToken(code);
    const tokenPath = join(TOKENS_DIR, `${label}.json`);
    writeFileSync(tokenPath, JSON.stringify(tokens, null, 2));

    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(`<h2>Google Drive "${label}" authenticated!</h2><p>You can close this tab.</p>`);

    console.log(`Token saved to ${tokenPath}`);
    console.log(`Google Drive account "${label}" is ready.`);

    setTimeout(() => process.exit(0), 500);
  } catch (err) {
    res.writeHead(500);
    res.end(`Auth failed: ${err}`);
    console.error("Token exchange failed:", err);
    process.exit(1);
  }
});

server.listen(3335);
