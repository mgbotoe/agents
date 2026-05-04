' Hidden launcher for Task Scheduler.
' Spawns run-task.cmd with no visible console window.
' Usage: wscript run-hidden.vbs <task-name>

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

args = ""
For i = 0 To WScript.Arguments.Count - 1
    args = args & " " & WScript.Arguments(i)
Next

WshShell.Run """" & scriptDir & "\run-task.cmd""" & args, 0, False
