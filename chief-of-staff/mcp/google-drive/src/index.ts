import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { google, type drive_v3, type sheets_v4, type slides_v1 } from "googleapis";
import { readFileSync, readdirSync, existsSync, writeFileSync, createReadStream } from "fs";
import { join, dirname, basename } from "path";
import { z } from "zod";
import { Readable } from "stream";

// --- Config ---
const BASE_DIR = join(dirname(import.meta.dir));
const TOKENS_DIR = join(BASE_DIR, "tokens");
const CREDS_PATH = join(BASE_DIR, "credentials.json");

// --- Account management ---
interface Account {
  label: string;
  drive: drive_v3.Drive;
  sheets: sheets_v4.Sheets;
  slides: slides_v1.Slides;
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

    const auth = new google.auth.OAuth2(client_id, client_secret, "http://localhost:3335/callback");
    auth.setCredentials(tokens);

    auth.on("tokens", (newTokens) => {
      const merged = { ...tokens, ...newTokens };
      writeFileSync(join(TOKENS_DIR, file), JSON.stringify(merged, null, 2));
    });

    const drive = google.drive({ version: "v3", auth });
    const sheets = google.sheets({ version: "v4", auth });
    const slides = google.slides({ version: "v1", auth });
    accounts.push({ label, drive, sheets, slides });
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

// --- Google Doc export MIME map ---
const EXPORT_MIME: Record<string, string> = {
  "application/vnd.google-apps.document": "text/plain",
  "application/vnd.google-apps.spreadsheet": "text/csv",
  "application/vnd.google-apps.presentation": "text/plain",
  "application/vnd.google-apps.drawing": "image/png",
};

// --- MCP Server ---
const server = new McpServer({
  name: "atlas-google-drive",
  version: "1.0.0",
});

// --- gdrive_accounts ---
server.tool(
  "gdrive_accounts",
  "List all connected Google Drive accounts.",
  {},
  async () => {
    accounts = loadAccounts();
    const info: { label: string; email: string }[] = [];

    for (const acc of accounts) {
      try {
        const about = await acc.drive.about.get({ fields: "user" });
        info.push({ label: acc.label, email: about.data.user?.emailAddress || "unknown" });
      } catch (err) {
        info.push({ label: acc.label, email: `Error: ${err}` });
      }
    }

    return { content: [{ type: "text", text: JSON.stringify(info, null, 2) }] };
  }
);

// --- gdrive_search ---
server.tool(
  "gdrive_search",
  "Search for files and folders in Google Drive. Uses Google Drive query syntax (e.g. \"name contains 'report'\", \"mimeType='application/pdf'\").",
  {
    query: z.string().describe("Google Drive query syntax (e.g. \"name contains 'report'\", \"mimeType='application/pdf'\", \"fullText contains 'budget'\")"),
    account: z.string().optional().describe("Account label. Omit for default."),
    max_results: z.number().min(1).max(100).default(10).describe("Max results to return"),
  },
  async ({ query, account, max_results }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found. Available: ${accountLabels().join(", ")}` }], isError: true };
    }

    try {
      const res = await acc.drive.files.list({
        q: query,
        pageSize: max_results,
        fields: "files(id,name,mimeType,modifiedTime,size,webViewLink)",
        orderBy: "modifiedTime desc",
      });

      const files = (res.data.files || []).map((f) => ({
        id: f.id,
        name: f.name,
        mimeType: f.mimeType,
        modifiedTime: f.modifiedTime,
        size: f.size,
        webViewLink: f.webViewLink,
      }));

      return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_get_file ---
server.tool(
  "gdrive_get_file",
  "Get file metadata and optionally read its content. For Google Docs/Sheets/Slides, exports as plain text. For other text files, downloads content.",
  {
    account: z.string().describe("Account label"),
    file_id: z.string().describe("File ID from search results"),
    read_content: z.boolean().default(false).describe("If true, also read/export file content"),
  },
  async ({ account, file_id, read_content }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const meta = await acc.drive.files.get({
        fileId: file_id,
        fields: "id,name,mimeType,modifiedTime,size,webViewLink,parents,createdTime,owners,shared",
      });

      const result: Record<string, unknown> = { ...meta.data };

      if (read_content) {
        const mimeType = meta.data.mimeType || "";
        const exportMime = EXPORT_MIME[mimeType];

        if (exportMime) {
          // Google Workspace file — export it
          const exported = await acc.drive.files.export(
            { fileId: file_id, mimeType: exportMime },
            { responseType: "text" }
          );
          const content = typeof exported.data === "string" ? exported.data : JSON.stringify(exported.data);
          result.content = content.slice(0, 10000);
        } else {
          // Regular file — download it
          const downloaded = await acc.drive.files.get(
            { fileId: file_id, alt: "media" },
            { responseType: "text" }
          );
          const content = typeof downloaded.data === "string" ? downloaded.data : JSON.stringify(downloaded.data);
          result.content = content.slice(0, 10000);
        }
      }

      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_list_contents ---
server.tool(
  "gdrive_list_contents",
  "List all files and subfolders in a Google Drive folder.",
  {
    account: z.string().describe("Account label"),
    folder_id: z.string().default("root").describe("Folder ID (default: root)"),
    max_results: z.number().min(1).max(100).default(20).describe("Max results to return"),
  },
  async ({ account, folder_id, max_results }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.drive.files.list({
        q: `'${folder_id}' in parents and trashed = false`,
        pageSize: max_results,
        fields: "files(id,name,mimeType,modifiedTime)",
        orderBy: "folder,name",
      });

      const files = (res.data.files || []).map((f) => ({
        id: f.id,
        name: f.name,
        mimeType: f.mimeType,
        modifiedTime: f.modifiedTime,
      }));

      return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_create_folder ---
server.tool(
  "gdrive_create_folder",
  "Create a new folder in Google Drive.",
  {
    account: z.string().describe("Account label"),
    name: z.string().describe("Folder name"),
    parent_id: z.string().optional().describe("Parent folder ID (default: root)"),
  },
  async ({ account, name, parent_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.drive.files.create({
        requestBody: {
          name,
          mimeType: "application/vnd.google-apps.folder",
          parents: parent_id ? [parent_id] : undefined,
        },
        fields: "id,name,webViewLink",
      });

      return { content: [{ type: "text", text: JSON.stringify(res.data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_create_file ---
server.tool(
  "gdrive_create_file",
  "Create a plain text file in Google Drive.",
  {
    account: z.string().describe("Account label"),
    name: z.string().describe("File name"),
    content: z.string().describe("File content"),
    parent_id: z.string().optional().describe("Parent folder ID (default: root)"),
    mime_type: z.string().default("text/plain").describe("MIME type (default: text/plain)"),
  },
  async ({ account, name, content, parent_id, mime_type }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.drive.files.create({
        requestBody: {
          name,
          mimeType: mime_type,
          parents: parent_id ? [parent_id] : undefined,
        },
        media: {
          mimeType: mime_type,
          body: Readable.from([content]),
        },
        fields: "id,name,webViewLink",
      });

      return { content: [{ type: "text", text: JSON.stringify(res.data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_copy_file ---
server.tool(
  "gdrive_copy_file",
  "Copy a file in Google Drive.",
  {
    account: z.string().describe("Account label"),
    file_id: z.string().describe("File ID to copy"),
    new_name: z.string().optional().describe("Name for the copy"),
    parent_id: z.string().optional().describe("Destination folder ID"),
  },
  async ({ account, file_id, new_name, parent_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const requestBody: drive_v3.Schema$File = {};
      if (new_name) requestBody.name = new_name;
      if (parent_id) requestBody.parents = [parent_id];

      const res = await acc.drive.files.copy({
        fileId: file_id,
        requestBody,
        fields: "id,name,webViewLink",
      });

      return { content: [{ type: "text", text: JSON.stringify(res.data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_move_file ---
server.tool(
  "gdrive_move_file",
  "Move a file to a different folder in Google Drive.",
  {
    account: z.string().describe("Account label"),
    file_id: z.string().describe("File ID to move"),
    new_parent_id: z.string().describe("Destination folder ID"),
  },
  async ({ account, file_id, new_parent_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      // Get current parents
      const current = await acc.drive.files.get({
        fileId: file_id,
        fields: "parents",
      });
      const previousParents = (current.data.parents || []).join(",");

      const res = await acc.drive.files.update({
        fileId: file_id,
        addParents: new_parent_id,
        removeParents: previousParents,
        fields: "id,name,parents,webViewLink",
      });

      return { content: [{ type: "text", text: JSON.stringify(res.data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_rename ---
server.tool(
  "gdrive_rename",
  "Rename a file or folder in Google Drive.",
  {
    account: z.string().describe("Account label"),
    file_id: z.string().describe("File or folder ID"),
    new_name: z.string().describe("New name"),
  },
  async ({ account, file_id, new_name }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.drive.files.update({
        fileId: file_id,
        requestBody: { name: new_name },
        fields: "id,name,webViewLink",
      });

      return { content: [{ type: "text", text: JSON.stringify(res.data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_delete ---
server.tool(
  "gdrive_delete",
  "Delete a file or folder in Google Drive. For folders, set recursive=true to delete contents.",
  {
    account: z.string().describe("Account label"),
    file_id: z.string().describe("File or folder ID to delete"),
    recursive: z.boolean().default(false).describe("For folders: delete all contents recursively"),
  },
  async ({ account, file_id, recursive }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      // Check if it's a folder with contents
      const meta = await acc.drive.files.get({ fileId: file_id, fields: "name,mimeType" });
      const isFolder = meta.data.mimeType === "application/vnd.google-apps.folder";

      if (isFolder && !recursive) {
        // Check if folder has children
        const children = await acc.drive.files.list({
          q: `'${file_id}' in parents and trashed = false`,
          pageSize: 1,
          fields: "files(id)",
        });

        if ((children.data.files || []).length > 0) {
          return {
            content: [{ type: "text", text: `Folder "${meta.data.name}" is not empty. Set recursive=true to delete it and all contents.` }],
            isError: true,
          };
        }
      }

      await acc.drive.files.delete({ fileId: file_id });

      return { content: [{ type: "text", text: `Deleted "${meta.data.name}" (${file_id})` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_share ---
server.tool(
  "gdrive_share",
  "Share a file or folder with someone via email.",
  {
    account: z.string().describe("Account label"),
    file_id: z.string().describe("File or folder ID to share"),
    email: z.string().describe("Email address to share with"),
    role: z.enum(["reader", "writer", "commenter"]).describe("Permission role"),
  },
  async ({ account, file_id, email, role }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      await acc.drive.permissions.create({
        fileId: file_id,
        requestBody: {
          type: "user",
          role: role === "commenter" ? "reader" : role,
          emailAddress: email,
          ...(role === "commenter" ? { additionalRoles: ["commenter"] } : {}),
        } as drive_v3.Schema$Permission,
        sendNotificationEmail: true,
      });

      // Get the sharing link
      const file = await acc.drive.files.get({ fileId: file_id, fields: "webViewLink" });

      return {
        content: [{ type: "text", text: JSON.stringify({ shared_with: email, role, link: file.data.webViewLink }, null, 2) }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_upload ---
server.tool(
  "gdrive_upload",
  "Upload a local file to Google Drive.",
  {
    account: z.string().describe("Account label"),
    local_path: z.string().describe("Absolute path to the local file"),
    parent_id: z.string().optional().describe("Destination folder ID (default: root)"),
    name: z.string().optional().describe("Override file name (default: use local filename)"),
  },
  async ({ account, local_path, parent_id, name: overrideName }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    if (!existsSync(local_path)) {
      return { content: [{ type: "text", text: `Local file not found: ${local_path}` }], isError: true };
    }

    try {
      const fileName = overrideName || basename(local_path);
      const ext = local_path.split(".").pop()?.toLowerCase() || "";
      const MIME_MAP: Record<string, string> = {
        pdf: "application/pdf",
        pptx: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ppt: "application/vnd.ms-powerpoint",
        xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        xls: "application/vnd.ms-excel",
        docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        doc: "application/msword",
        csv: "text/csv",
        txt: "text/plain",
        png: "image/png",
        jpg: "image/jpeg",
        jpeg: "image/jpeg",
        gif: "image/gif",
        svg: "image/svg+xml",
        mp4: "video/mp4",
        json: "application/json",
        html: "text/html",
        zip: "application/zip",
      };
      const detectedMime = MIME_MAP[ext] || "application/octet-stream";

      const res = await acc.drive.files.create({
        requestBody: {
          name: fileName,
          mimeType: detectedMime,
          parents: parent_id ? [parent_id] : undefined,
        },
        media: {
          mimeType: detectedMime,
          body: createReadStream(local_path),
        },
        fields: "id,name,webViewLink,size",
      });

      return { content: [{ type: "text", text: JSON.stringify(res.data, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- gdrive_download ---
server.tool(
  "gdrive_download",
  "Download a file from Google Drive to a local path.",
  {
    account: z.string().describe("Account label"),
    file_id: z.string().describe("File ID to download"),
    local_path: z.string().describe("Absolute local path to save the file"),
  },
  async ({ account, file_id, local_path }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const meta = await acc.drive.files.get({ fileId: file_id, fields: "name,mimeType" });
      const mimeType = meta.data.mimeType || "";
      const exportMime = EXPORT_MIME[mimeType];

      let data: Buffer;

      if (exportMime) {
        // Google Workspace file — export it
        const res = await acc.drive.files.export(
          { fileId: file_id, mimeType: exportMime },
          { responseType: "arraybuffer" }
        );
        data = Buffer.from(res.data as ArrayBuffer);
      } else {
        // Regular file — download it
        const res = await acc.drive.files.get(
          { fileId: file_id, alt: "media" },
          { responseType: "arraybuffer" }
        );
        data = Buffer.from(res.data as ArrayBuffer);
      }

      writeFileSync(local_path, data);

      return {
        content: [{ type: "text", text: `Downloaded "${meta.data.name}" to ${local_path} (${data.length} bytes)` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

// --- Google Sheets tools ---

server.tool(
  "gdrive_create_sheet",
  "Create a new native Google Spreadsheet in Google Drive. Returns the spreadsheet ID and URL.",
  {
    account: z.string().describe("Account label"),
    title: z.string().describe("Spreadsheet title"),
    parent_id: z.string().optional().describe("Parent folder ID (default: root)"),
    sheet_names: z.array(z.string()).optional().describe("Sheet/tab names to create (default: ['Sheet1'])"),
  },
  async ({ account, title, parent_id, sheet_names }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found. Available: ${accountLabels().join(", ")}` }], isError: true };
    }

    try {
      const sheets = sheet_names || ["Sheet1"];
      const res = await acc.sheets.spreadsheets.create({
        requestBody: {
          properties: { title },
          sheets: sheets.map((name) => ({ properties: { title: name } })),
        },
      });

      const fileId = res.data.spreadsheetId!;

      // Move to parent folder if specified
      if (parent_id) {
        await acc.drive.files.update({
          fileId,
          addParents: parent_id,
          removeParents: "root",
          fields: "id,parents",
        });
      }

      return {
        content: [{ type: "text", text: JSON.stringify({
          id: fileId,
          url: res.data.spreadsheetUrl,
          title: res.data.properties?.title,
          sheets: res.data.sheets?.map((s) => s.properties?.title),
        }, null, 2) }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gdrive_sheet_write",
  "Write data to a Google Spreadsheet. Provide rows as a 2D array of values.",
  {
    account: z.string().describe("Account label"),
    spreadsheet_id: z.string().describe("Spreadsheet ID"),
    range: z.string().describe("A1 notation range (e.g., 'Sheet1!A1:D10' or 'Sheet1!A1')"),
    values: z.array(z.array(z.union([z.string(), z.number(), z.boolean(), z.null()]))).describe("2D array of values (rows x columns)"),
  },
  async ({ account, spreadsheet_id, range, values }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.sheets.spreadsheets.values.update({
        spreadsheetId: spreadsheet_id,
        range,
        valueInputOption: "USER_ENTERED",
        requestBody: { values },
      });

      return {
        content: [{ type: "text", text: `Updated ${res.data.updatedCells} cells in ${res.data.updatedRange}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gdrive_sheet_append",
  "Append rows to the end of a Google Spreadsheet.",
  {
    account: z.string().describe("Account label"),
    spreadsheet_id: z.string().describe("Spreadsheet ID"),
    range: z.string().describe("Sheet name or range to append to (e.g., 'Sheet1')"),
    values: z.array(z.array(z.union([z.string(), z.number(), z.boolean(), z.null()]))).describe("2D array of rows to append"),
  },
  async ({ account, spreadsheet_id, range, values }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.sheets.spreadsheets.values.append({
        spreadsheetId: spreadsheet_id,
        range,
        valueInputOption: "USER_ENTERED",
        insertDataOption: "INSERT_ROWS",
        requestBody: { values },
      });

      return {
        content: [{ type: "text", text: `Appended ${values.length} rows to ${res.data.updates?.updatedRange}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gdrive_sheet_read",
  "Read data from a Google Spreadsheet range.",
  {
    account: z.string().describe("Account label"),
    spreadsheet_id: z.string().describe("Spreadsheet ID"),
    range: z.string().describe("A1 notation range (e.g., 'Sheet1!A1:D10')"),
  },
  async ({ account, spreadsheet_id, range }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.sheets.spreadsheets.values.get({
        spreadsheetId: spreadsheet_id,
        range,
      });

      return {
        content: [{ type: "text", text: JSON.stringify({
          range: res.data.range,
          rows: res.data.values?.length || 0,
          values: res.data.values,
        }, null, 2) }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gdrive_create_slides",
  "Create a new native Google Slides presentation in Google Drive.",
  {
    account: z.string().describe("Account label"),
    title: z.string().describe("Presentation title"),
    parent_id: z.string().optional().describe("Parent folder ID (default: root)"),
  },
  async ({ account, title, parent_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.drive.files.create({
        requestBody: {
          name: title,
          mimeType: "application/vnd.google-apps.presentation",
          parents: parent_id ? [parent_id] : undefined,
        },
        fields: "id,name,webViewLink",
      });

      return {
        content: [{ type: "text", text: JSON.stringify(res.data, null, 2) }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gdrive_slides_get",
  "Get the structure of a Google Slides presentation — slide IDs, titles, and element details.",
  {
    account: z.string().describe("Account label"),
    presentation_id: z.string().describe("Presentation ID"),
  },
  async ({ account, presentation_id }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.slides.presentations.get({ presentationId: presentation_id });
      const summary = res.data.slides?.map((slide, i) => ({
        index: i,
        objectId: slide.objectId,
        elements: slide.pageElements?.length || 0,
      }));
      return {
        content: [{ type: "text", text: JSON.stringify({
          title: res.data.title,
          slideCount: res.data.slides?.length || 0,
          slides: summary,
        }, null, 2) }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gdrive_slides_add_slide",
  "Add a new blank slide to a Google Slides presentation.",
  {
    account: z.string().describe("Account label"),
    presentation_id: z.string().describe("Presentation ID"),
    layout: z.enum(["BLANK", "TITLE", "TITLE_AND_BODY", "TITLE_AND_TWO_COLUMNS", "TITLE_ONLY", "SECTION_HEADER"]).default("BLANK").describe("Slide layout"),
    insert_at: z.number().optional().describe("Index to insert at (0-based). Omit to append at end."),
  },
  async ({ account, presentation_id, layout, insert_at }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const layoutMap: Record<string, string> = {
        BLANK: "BLANK",
        TITLE: "TITLE",
        TITLE_AND_BODY: "TITLE_AND_BODY",
        TITLE_AND_TWO_COLUMNS: "TITLE_AND_TWO_COLUMNS",
        TITLE_ONLY: "TITLE_ONLY",
        SECTION_HEADER: "SECTION_HEADER",
      };

      const request: any = {
        createSlide: {
          slideLayoutReference: { predefinedLayout: layoutMap[layout] || "BLANK" },
        },
      };
      if (insert_at !== undefined) {
        request.createSlide.insertionIndex = insert_at;
      }

      const res = await acc.slides.presentations.batchUpdate({
        presentationId: presentation_id,
        requestBody: { requests: [request] },
      });

      const slideId = res.data.replies?.[0]?.createSlide?.objectId;
      return {
        content: [{ type: "text", text: `Created slide: ${slideId} (layout: ${layout})` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gdrive_slides_add_text",
  "Add a text box to a specific slide in a Google Slides presentation.",
  {
    account: z.string().describe("Account label"),
    presentation_id: z.string().describe("Presentation ID"),
    slide_id: z.string().describe("Slide object ID (from gdrive_slides_get)"),
    text: z.string().describe("Text content to add"),
    x: z.number().default(100).describe("X position in points from left"),
    y: z.number().default(100).describe("Y position in points from top"),
    width: z.number().default(400).describe("Width in points"),
    height: z.number().default(50).describe("Height in points"),
    font_size: z.number().default(14).describe("Font size in points"),
    bold: z.boolean().default(false).describe("Bold text"),
    color: z.string().default("000000").describe("Text color hex (e.g., '000000' for black)"),
  },
  async ({ account, presentation_id, slide_id, text, x, y, width, height, font_size, bold, color }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const elementId = `textbox_${Date.now()}`;
      const r = parseInt(color.substring(0, 2), 16) / 255;
      const g = parseInt(color.substring(2, 4), 16) / 255;
      const b = parseInt(color.substring(4, 6), 16) / 255;

      const requests = [
        {
          createShape: {
            objectId: elementId,
            shapeType: "TEXT_BOX",
            elementProperties: {
              pageObjectId: slide_id,
              size: {
                width: { magnitude: width, unit: "PT" },
                height: { magnitude: height, unit: "PT" },
              },
              transform: {
                scaleX: 1, scaleY: 1,
                translateX: x, translateY: y,
                unit: "PT",
              },
            },
          },
        },
        {
          insertText: {
            objectId: elementId,
            text,
            insertionIndex: 0,
          },
        },
        {
          updateTextStyle: {
            objectId: elementId,
            style: {
              fontSize: { magnitude: font_size, unit: "PT" },
              bold,
              foregroundColor: {
                opaqueColor: { rgbColor: { red: r, green: g, blue: b } },
              },
            },
            textRange: { type: "ALL" },
            fields: "fontSize,bold,foregroundColor",
          },
        },
      ];

      await acc.slides.presentations.batchUpdate({
        presentationId: presentation_id,
        requestBody: { requests },
      });

      return {
        content: [{ type: "text", text: `Added text box "${elementId}" to slide ${slide_id}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gdrive_slides_add_shape",
  "Add a shape (rectangle, oval, etc.) to a slide with optional fill color.",
  {
    account: z.string().describe("Account label"),
    presentation_id: z.string().describe("Presentation ID"),
    slide_id: z.string().describe("Slide object ID"),
    shape_type: z.enum(["RECTANGLE", "ROUND_RECTANGLE", "ELLIPSE", "TEXT_BOX"]).default("RECTANGLE").describe("Shape type"),
    x: z.number().default(100).describe("X position in points"),
    y: z.number().default(100).describe("Y position in points"),
    width: z.number().default(200).describe("Width in points"),
    height: z.number().default(100).describe("Height in points"),
    fill_color: z.string().optional().describe("Fill color hex (e.g., '028090'). Omit for no fill."),
  },
  async ({ account, presentation_id, slide_id, shape_type, x, y, width, height, fill_color }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const elementId = `shape_${Date.now()}`;
      const requests: any[] = [
        {
          createShape: {
            objectId: elementId,
            shapeType: shape_type,
            elementProperties: {
              pageObjectId: slide_id,
              size: {
                width: { magnitude: width, unit: "PT" },
                height: { magnitude: height, unit: "PT" },
              },
              transform: {
                scaleX: 1, scaleY: 1,
                translateX: x, translateY: y,
                unit: "PT",
              },
            },
          },
        },
      ];

      if (fill_color) {
        const r = parseInt(fill_color.substring(0, 2), 16) / 255;
        const g = parseInt(fill_color.substring(2, 4), 16) / 255;
        const b = parseInt(fill_color.substring(4, 6), 16) / 255;
        requests.push({
          updateShapeProperties: {
            objectId: elementId,
            shapeProperties: {
              shapeBackgroundFill: {
                solidFill: {
                  color: { rgbColor: { red: r, green: g, blue: b } },
                },
              },
            },
            fields: "shapeBackgroundFill.solidFill.color",
          },
        });
      }

      await acc.slides.presentations.batchUpdate({
        presentationId: presentation_id,
        requestBody: { requests },
      });

      return {
        content: [{ type: "text", text: `Added ${shape_type} "${elementId}" to slide ${slide_id}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed: ${err}` }], isError: true };
    }
  }
);

server.tool(
  "gdrive_slides_batch_update",
  "Execute raw batch update requests on a Google Slides presentation. For advanced operations.",
  {
    account: z.string().describe("Account label"),
    presentation_id: z.string().describe("Presentation ID"),
    requests: z.array(z.record(z.any())).describe("Array of Slides API request objects"),
  },
  async ({ account, presentation_id, requests }) => {
    const acc = getAccount(account);
    if (!acc) {
      return { content: [{ type: "text", text: `Account "${account}" not found.` }], isError: true };
    }

    try {
      const res = await acc.slides.presentations.batchUpdate({
        presentationId: presentation_id,
        requestBody: { requests },
      });

      return {
        content: [{ type: "text", text: `Executed ${requests.length} requests. Replies: ${JSON.stringify(res.data.replies, null, 2)}` }],
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
    console.error(`Loaded ${accounts.length} Google Drive account(s): ${accountLabels().join(", ")}`);
  }

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
