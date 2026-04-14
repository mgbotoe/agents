import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  Client,
  Events,
  GatewayIntentBits,
  Partials,
  type Message,
} from "discord.js";
import { z } from "zod";

// --- Config ---
const DISCORD_TOKEN = process.env.DISCORD_BOT_TOKEN;
const OWNER_ID = process.env.DISCORD_OWNER_ID || "";

if (!DISCORD_TOKEN) {
  console.error("DISCORD_BOT_TOKEN is required");
  process.exit(1);
}

// --- Message queue ---
interface QueuedMessage {
  id: string;
  channelId: string;
  guildId: string | null;
  author: string;
  authorId: string;
  content: string;
  timestamp: string;
  isDM: boolean;
  isOwner: boolean;
}

const messageQueue: QueuedMessage[] = [];
const MAX_QUEUE = 100;

// --- Discord client ---
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.DirectMessages,
    GatewayIntentBits.MessageContent,
  ],
  partials: [Partials.Channel, Partials.Message],
});

client.on(Events.MessageCreate, (msg: Message) => {
  if (msg.author.bot) return;

  const queued: QueuedMessage = {
    id: msg.id,
    channelId: msg.channelId,
    guildId: msg.guildId,
    author: msg.author.displayName || msg.author.username,
    authorId: msg.author.id,
    content: msg.content,
    timestamp: msg.createdAt.toISOString(),
    isDM: !msg.guild,
    isOwner: OWNER_ID ? msg.author.id === OWNER_ID : false,
  };

  messageQueue.push(queued);
  if (messageQueue.length > MAX_QUEUE) messageQueue.shift();
});

client.once(Events.ClientReady, (c) => {
  console.error(`Discord connected as ${c.user.tag}`);
});

// --- MCP Server ---
const server = new McpServer({
  name: "atlas-discord",
  version: "1.0.0",
});

server.tool(
  "discord_poll",
  "Get new messages received since last poll. Returns and clears the queue.",
  {},
  async () => {
    const messages = [...messageQueue];
    messageQueue.length = 0;
    return {
      content: [
        {
          type: "text",
          text:
            messages.length === 0
              ? "No new messages."
              : JSON.stringify(messages, null, 2),
        },
      ],
    };
  }
);

server.tool(
  "discord_send",
  "Send a message to a Discord channel or DM.",
  {
    channel_id: z.string().describe("Channel or DM channel ID to send to"),
    content: z.string().describe("Message content (max 2000 chars)"),
    reply_to: z
      .string()
      .optional()
      .describe("Message ID to reply to (optional)"),
  },
  async ({ channel_id, content, reply_to }) => {
    const channel = await client.channels.fetch(channel_id);
    if (!channel || !("send" in channel)) {
      return {
        content: [{ type: "text", text: `Cannot send to channel ${channel_id}` }],
        isError: true,
      };
    }

    const options: { content: string; reply?: { messageReference: string } } = {
      content: content.slice(0, 2000),
    };

    const msg = reply_to
      ? await channel.send({
          content: content.slice(0, 2000),
          reply: { messageReference: reply_to },
        })
      : await channel.send(content.slice(0, 2000));

    return {
      content: [
        {
          type: "text",
          text: `Sent message ${msg.id} to ${channel_id}`,
        },
      ],
    };
  }
);

server.tool(
  "discord_dm",
  "Send a DM to a user by their Discord user ID.",
  {
    user_id: z.string().describe("Discord user ID"),
    content: z.string().describe("Message content (max 2000 chars)"),
  },
  async ({ user_id, content }) => {
    const user = await client.users.fetch(user_id);
    const dm = await user.createDM();
    const msg = await dm.send(content.slice(0, 2000));
    return {
      content: [
        { type: "text", text: `Sent DM ${msg.id} to ${user.tag}` },
      ],
    };
  }
);

server.tool(
  "discord_channels",
  "List all channels the bot can see across servers.",
  {},
  async () => {
    const channels: { id: string; name: string; guild: string; type: string }[] = [];

    for (const guild of client.guilds.cache.values()) {
      for (const channel of guild.channels.cache.values()) {
        if ("send" in channel) {
          channels.push({
            id: channel.id,
            name: channel.name,
            guild: guild.name,
            type: channel.type === 0 ? "text" : String(channel.type),
          });
        }
      }
    }

    return {
      content: [{ type: "text", text: JSON.stringify(channels, null, 2) }],
    };
  }
);

server.tool(
  "discord_set_owner",
  "Set the owner's Discord user ID for access control. Run once during setup.",
  {
    user_id: z.string().describe("Your Discord user ID"),
  },
  async ({ user_id }) => {
    process.env.DISCORD_OWNER_ID = user_id;
    return {
      content: [
        {
          type: "text",
          text: `Owner set to ${user_id}. Add DISCORD_OWNER_ID=${user_id} to your .env to persist.`,
        },
      ],
    };
  }
);

server.tool(
  "discord_status",
  "Check if the Discord bot is connected and show bot info.",
  {},
  async () => {
    const ready = client.isReady();
    return {
      content: [
        {
          type: "text",
          text: ready
            ? `Connected as ${client.user?.tag} | Guilds: ${client.guilds.cache.size} | Queue: ${messageQueue.length} messages`
            : "Bot is not connected.",
        },
      ],
    };
  }
);

// --- Start ---
async function main() {
  await client.login(DISCORD_TOKEN);
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
