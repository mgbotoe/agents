import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "polaris-slack",
  version: "1.0.0",
});

server.tool(
  "slack_ping",
  "Test tool — returns pong.",
  {},
  async () => ({
    content: [{ type: "text", text: "pong" }],
  })
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
