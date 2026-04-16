import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { WebClient } from "@slack/web-api";
import { z } from "zod";

const SLACK_TOKEN = process.env.SLACK_BOT_TOKEN;
const OWNER_SLACK_ID = process.env.OWNER_SLACK_ID || "";

if (!SLACK_TOKEN) {
  console.error("SLACK_BOT_TOKEN is required");
  process.exit(1);
}

const slack = new WebClient(SLACK_TOKEN);

const server = new McpServer({
  name: "atlas-slack",
  version: "1.0.0",
});

server.tool(
  "slack_send",
  "Send a message to a Slack channel or DM.",
  {
    channel: z.string().describe("Channel ID or user ID to send to"),
    text: z.string().describe("Message content"),
    thread_ts: z.string().optional().describe("Thread timestamp to reply to"),
  },
  async ({ channel, text, thread_ts }) => {
    const result = await slack.chat.postMessage({
      channel,
      text,
      thread_ts,
    });
    return {
      content: [
        {
          type: "text",
          text: `Sent message ${result.ts} to ${channel}`,
        },
      ],
    };
  }
);

server.tool(
  "slack_dm_owner",
  "Send a DM to the owner (Dina). Shortcut so you don't need to look up the user ID.",
  {
    text: z.string().describe("Message content"),
  },
  async ({ text }) => {
    if (!OWNER_SLACK_ID) {
      return {
        content: [{ type: "text", text: "OWNER_SLACK_ID not configured" }],
        isError: true,
      };
    }
    const result = await slack.chat.postMessage({
      channel: OWNER_SLACK_ID,
      text,
    });
    return {
      content: [
        {
          type: "text",
          text: `Sent DM ${result.ts} to owner`,
        },
      ],
    };
  }
);

server.tool(
  "slack_read",
  "Read recent messages from a channel or DM.",
  {
    channel: z.string().describe("Channel ID to read from"),
    limit: z.coerce.number().optional().describe("Number of messages to fetch (default 10)"),
  },
  async ({ channel, limit }) => {
    const result = await slack.conversations.history({
      channel,
      limit: limit || 10,
    });
    const messages = (result.messages || []).map((m) => ({
      user: m.user || m.bot_id || "unknown",
      text: m.text || "",
      ts: m.ts,
    }));
    return {
      content: [{ type: "text", text: JSON.stringify(messages, null, 2) }],
    };
  }
);

server.tool(
  "slack_channels",
  "List channels the bot can see.",
  {},
  async () => {
    const result = await slack.conversations.list({
      types: "public_channel,private_channel,im",
      limit: 100,
    });
    const channels = (result.channels || []).map((c) => ({
      id: c.id,
      name: c.name || c.user || "dm",
      is_im: c.is_im || false,
    }));
    return {
      content: [{ type: "text", text: JSON.stringify(channels, null, 2) }],
    };
  }
);

server.tool(
  "slack_react",
  "Add an emoji reaction to a message.",
  {
    channel: z.string().describe("Channel ID where the message is"),
    timestamp: z.string().describe("Message timestamp (ts) to react to"),
    emoji: z.string().describe("Emoji name without colons (e.g. 'white_check_mark', 'eyes', 'fire')"),
  },
  async ({ channel, timestamp, emoji }) => {
    await slack.reactions.add({ channel, timestamp, name: emoji });
    return {
      content: [{ type: "text", text: `Reacted :${emoji}: to ${timestamp}` }],
    };
  }
);

server.tool(
  "slack_pin",
  "Pin or unpin a message in a channel.",
  {
    channel: z.string().describe("Channel ID"),
    timestamp: z.string().describe("Message timestamp to pin/unpin"),
    action: z.enum(["pin", "unpin"]).describe("Whether to pin or unpin"),
  },
  async ({ channel, timestamp, action }) => {
    if (action === "pin") {
      await slack.pins.add({ channel, timestamp });
    } else {
      await slack.pins.remove({ channel, timestamp });
    }
    return {
      content: [{ type: "text", text: `${action === "pin" ? "Pinned" : "Unpinned"} message ${timestamp}` }],
    };
  }
);

server.tool(
  "slack_schedule",
  "Schedule a message to be sent at a future time.",
  {
    channel: z.string().describe("Channel ID to send to"),
    text: z.string().describe("Message content"),
    post_at: z.coerce.number().describe("Unix timestamp for when to send the message"),
    thread_ts: z.string().optional().describe("Thread timestamp to reply to"),
  },
  async ({ channel, text, post_at, thread_ts }) => {
    const result = await slack.chat.scheduleMessage({
      channel,
      text,
      post_at,
      thread_ts,
    });
    return {
      content: [
        {
          type: "text",
          text: `Scheduled message ${result.scheduled_message_id} for ${new Date(post_at * 1000).toISOString()}`,
        },
      ],
    };
  }
);

server.tool(
  "slack_upload",
  "Upload a file to a channel.",
  {
    channel: z.string().describe("Channel ID to upload to"),
    filename: z.string().describe("Filename to display"),
    content: z.string().describe("File content as string"),
    title: z.string().optional().describe("Title for the file"),
    initial_comment: z.string().optional().describe("Message to accompany the file"),
    thread_ts: z.string().optional().describe("Thread timestamp to upload into"),
  },
  async ({ channel, filename, content: fileContent, title, initial_comment, thread_ts }) => {
    const result = await slack.filesUploadV2({
      channel_id: channel,
      filename,
      content: fileContent,
      title,
      initial_comment,
      thread_ts,
    });
    return {
      content: [{ type: "text", text: `Uploaded ${filename} to ${channel}` }],
    };
  }
);

server.tool(
  "slack_set_topic",
  "Set the topic or purpose of a channel.",
  {
    channel: z.string().describe("Channel ID"),
    topic: z.string().optional().describe("Channel topic (shows in header)"),
    purpose: z.string().optional().describe("Channel purpose (shows in details)"),
  },
  async ({ channel, topic, purpose }) => {
    const results: string[] = [];
    if (topic !== undefined) {
      await slack.conversations.setTopic({ channel, topic });
      results.push(`Topic set to: ${topic}`);
    }
    if (purpose !== undefined) {
      await slack.conversations.setPurpose({ channel, purpose });
      results.push(`Purpose set to: ${purpose}`);
    }
    return {
      content: [{ type: "text", text: results.join(". ") || "No changes made" }],
    };
  }
);

server.tool(
  "slack_status",
  "Check if the Slack bot is connected and show bot info.",
  {},
  async () => {
    const result = await slack.auth.test();
    return {
      content: [
        {
          type: "text",
          text: `Connected as ${result.user} in workspace ${result.team} (${result.url})`,
        },
      ],
    };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
