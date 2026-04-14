import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { google, type gmail_v1 } from "googleapis";
import { readFileSync, readdirSync, existsSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import { z } from "zod";

// --- Config ---
const BASE_DIR = join(dirname(import.meta.dir));
const TOKENS_DIR = join(BASE_DIR, "tokens");
const CREDS_PATH = join(BASE_DIR, "credentials.json");

// --- Account management ---
interface Account {
  label: string;
  gmail: gmail_v1.Gmail;
}

function loadAccounts(): Account[] {
  if (!existsSync(CREDS_PATH) || !existsSync(TOKENS_DIR)) return [];

  const creds = JSON.parse(readFileSync(CREDS_PATH, "utf-8"));
  const { client_id, client_secret } = creds.installed || creds.web;
  const accounts: Account[] = [];

  for (const file of readdirSync(TOKENS_DIR)) {
    if (!file.endsWith(".json")) continue;

    const label = file.replace(".json", "");
    const tokens = JSON.parse(readFileSync(join(TOKENS_DIR, file), "utf-8"));

    const auth = new google.auth.OAuth2(client_id, client_secret, "http://localhost:3334/callback");
    auth.setCredentials(tokens);

    auth.on("tokens", (newTokens) => {
      const merged = { ...tokens, ...newTokens };
      writeFileSync(join(TOKENS_DIR, file), JSON.stringify(merged, null, 2));
    });

    const gmail = google.gmail({ version: "v1", auth });
    accounts.push({ label, gmail });
  }

  return accounts;
}

let accounts = loadAccounts();

function getAccount(label?: string): Account | undefined {
  if (!label) return accounts[0];
  return accounts.find((a) => a.label === label);
}

function accountLabels(): string[] {
  return accounts.map((a) => a.label);
}

function decodeBody(part: gmail_v1.Schema$MessagePart): string {
  if (part.body?.data) {
    return Buffer.from(part.body.data, "base64url").toString("utf-8");
  }
  if (part.parts) {
    const textPart = part.parts.find((p) => p.mimeType === "text/plain");
    if (textPart?.body?.data) {
      return Buffer.from(textPart.body.data, "base64url").toString("utf-8");
    }
    const htmlPart = part.parts.find((p) => p.mimeType === "text/html");
    if (htmlPart?.body?.data) {
      return Buffer.from(htmlPart.body.data, "base64url").toString("utf-8")
        .replace(/<[^>]+>/g, " ")
        .replace(/\s+/g, " ")
        .trim();
    }
    for (const p of part.parts) {
      const result = decodeBody(p);
      if (result) return result;
    }
  }
  return "";
}

function getHeader(headers: gmail_v1.Schema$MessagePartHeader[] | undefined, name: string): string {
  return headers?.find((h) => h.name?.toLowerCase() === name.toLowerCase())?.value || "";
}

// --- MCP Server ---
const server = new McpServer({
  name: "atlas-gmail",
  version: "1.0.0",
});

server.tool(
  "gmail_accounts",
  "List all connected Gmail accounts.",
  {},
  async () => {
    accounts = loadAccounts();
    const info: { label: string; email: string }[] = [];

    for (const acc of accounts) {
      try {
        const profile = await acc.gmail.users.getProfile({ userId: "me" });
        info.push({ label: acc.label, email: profile.data.emailAddress || "unknown" });
      } catch (err) {
        info.push({ label: acc.label, email: `Error: ${err}` });
      }
    }

    return { content: [{ type: "text", text: JSON.stringify(info, null, 2) }] };
  }
);

server.tool(
  "gmail_search",
  "Search emails across one or all accounts. Uses Gmail search syntax.",
  {
    query: z.string().describe("Gmail search query (e.g. 'from:boss@co.com', 'subject:invoice', 'is:unread')"),
    account: z.string().optional().describe("Account label. Omit for all."),
    max_results: z.number().min(1).max(20).default(10).describe("Max results per account"),
  },
  async ({ query, account, max_results }) => {
    const targetAccounts = account ? [getAccount(account)].filter(Boolean) as Account[] : accounts;
    const results: { account: string; messages: object[] }[] = [];

    for (const acc of targetAccounts) {
      try {
        const res = await acc.gmail.users.messages.list({
          userId: "me",
          q: query,
          maxResults: max_results,
        });

        const messages: object[] = [];
        for (const msg of res.data.messages || []) {
          const full = await acc.gmail.users.messages.get({
            userId: "me",
            id: msg.id!,
            format: "metadata",
            metadataHeaders: ["From", "To", "Subject", "Date"],
          });

          messages.push({
            id: msg.id,
            threadId: msg.threadId,
            from: getHeader(full.data.payload?.headers, "From"),
            to: getHeader(full.data.payload?.headers, "To"),
            subject: getHeader(full.data.payload?.headers, "Subject"),
            date: getHeader(full.data.payload?.headers, "Date"),
            snippet: full.data.snippet,
            labels: full.data.labelIds,
          });
        }

        results.push({ account: acc.label, messages });
      } catch (err) {
        results.push({ account: acc.label, messages: [{ error: `${err}` }] });
      }
    }

    return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
  }
);

server.tool(
  "gmail_read",
  "Read the full content of an email by ID.",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID from gmail_search results"),
  },
  async ({ account, message_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.gmail.users.messages.get({
        userId: "me",
        id: message_id,
        format: "full",
      });

      const headers = res.data.payload?.headers;
      const body = res.data.payload ? decodeBody(res.data.payload) : "";

      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            from: getHeader(headers, "From"),
            to: getHeader(headers, "To"),
            cc: getHeader(headers, "Cc"),
            subject: getHeader(headers, "Subject"),
            date: getHeader(headers, "Date"),
            body: body.slice(0, 5000),
            labels: res.data.labelIds,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_unread",
  "Get unread emails across one or all accounts.",
  {
    account: z.string().optional().describe("Account label. Omit for all."),
    max_results: z.number().min(1).max(20).default(10).describe("Max results per account"),
  },
  async ({ account, max_results }) => {
    const targetAccounts = account ? [getAccount(account)].filter(Boolean) as Account[] : accounts;
    const results: { account: string; unread_count: number; messages: object[] }[] = [];

    for (const acc of targetAccounts) {
      try {
        const res = await acc.gmail.users.messages.list({
          userId: "me",
          q: "is:unread",
          maxResults: max_results,
        });

        const total = res.data.resultSizeEstimate || 0;
        const messages: object[] = [];

        for (const msg of (res.data.messages || []).slice(0, max_results)) {
          const full = await acc.gmail.users.messages.get({
            userId: "me",
            id: msg.id!,
            format: "metadata",
            metadataHeaders: ["From", "Subject", "Date"],
          });

          messages.push({
            id: msg.id,
            from: getHeader(full.data.payload?.headers, "From"),
            subject: getHeader(full.data.payload?.headers, "Subject"),
            date: getHeader(full.data.payload?.headers, "Date"),
            snippet: full.data.snippet,
          });
        }

        results.push({ account: acc.label, unread_count: total, messages });
      } catch (err) {
        results.push({ account: acc.label, unread_count: 0, messages: [{ error: `${err}` }] });
      }
    }

    return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
  }
);

server.tool(
  "gmail_draft",
  "Create a draft email.",
  {
    account: z.string().describe("Account label to send from"),
    to: z.string().describe("Recipient email address"),
    subject: z.string().describe("Email subject"),
    body: z.string().describe("Email body (plain text)"),
    cc: z.string().optional().describe("CC recipients (comma-separated)"),
    in_reply_to: z.string().optional().describe("Message ID to reply to (creates a reply draft)"),
  },
  async ({ account, to, subject, body, cc, in_reply_to }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      let headers = `To: ${to}\nSubject: ${subject}\nContent-Type: text/plain; charset=utf-8\n`;
      if (cc) headers += `Cc: ${cc}\n`;

      let threadId: string | undefined;
      if (in_reply_to) {
        const original = await acc.gmail.users.messages.get({ userId: "me", id: in_reply_to, format: "metadata" });
        threadId = original.data.threadId || undefined;
        const msgId = getHeader(original.data.payload?.headers, "Message-ID");
        if (msgId) headers += `In-Reply-To: ${msgId}\nReferences: ${msgId}\n`;
      }

      const raw = Buffer.from(`${headers}\n${body}`).toString("base64url");

      const res = await acc.gmail.users.drafts.create({
        userId: "me",
        requestBody: {
          message: { raw, threadId },
        },
      });

      return {
        content: [{ type: "text", text: `Draft created (ID: ${res.data.id}). Open Gmail to review and send.` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_labels",
  "List all labels/folders for an account.",
  {
    account: z.string().describe("Account label"),
  },
  async ({ account }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.gmail.users.labels.list({ userId: "me" });
      const labels = (res.data.labels || []).map((l) => ({ id: l.id, name: l.name, type: l.type }));
      return { content: [{ type: "text", text: JSON.stringify(labels, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- Sending ---

server.tool(
  "gmail_send",
  "Send a new email or reply to an existing thread.",
  {
    account: z.string().describe("Account label"),
    to: z.string().describe("Recipient email address"),
    subject: z.string().describe("Email subject"),
    body: z.string().describe("Email body (plain text)"),
    cc: z.string().optional().describe("CC recipients (comma-separated)"),
    bcc: z.string().optional().describe("BCC recipients (comma-separated)"),
    in_reply_to: z.string().optional().describe("Message ID to reply to (threads the reply)"),
  },
  async ({ account, to, subject, body, cc, bcc, in_reply_to }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      let headers = `To: ${to}\nSubject: ${subject}\nContent-Type: text/plain; charset=utf-8\n`;
      if (cc) headers += `Cc: ${cc}\n`;
      if (bcc) headers += `Bcc: ${bcc}\n`;

      let threadId: string | undefined;
      if (in_reply_to) {
        const original = await acc.gmail.users.messages.get({ userId: "me", id: in_reply_to, format: "metadata", metadataHeaders: ["Message-ID"] });
        threadId = original.data.threadId || undefined;
        const msgId = getHeader(original.data.payload?.headers, "Message-ID");
        if (msgId) headers += `In-Reply-To: ${msgId}\nReferences: ${msgId}\n`;
      }

      const raw = Buffer.from(`${headers}\n${body}`).toString("base64url");

      const res = await acc.gmail.users.messages.send({
        userId: "me",
        requestBody: { raw, threadId },
      });

      return {
        content: [{ type: "text", text: `Sent (ID: ${res.data.id}, Thread: ${res.data.threadId}).` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_forward",
  "Forward an email to another recipient.",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID to forward"),
    to: z.string().describe("Recipient email address"),
    comment: z.string().optional().describe("Text to add above forwarded content"),
  },
  async ({ account, message_id, to, comment }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const original = await acc.gmail.users.messages.get({ userId: "me", id: message_id, format: "full" });
      const origHeaders = original.data.payload?.headers;
      const origFrom = getHeader(origHeaders, "From");
      const origDate = getHeader(origHeaders, "Date");
      const origSubject = getHeader(origHeaders, "Subject");
      const origTo = getHeader(origHeaders, "To");
      const origBody = original.data.payload ? decodeBody(original.data.payload) : "";

      const fwdHeader = `---------- Forwarded message ----------\nFrom: ${origFrom}\nDate: ${origDate}\nSubject: ${origSubject}\nTo: ${origTo}\n\n`;
      const fullBody = (comment ? `${comment}\n\n` : "") + fwdHeader + origBody;

      const subject = origSubject.startsWith("Fwd:") ? origSubject : `Fwd: ${origSubject}`;
      const headers = `To: ${to}\nSubject: ${subject}\nContent-Type: text/plain; charset=utf-8\n`;
      const raw = Buffer.from(`${headers}\n${fullBody}`).toString("base64url");

      const res = await acc.gmail.users.messages.send({
        userId: "me",
        requestBody: { raw },
      });

      return {
        content: [{ type: "text", text: `Forwarded to ${to} (ID: ${res.data.id}).` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- Drafts ---

server.tool(
  "gmail_send_draft",
  "Send an existing draft.",
  {
    account: z.string().describe("Account label"),
    draft_id: z.string().describe("Draft ID to send"),
  },
  async ({ account, draft_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.gmail.users.drafts.send({
        userId: "me",
        requestBody: { id: draft_id },
      });

      return {
        content: [{ type: "text", text: `Draft sent (Message ID: ${res.data.id}).` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_update_draft",
  "Update an existing draft with new content.",
  {
    account: z.string().describe("Account label"),
    draft_id: z.string().describe("Draft ID to update"),
    to: z.string().describe("Recipient email address"),
    subject: z.string().describe("Email subject"),
    body: z.string().describe("Email body (plain text)"),
    cc: z.string().optional().describe("CC recipients (comma-separated)"),
  },
  async ({ account, draft_id, to, subject, body, cc }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      let headers = `To: ${to}\nSubject: ${subject}\nContent-Type: text/plain; charset=utf-8\n`;
      if (cc) headers += `Cc: ${cc}\n`;

      const raw = Buffer.from(`${headers}\n${body}`).toString("base64url");

      const res = await acc.gmail.users.drafts.update({
        userId: "me",
        id: draft_id,
        requestBody: {
          message: { raw },
        },
      });

      return {
        content: [{ type: "text", text: `Draft updated (ID: ${res.data.id}).` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_delete_draft",
  "Permanently delete a draft.",
  {
    account: z.string().describe("Account label"),
    draft_id: z.string().describe("Draft ID to delete"),
  },
  async ({ account, draft_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.gmail.users.drafts.delete({ userId: "me", id: draft_id });
      return {
        content: [{ type: "text", text: `Draft ${draft_id} deleted.` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_list_drafts",
  "List drafts in the mailbox.",
  {
    account: z.string().describe("Account label"),
    max_results: z.number().min(1).max(50).default(10).describe("Max drafts to return"),
  },
  async ({ account, max_results }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.gmail.users.drafts.list({ userId: "me", maxResults: max_results });
      const drafts: object[] = [];

      for (const draft of res.data.drafts || []) {
        const full = await acc.gmail.users.drafts.get({ userId: "me", id: draft.id!, format: "metadata" });
        const headers = full.data.message?.payload?.headers;
        drafts.push({
          id: draft.id,
          messageId: full.data.message?.id,
          to: getHeader(headers, "To"),
          subject: getHeader(headers, "Subject"),
          date: getHeader(headers, "Date"),
          snippet: full.data.message?.snippet,
        });
      }

      return { content: [{ type: "text", text: JSON.stringify(drafts, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- Threads ---

server.tool(
  "gmail_get_thread",
  "Get a full email thread with all messages.",
  {
    account: z.string().describe("Account label"),
    thread_id: z.string().describe("Thread ID"),
  },
  async ({ account, thread_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.gmail.users.threads.get({ userId: "me", id: thread_id, format: "full" });
      const messages = (res.data.messages || []).map((msg) => ({
        id: msg.id,
        from: getHeader(msg.payload?.headers, "From"),
        to: getHeader(msg.payload?.headers, "To"),
        subject: getHeader(msg.payload?.headers, "Subject"),
        date: getHeader(msg.payload?.headers, "Date"),
        body: msg.payload ? decodeBody(msg.payload).slice(0, 3000) : "",
        labels: msg.labelIds,
      }));

      return {
        content: [{ type: "text", text: JSON.stringify({ threadId: thread_id, messageCount: messages.length, messages }, null, 2) }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- Message actions ---

server.tool(
  "gmail_archive",
  "Archive an email (remove from inbox).",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID to archive"),
  },
  async ({ account, message_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.gmail.users.messages.modify({
        userId: "me",
        id: message_id,
        requestBody: { removeLabelIds: ["INBOX"] },
      });
      return { content: [{ type: "text", text: `Archived message ${message_id}.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_trash",
  "Move an email to trash.",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID to trash"),
  },
  async ({ account, message_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.gmail.users.messages.trash({ userId: "me", id: message_id });
      return { content: [{ type: "text", text: `Trashed message ${message_id}.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_star",
  "Add star to an email.",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID to star"),
  },
  async ({ account, message_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.gmail.users.messages.modify({
        userId: "me",
        id: message_id,
        requestBody: { addLabelIds: ["STARRED"] },
      });
      return { content: [{ type: "text", text: `Starred message ${message_id}.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_unstar",
  "Remove star from an email.",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID to unstar"),
  },
  async ({ account, message_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.gmail.users.messages.modify({
        userId: "me",
        id: message_id,
        requestBody: { removeLabelIds: ["STARRED"] },
      });
      return { content: [{ type: "text", text: `Unstarred message ${message_id}.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_mark_read",
  "Mark an email as read.",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID"),
  },
  async ({ account, message_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.gmail.users.messages.modify({
        userId: "me",
        id: message_id,
        requestBody: { removeLabelIds: ["UNREAD"] },
      });
      return { content: [{ type: "text", text: `Marked ${message_id} as read.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_mark_unread",
  "Mark an email as unread.",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID"),
  },
  async ({ account, message_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.gmail.users.messages.modify({
        userId: "me",
        id: message_id,
        requestBody: { addLabelIds: ["UNREAD"] },
      });
      return { content: [{ type: "text", text: `Marked ${message_id} as unread.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- Label management ---

server.tool(
  "gmail_update_labels",
  "Update labels on an email (add and/or remove).",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID"),
    add_labels: z.array(z.string()).optional().describe("Label IDs to add"),
    remove_labels: z.array(z.string()).optional().describe("Label IDs to remove"),
  },
  async ({ account, message_id, add_labels, remove_labels }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.gmail.users.messages.modify({
        userId: "me",
        id: message_id,
        requestBody: {
          addLabelIds: add_labels || [],
          removeLabelIds: remove_labels || [],
        },
      });
      return { content: [{ type: "text", text: `Updated labels on ${message_id}.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gmail_create_label",
  "Create a new Gmail label.",
  {
    account: z.string().describe("Account label"),
    name: z.string().describe("Label name to create"),
  },
  async ({ account, name }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.gmail.users.labels.create({
        userId: "me",
        requestBody: { name, labelListVisibility: "labelShow", messageListVisibility: "show" },
      });
      return {
        content: [{ type: "text", text: `Label created: "${res.data.name}" (ID: ${res.data.id}).` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- Batch operations ---

server.tool(
  "gmail_batch_update",
  "Modify labels on multiple emails at once.",
  {
    account: z.string().describe("Account label"),
    message_ids: z.array(z.string()).describe("Array of message IDs to modify"),
    add_labels: z.array(z.string()).optional().describe("Label IDs to add"),
    remove_labels: z.array(z.string()).optional().describe("Label IDs to remove"),
  },
  async ({ account, message_ids, add_labels, remove_labels }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.gmail.users.messages.batchModify({
        userId: "me",
        requestBody: {
          ids: message_ids,
          addLabelIds: add_labels || [],
          removeLabelIds: remove_labels || [],
        },
      });
      return { content: [{ type: "text", text: `Batch updated ${message_ids.length} messages.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- Attachments ---

server.tool(
  "gmail_get_attachment",
  "Download an attachment and return its base64 data.",
  {
    account: z.string().describe("Account label"),
    message_id: z.string().describe("Message ID containing the attachment"),
    attachment_id: z.string().describe("Attachment ID"),
  },
  async ({ account, message_id, attachment_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.gmail.users.messages.attachments.get({
        userId: "me",
        messageId: message_id,
        id: attachment_id,
      });

      return {
        content: [{ type: "text", text: JSON.stringify({ size: res.data.size, data: res.data.data }, null, 2) }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- Start ---
async function main() {
  if (accounts.length === 0) {
    console.error("No accounts authenticated. Run: bun run src/auth.ts <label>");
  } else {
    console.error(`Loaded ${accounts.length} Gmail account(s): ${accountLabels().join(", ")}`);
  }

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
