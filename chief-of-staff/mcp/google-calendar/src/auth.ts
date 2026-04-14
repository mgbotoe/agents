/**
 * OAuth helper — run this to authenticate each Google account.
 * Usage: bun run src/auth.ts <label>
 * Example: bun run src/auth.ts personal
 *          bun run src/auth.ts business
 */

import { google } from "googleapis";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { join, dirname } from "path";
import { createServer } from "http";

const SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar.events"];
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
  console.error("Download it from Google Cloud Console → Credentials → OAuth 2.0 Client ID");
  process.exit(1);
}

mkdirSync(TOKENS_DIR, { recursive: true });

const creds = JSON.parse(readFileSync(CREDS_PATH, "utf-8"));
const { client_id, client_secret } = creds.installed || creds.web;

const oauth2 = new google.auth.OAuth2(client_id, client_secret, "http://localhost:3333/callback");

const authUrl = oauth2.generateAuthUrl({
  access_type: "offline",
  scope: SCOPES,
  prompt: "consent",
});

console.log(`\nAuthenticating account: "${label}"`);
console.log(`\nOpen this URL in your browser:\n\n${authUrl}\n`);
console.log("Waiting for callback on http://localhost:3333/callback ...\n");

const server = createServer(async (req, res) => {
  if (!req.url?.startsWith("/callback")) {
    res.writeHead(404);
    res.end();
    return;
  }

  const url = new URL(req.url, "http://localhost:3333");
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
    res.end(`<h2>Account "${label}" authenticated!</h2><p>You can close this tab.</p>`);

    console.log(`Token saved to ${tokenPath}`);
    console.log(`Account "${label}" is ready.`);

    setTimeout(() => process.exit(0), 500);
  } catch (err) {
    res.writeHead(500);
    res.end(`Auth failed: ${err}`);
    console.error("Token exchange failed:", err);
    process.exit(1);
  }
});

server.listen(3333);
