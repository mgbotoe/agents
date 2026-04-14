@echo off
REM Start the Discord watcher — listens for messages and triggers Claude Code responses.
REM Usage: discord-watcher.cmd
REM Stop: Ctrl+C or close the window
echo Starting Atlas Discord watcher...
cd /d C:\Workspace\agents\chief-of-staff
bun run mcp/discord/src/watcher.ts
