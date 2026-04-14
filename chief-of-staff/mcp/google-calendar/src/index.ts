import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { google, type calendar_v3 } from "googleapis";
import { readFileSync, readdirSync, existsSync } from "fs";
import { join, dirname } from "path";
import { z } from "zod";

// --- Config ---
const BASE_DIR = join(dirname(import.meta.dir));
const TOKENS_DIR = join(BASE_DIR, "tokens");
const CREDS_PATH = join(BASE_DIR, "credentials.json");

// --- Account management ---
interface Account {
  label: string;
  calendar: calendar_v3.Calendar;
  email?: string;
}

function loadAccounts(): Account[] {
  if (!existsSync(CREDS_PATH)) {
    console.error("credentials.json not found");
    return [];
  }

  if (!existsSync(TOKENS_DIR)) {
    console.error("No tokens directory — run auth first");
    return [];
  }

  const creds = JSON.parse(readFileSync(CREDS_PATH, "utf-8"));
  const { client_id, client_secret } = creds.installed || creds.web;
  const accounts: Account[] = [];

  for (const file of readdirSync(TOKENS_DIR)) {
    if (!file.endsWith(".json")) continue;

    const label = file.replace(".json", "");
    const tokens = JSON.parse(readFileSync(join(TOKENS_DIR, file), "utf-8"));

    const auth = new google.auth.OAuth2(client_id, client_secret, "http://localhost:3333/callback");
    auth.setCredentials(tokens);

    // Auto-refresh tokens
    auth.on("tokens", (newTokens) => {
      const merged = { ...tokens, ...newTokens };
      const fs = require("fs");
      fs.writeFileSync(join(TOKENS_DIR, file), JSON.stringify(merged, null, 2));
    });

    const calendar = google.calendar({ version: "v3", auth });
    accounts.push({ label, calendar });
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

// --- Helpers ---
async function getAllCalendarIds(acc: Account): Promise<{ id: string; name: string }[]> {
  try {
    const res = await acc.calendar.calendarList.list();
    return (res.data.items || [])
      .filter((c) => c.id)
      .map((c) => ({ id: c.id!, name: c.summary || c.id! }));
  } catch {
    return [{ id: "primary", name: "primary" }];
  }
}

async function getEventsAllCalendars(
  acc: Account,
  timeMin: string,
  timeMax: string,
  maxResults = 50
): Promise<{ title: string; calendar: string; start?: string; end?: string; location?: string; meetLink?: string; status?: string; attendees?: string[] }[]> {
  const calendars = await getAllCalendarIds(acc);
  const events: { title: string; calendar: string; start?: string; end?: string; location?: string; meetLink?: string; status?: string; attendees?: string[] }[] = [];

  for (const cal of calendars) {
    try {
      const res = await acc.calendar.events.list({
        calendarId: cal.id,
        timeMin,
        timeMax,
        singleEvents: true,
        orderBy: "startTime",
        maxResults,
      });

      for (const e of res.data.items || []) {
        events.push({
          title: e.summary || "(no title)",
          calendar: cal.name,
          start: e.start?.dateTime || e.start?.date,
          end: e.end?.dateTime || e.end?.date,
          location: e.location,
          meetLink: e.hangoutLink,
          status: e.status,
          attendees: e.attendees?.map((a) => a.email || "").slice(0, 10),
        });
      }
    } catch { /* skip errored calendars */ }
  }

  // Sort by start time
  events.sort((a, b) => (a.start || "").localeCompare(b.start || ""));
  return events;
}

// --- MCP Server ---
const server = new McpServer({
  name: "atlas-google-calendar",
  version: "1.0.0",
});

server.tool(
  "gcal_accounts",
  "List all connected Google Calendar accounts.",
  {},
  async () => {
    accounts = loadAccounts();
    const info: { label: string; calendars: string[] }[] = [];

    for (const acc of accounts) {
      try {
        const res = await acc.calendar.calendarList.list();
        const cals = res.data.items?.map((c) => `${c.summary} (${c.id})`) || [];
        info.push({ label: acc.label, calendars: cals });
      } catch (err) {
        info.push({ label: acc.label, calendars: [`Error: ${err}`] });
      }
    }

    return {
      content: [{ type: "text", text: JSON.stringify(info, null, 2) }],
    };
  }
);

server.tool(
  "gcal_today",
  "Get today's events across all accounts or a specific one.",
  {
    account: z.string().optional().describe(`Account label (${accountLabels().join(", ")}). Omit for all.`),
  },
  async ({ account }) => {
    const now = new Date();
    const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate()).toISOString();
    const endOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1).toISOString();

    const targetAccounts = account ? [getAccount(account)].filter(Boolean) as Account[] : accounts;
    const allEvents: { account: string; events: object[] }[] = [];

    for (const acc of targetAccounts) {
      try {
        const events = await getEventsAllCalendars(acc, startOfDay, endOfDay);
        allEvents.push({ account: acc.label, events });
      } catch (err) {
        allEvents.push({ account: acc.label, events: [{ error: `${err}` }] });
      }
    }

    return {
      content: [{ type: "text", text: JSON.stringify(allEvents, null, 2) }],
    };
  }
);

server.tool(
  "gcal_upcoming",
  "Get upcoming events for the next N days.",
  {
    days: z.number().min(1).max(30).default(7).describe("Number of days to look ahead (max 30)"),
    account: z.string().optional().describe("Account label. Omit for all."),
  },
  async ({ days, account }) => {
    const now = new Date();
    const end = new Date(now.getTime() + days * 86400000);

    const targetAccounts = account ? [getAccount(account)].filter(Boolean) as Account[] : accounts;
    const allEvents: { account: string; events: object[] }[] = [];

    for (const acc of targetAccounts) {
      try {
        const events = await getEventsAllCalendars(acc, now.toISOString(), end.toISOString());
        allEvents.push({ account: acc.label, events });
      } catch (err) {
        allEvents.push({ account: acc.label, events: [{ error: `${err}` }] });
      }
    }

    return {
      content: [{ type: "text", text: JSON.stringify(allEvents, null, 2) }],
    };
  }
);

server.tool(
  "gcal_create_event",
  "Create a calendar event.",
  {
    account: z.string().describe("Account label to create event on"),
    title: z.string().describe("Event title"),
    start: z.string().describe("Start time (ISO 8601, e.g. 2026-04-15T10:00:00-07:00)"),
    end: z.string().describe("End time (ISO 8601)"),
    description: z.string().optional().describe("Event description"),
    location: z.string().optional().describe("Event location"),
    attendees: z.array(z.string()).optional().describe("List of attendee email addresses"),
    calendar_id: z.string().default("primary").describe("Calendar ID (default: primary)"),
  },
  async ({ account, title, start, end, description, location, attendees, calendar_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found. Available: ${accountLabels().join(", ")}` }], isError: true };
    }

    try {
      const event: calendar_v3.Schema$Event = {
        summary: title,
        start: { dateTime: start },
        end: { dateTime: end },
        description,
        location,
        attendees: attendees?.map((email) => ({ email })),
      };

      const res = await acc.calendar.events.insert({
        calendarId: calendar_id,
        requestBody: event,
        sendUpdates: attendees?.length ? "all" : "none",
      });

      return {
        content: [{ type: "text", text: `Event created: ${res.data.summary} (${res.data.htmlLink})` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed to create event: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gcal_delete_event",
  "Delete a calendar event by ID.",
  {
    account: z.string().describe("Account label"),
    event_id: z.string().describe("Event ID to delete"),
    calendar_id: z.string().default("primary").describe("Calendar ID (default: primary)"),
  },
  async ({ account, event_id, calendar_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.calendar.events.delete({ calendarId: calendar_id, eventId: event_id });
      return { content: [{ type: "text", text: `Event ${event_id} deleted.` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gcal_find_free_time",
  "Find free slots across accounts for a given day.",
  {
    date: z.string().describe("Date to check (YYYY-MM-DD)"),
    duration_minutes: z.number().min(15).max(480).default(60).describe("Desired slot duration in minutes"),
    start_hour: z.number().min(0).max(23).default(9).describe("Earliest hour (24h format)"),
    end_hour: z.number().min(1).max(24).default(17).describe("Latest hour (24h format)"),
  },
  async ({ date, duration_minutes, start_hour, end_hour }) => {
    const dayStart = new Date(`${date}T${String(start_hour).padStart(2, "0")}:00:00`);
    const dayEnd = new Date(`${date}T${String(end_hour).padStart(2, "0")}:00:00`);

    // Gather all events across all accounts
    const busy: { start: Date; end: Date }[] = [];

    for (const acc of accounts) {
      try {
        const events = await getEventsAllCalendars(acc, dayStart.toISOString(), dayEnd.toISOString());
        for (const e of events) {
          if (e.start && e.end && e.start.includes("T") && e.end.includes("T")) {
            busy.push({ start: new Date(e.start), end: new Date(e.end) });
          }
        }
      } catch { /* skip errored accounts */ }
    }

    // Sort by start time
    busy.sort((a, b) => a.start.getTime() - b.start.getTime());

    // Find gaps
    const slots: { start: string; end: string }[] = [];
    let cursor = dayStart.getTime();
    const durationMs = duration_minutes * 60000;

    for (const block of busy) {
      const gap = block.start.getTime() - cursor;
      if (gap >= durationMs) {
        slots.push({
          start: new Date(cursor).toISOString(),
          end: new Date(cursor + durationMs).toISOString(),
        });
      }
      cursor = Math.max(cursor, block.end.getTime());
    }

    // Check remaining time after last event
    if (dayEnd.getTime() - cursor >= durationMs) {
      slots.push({
        start: new Date(cursor).toISOString(),
        end: new Date(cursor + durationMs).toISOString(),
      });
    }

    return {
      content: [{
        type: "text",
        text: slots.length === 0
          ? `No ${duration_minutes}-minute free slots found on ${date} between ${start_hour}:00-${end_hour}:00.`
          : JSON.stringify({ date, duration_minutes, free_slots: slots }, null, 2),
      }],
    };
  }
);

// --- Event Management Tools ---

server.tool(
  "gcal_get_event",
  "Get a single calendar event by ID.",
  {
    account: z.string().describe("Account label"),
    event_id: z.string().describe("Event ID"),
    calendar_id: z.string().default("primary").describe("Calendar ID (default: primary)"),
  },
  async ({ account, event_id, calendar_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found. Available: ${accountLabels().join(", ")}` }], isError: true };
    }

    try {
      const res = await acc.calendar.events.get({ calendarId: calendar_id, eventId: event_id });
      return { content: [{ type: "text", text: JSON.stringify(res.data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed to get event: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gcal_update_event",
  "Update an existing calendar event. Only provided fields are modified.",
  {
    account: z.string().describe("Account label"),
    event_id: z.string().describe("Event ID to update"),
    calendar_id: z.string().default("primary").describe("Calendar ID (default: primary)"),
    title: z.string().optional().describe("New event title"),
    start: z.string().optional().describe("New start time (ISO 8601)"),
    end: z.string().optional().describe("New end time (ISO 8601)"),
    description: z.string().optional().describe("New event description"),
    location: z.string().optional().describe("New event location"),
    attendees: z.array(z.string()).optional().describe("New list of attendee email addresses"),
  },
  async ({ account, event_id, calendar_id, title, start, end, description, location, attendees }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found. Available: ${accountLabels().join(", ")}` }], isError: true };
    }

    try {
      const patch: calendar_v3.Schema$Event = {};
      if (title !== undefined) patch.summary = title;
      if (start !== undefined) patch.start = { dateTime: start };
      if (end !== undefined) patch.end = { dateTime: end };
      if (description !== undefined) patch.description = description;
      if (location !== undefined) patch.location = location;
      if (attendees !== undefined) patch.attendees = attendees.map((email) => ({ email }));

      const res = await acc.calendar.events.patch({
        calendarId: calendar_id,
        eventId: event_id,
        requestBody: patch,
        sendUpdates: attendees !== undefined ? "all" : "none",
      });

      return { content: [{ type: "text", text: `Event updated: ${res.data.summary} (${res.data.htmlLink})` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed to update event: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gcal_rsvp",
  "Update your RSVP status for a calendar event.",
  {
    account: z.string().describe("Account label"),
    event_id: z.string().describe("Event ID to RSVP to"),
    calendar_id: z.string().default("primary").describe("Calendar ID (default: primary)"),
    status: z.enum(["accepted", "declined", "tentative"]).describe("RSVP status"),
  },
  async ({ account, event_id, calendar_id, status }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found. Available: ${accountLabels().join(", ")}` }], isError: true };
    }

    try {
      // Get current event to find our email in attendees
      const current = await acc.calendar.events.get({ calendarId: calendar_id, eventId: event_id });
      const attendees = current.data.attendees || [];

      // Get account email from calendar settings
      const settings = await acc.calendar.calendars.get({ calendarId: "primary" });
      const myEmail = settings.data.id;

      if (!myEmail) {
        return { content: [{ type: "text", text: "Could not determine account email." }], isError: true };
      }

      const found = attendees.find((a) => a.email?.toLowerCase() === myEmail.toLowerCase());
      if (!found) {
        // Add self as attendee with the status if not in the list
        attendees.push({ email: myEmail, responseStatus: status });
      } else {
        found.responseStatus = status;
      }

      const res = await acc.calendar.events.patch({
        calendarId: calendar_id,
        eventId: event_id,
        requestBody: { attendees },
        sendUpdates: "all",
      });

      return { content: [{ type: "text", text: `RSVP "${status}" set for: ${res.data.summary}` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed to RSVP: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gcal_move_event",
  "Move an event from one calendar to another.",
  {
    account: z.string().describe("Account label"),
    event_id: z.string().describe("Event ID to move"),
    source_calendar_id: z.string().describe("Source calendar ID"),
    destination_calendar_id: z.string().describe("Destination calendar ID"),
  },
  async ({ account, event_id, source_calendar_id, destination_calendar_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found. Available: ${accountLabels().join(", ")}` }], isError: true };
    }

    try {
      const res = await acc.calendar.events.move({
        calendarId: source_calendar_id,
        eventId: event_id,
        destination: destination_calendar_id,
      });

      return { content: [{ type: "text", text: `Event moved: ${res.data.summary} → ${destination_calendar_id}` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed to move event: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gcal_manage_attendee",
  "Add or remove an attendee from a calendar event.",
  {
    account: z.string().describe("Account label"),
    event_id: z.string().describe("Event ID"),
    calendar_id: z.string().default("primary").describe("Calendar ID (default: primary)"),
    action: z.enum(["add", "remove"]).describe("Whether to add or remove the attendee"),
    email: z.string().describe("Attendee email address"),
  },
  async ({ account, event_id, calendar_id, action, email }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found. Available: ${accountLabels().join(", ")}` }], isError: true };
    }

    try {
      const current = await acc.calendar.events.get({ calendarId: calendar_id, eventId: event_id });
      let attendees = current.data.attendees || [];

      if (action === "add") {
        const exists = attendees.some((a) => a.email?.toLowerCase() === email.toLowerCase());
        if (exists) {
          return { content: [{ type: "text", text: `${email} is already an attendee.` }] };
        }
        attendees.push({ email });
      } else {
        const before = attendees.length;
        attendees = attendees.filter((a) => a.email?.toLowerCase() !== email.toLowerCase());
        if (attendees.length === before) {
          return { content: [{ type: "text", text: `${email} is not an attendee.` }] };
        }
      }

      const res = await acc.calendar.events.patch({
        calendarId: calendar_id,
        eventId: event_id,
        requestBody: { attendees },
        sendUpdates: "all",
      });

      const verb = action === "add" ? "added to" : "removed from";
      return { content: [{ type: "text", text: `${email} ${verb}: ${res.data.summary}` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed to ${action} attendee: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gcal_list_recurring",
  "List instances of a recurring event.",
  {
    account: z.string().describe("Account label"),
    event_id: z.string().describe("Recurring event ID"),
    calendar_id: z.string().default("primary").describe("Calendar ID (default: primary)"),
    time_min: z.string().optional().describe("Start of range (ISO 8601)"),
    time_max: z.string().optional().describe("End of range (ISO 8601)"),
  },
  async ({ account, event_id, calendar_id, time_min, time_max }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found. Available: ${accountLabels().join(", ")}` }], isError: true };
    }

    try {
      const params: {
        calendarId: string;
        eventId: string;
        timeMin?: string;
        timeMax?: string;
      } = {
        calendarId: calendar_id,
        eventId: event_id,
      };
      if (time_min) params.timeMin = time_min;
      if (time_max) params.timeMax = time_max;

      const res = await acc.calendar.events.instances(params);
      const instances = (res.data.items || []).map((e) => ({
        id: e.id,
        title: e.summary,
        start: e.start?.dateTime || e.start?.date,
        end: e.end?.dateTime || e.end?.date,
        status: e.status,
      }));

      return {
        content: [{
          type: "text",
          text: instances.length === 0
            ? "No instances found for this recurring event."
            : JSON.stringify(instances, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed to list instances: ${err}` }], isError: true };
    }
  }
);

// --- Start ---
async function main() {
  if (accounts.length === 0) {
    console.error("No accounts authenticated. Run: bun run src/auth.ts <label>");
  } else {
    console.error(`Loaded ${accounts.length} account(s): ${accountLabels().join(", ")}`);
  }

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
