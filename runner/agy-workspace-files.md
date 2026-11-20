---
name: workspace-files
description: Complete tasks using workspace files.
mainAgent: true
subagent: false
model: inherit
tools: [read_file, edit_file, write_file]
---
Use the available workspace tools to complete the user's request.

The caller collects deliverables from this session's workspace at WORKSPACE_PATH.
Use absolute paths under that directory when creating files. A file saved in
a gateway scratch directory is invisible to the caller.

<cwd>WORKSPACE_PATH</cwd>
