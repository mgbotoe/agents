@echo off
REM Wrapper for Task Scheduler — calls the PowerShell script with the task name.
REM Usage: run-task.cmd promote
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0run-task.ps1" -Task %1
