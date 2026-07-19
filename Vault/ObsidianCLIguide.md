



## How Your Architect Benefits from the Obsidian Vault
Moving from grep to an Obsidian-based vault transforms how your Architect Agent (Claude) understands the codebase. Instead of treating code as flat text, the Architect can now leverage graph relationships, metadata, and structural boundaries.

┌────────────────────────────────────────────────────────┐
│               ARCHITECT AGENT (Claude)                 │
│  • Maps out tasks via Dataview queries                 │
│  • Reads cross-lab dependencies (_vocabulary)          │
│  • Monitors task pipelines via /tasks/progress_notes   │
└───────────────────────────┬────────────────────────────┘
                            │ (Outputs precise context & rules)
                            ▼
┌────────────────────────────────────────────────────────┐
│               CODING AGENTS (Subagents)                │
│  • Codex  • Claude  • Antigravity                      │
│  • Get narrow, accurate code scopes                    │
│  • Do not hallucinate cross-lab dependencies           │
└────────────────────────────────────────────────────────┘

## 1. Graph-Aware Impact Analysis
Because the codebase was "graphified" before entry, the Architect can see exactly how a change in dtclab/code/schemas/ will ripple into gaslab/code/rule_engine/. Instead of grepping for a string and guessing dependencies, Claude can read your System-Map.md and _bases/ query files to find connected nodes instantly. [1] 
## 2. Cross-Lab Vocabulary Alignment
With a unified _vocabulary/ folder (DTC_VOCABULARY.md, etc.), the Architect acts as a semantic bridge. When designing a task, it checks these vocabulary files to ensure the coding subagents use consistent naming conventions and domain logic across all three labs (dtclab, gaslab, obdlab).
## 3. Living Pipeline Tracking
The /tasks/ directory acts as a live state machine. The Architect can scan *_START_HERE.md and /progress_notes/ to immediately see what is built, what is blocked, and what code schemas are ready for the next subagent task assignment.
------------------------------

------------------------------
## Option 1: The Official Obsidian CLI (Native & Token Efficient)
Obsidian includes a powerful native [Obsidian CLI](https://obsidian.md/cli) featuring over 80 built-in commands. Because your Claude desktop app has local command execution capabilities, it can run shell commands natively instead of maintaining a persistent MCP server wrapper. [2, 6, 8, 9] 
## 1. Enable it in Obsidian [10] 
Go to Obsidian Settings → CLI → Enable CLI. (Note: This requires Obsidian version 1.12+ and a Catalyst license). [6] 
## 2. How the Agent Queries via Bash
Instead of using basic grep, Claude can invoke native structural and semantic queries directly from the terminal, returning clean, structural data: [11] 

# Get all backlinks pointing to a core module schema
obsidian query backlinks "labs/dtclab/code/schemas/ranking.py"
# Get a structured JSON summary of all tasks marked with specific tags
obsidian query tags --json
# Find all dead-ends or unlinked project documentation notes in a lab
obsidian query deadends "labs/obdlab/wiki"

------------------------------
## Option 2: The Dataview CLI Scripting Strategy
If your Architect needs to run complex database style logic (like the .base queries in your _bases/ folder), you can give the agent a standard Python or Node.js shell script.
Because your codebase is already local, the script reads your frontmatter markdown text instantly and treats the folder as a database. [4] 
You can instruct your Architect to execute a simple script that mimics Dataview logic without requiring the Obsidian application to be open: [12] 
## 1. The Python Script Strategy (vault_query.py)
Place a small utility script in your vault root that searches frontmatter properties.

import osimport sysimport yaml
def query_vault(target_folder, key, value):
    results = []
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.startswith('---'):
                        try:
                            # Parse markdown frontmatter
                            _, frontmatter, _ = content.split('---', 2)
                            meta = yaml.safe_load(frontmatter)
                            if meta and meta.get(key) == value:
                                results.append({"file": file, "path": path, "meta": meta})
                        except Exception:
                            pass
    return results
if __name__ == "__main__":
    # Example usage: python vault_query.py labs/dtclab status "review"
    print(query_vault(sys.argv[1], sys.argv[2], sys.argv[3]))

## 2. How the Agent Uses It
When the Architect wants to check dependencies or look for task progress notes, it simply fires a quick shell command via its terminal interface: [2] 

python vault_query.py tasks status "blocked"


* Composability with Unix Tools: Since the agent outputs shell commands, it can seamlessly pipe the output of your vault queries directly into your subagent pipelines using standard utilities like jq or file redirects. [4, 16] 

# Architect filters tasks and pipes the exact paths to a subagent script
obsidian query tasks --json | jq '.[] | select(.status=="ready")' > pending_tasks.json

If you prefer using the native route, run obsidian help inside your desktop app's terminal to verify that Claude can access the executable. Let me know if you would like me to draft a custom Bash pipeline script that automatically matches your .base format templates directly via the command line! [6] 




------------------------------
## The Massive Benefit for Your Coding Subagents
While the Architect uses the vault to design the tasks, your Coding Agents (Codex, Claude, Antigravity) benefit significantly when you pass those tasks down to them. [14, 15, 16, 17] 

* Zero Hallucination Scopes: When you assign a task (e.g., T-GAS-*), the Architect will have already queried the vault to append the exact markdown notes, relevant _vocabulary/ definitions, and precise file paths needed. The coding agent doesn't need to guess the architecture; it receives a "context sandbox." [18] 
* Strict Interface Boundaries: Because the coding subagents work inside isolated labs (gaslab, obdlab), they often lack the "big picture." The Architect uses the vault's graph views to write strict input/output rules for the subagents, preventing them from breaking code in another lab. [19, 20] 
* Automated Context Injection: Instead of passing an entire massive codebase to Codex (which wastes token context and causes confusion), you pass a lean package: the code file to modify, the matching test fixture from /tests/, and the specific architectural note from /wiki/ provided by the Architect's vault query.






The official Obsidian CLI (released in v1.12, February 2026) lets you control every aspect of Obsidian from the terminal. It communicates with a running Obsidian desktop instance via IPC.Obsidian CLI

Read references/command-reference.md when you need specific flags, output formats, or subcommands for any command group. It covers all 130+ commands with full parameter tables and has a table of contents at the top.

Prerequisites
Requirement	Details
Obsidian Desktop	v1.12.0+
CLI enabled	Settings → Command line interface → Toggle ON
Obsidian running	The desktop app must be running for CLI to work (IPC)
Platform Notes
macOS / Linux: The obsidian binary is registered in PATH automatically when you enable CLI in settings.
Windows: Requires an Obsidian.com redirector file placed alongside Obsidian.exe. Must run with normal user privileges — admin terminals produce silent failures.
If colon subcommands (property:set, daily:append, etc.) with parameters return exit 127, check that Obsidian.com exists alongside Obsidian.exe. If missing, you have an outdated installer — download the latest from obsidian.md/download and reinstall.
Git Bash / MSYS2 users: Bash resolves obsidian to Obsidian.exe (GUI) instead of Obsidian.com (CLI), causing colon+params to fail with exit 127 even when Obsidian.com is present. Create a wrapper script — see Troubleshooting.
Headless Linux: Use the .deb package (not snap). Run under xvfb. Prefix commands with DISPLAY=:5 (or your xvfb display number). Ensure PrivateTmp=false if running as a service.
Syntax
All parameters use key=value syntax. Quote values containing spaces.

obsidian <command> [subcommand] [key=value ...] [flags]
Multi-Vault
Target a specific vault by making it the first argument:

obsidian "My Vault" daily:read
obsidian "Work Notes" search query="meeting"
If omitted, the CLI targets the most recently active vault.

Command Overview
The CLI provides 130+ commands across these groups:

Group	Key Commands	Purpose
files	read, create, append, prepend, move, rename, delete, files, folders, file, random	Note CRUD and file discovery
daily	daily, daily:read, daily:append, daily:prepend, daily:path	Daily note operations
search	search, search:context	Full-text search; search:context returns matching lines
properties	properties, property:read, property:set, property:remove, aliases	Frontmatter/metadata management
tags	tags, tag	Tag listing, counts, and filtering
tasks	tasks, task	Task querying, filtering, and toggling
links	backlinks, links, unresolved, orphans, deadends	Graph and link analysis
bookmarks	bookmarks, bookmark	List and add bookmarks
templates	templates, template:read, template:insert	Template listing, rendering, insertion
plugins	plugins, plugin, plugin:enable, plugin:disable, plugin:install, plugin:uninstall, plugins:restrict	Plugin management
sync	sync, sync:status, sync:history, sync:read, sync:restore, sync:deleted	Obsidian Sync operations
themes	themes, theme, theme:set, theme:install, theme:uninstall	Theme management
snippets	snippets, snippets:enabled, snippet:enable, snippet:disable	CSS snippet management
commands	commands, command, hotkeys, hotkey	Execute Obsidian commands by ID; inspect hotkeys
bases	bases, base:query, base:views, base:create	Obsidian Bases (v1.12+ database feature)
history	history, history:list, history:read, history:restore	File version recovery (File Recovery plugin)
workspace	workspace, tabs, tab:open	Workspace layout and tab management
diff	diff	Compare local vs sync file versions
dev	eval, dev:screenshot, dev:debug, dev:console, dev:errors, dev:css, dev:dom, devtools	Developer/debugging tools
vault	vault, vaults, version, reload, restart	Vault info and app control
other	outline, wordcount, recents	Utility commands
Quick Reference — Most Common Commands
Reading & Writing Notes
obsidian read path="folder/note.md"
obsidian create path="folder/note" content="# New Note"
obsidian create path="folder/note" template="meeting-notes"
obsidian append path="folder/note.md" content="New paragraph"
obsidian prepend path="folder/note.md" content="Top content"
obsidian move path="old/note.md" to="new/note.md"
obsidian delete path="folder/note.md"
obsidian delete path="folder/note.md" permanent
Daily Notes
obsidian daily                          # Open today's daily note
obsidian daily:read                     # Print content of today's note
obsidian daily:append content="- [ ] New task"
obsidian daily:prepend content="## Morning Notes"
Search
obsidian search query="project alpha"
obsidian search query="TODO" path="projects" limit=10
obsidian search query="meeting" format=json   # Returns JSON array of file paths
obsidian search query="urgent" case
Properties & Tags
obsidian properties path="note.md"
obsidian property:set path="note.md" name="status" value="active"
obsidian property:read path="note.md" name="status"
obsidian property:remove path="note.md" name="draft"
obsidian tags counts sort=count
obsidian tag name="project/alpha"
Tasks
obsidian tasks                          # All tasks (done + todo) — same as tasks all in v1.12
obsidian tasks all                      # All tasks (done + todo)
obsidian tasks done                     # Completed only
obsidian tasks daily                    # Tasks in today's daily note
obsidian task path="note.md" line=12 toggle
obsidian tasks | grep "\[ \]"           # Workaround: filter to incomplete only
Developer & Automation
obsidian eval code="app.vault.getFiles().length"
obsidian dev:screenshot path="folder/screenshot.png"  # Path must be vault-relative
obsidian dev:debug on                                 # Required before dev:console
obsidian dev:console limit=20
obsidian dev:errors
TUI Mode
Running obsidian with no arguments launches an interactive TUI (Terminal User Interface):

Key	Action
↑↓	Navigate files
Enter	Open file
/	Search
n	Create new file
d	Delete file
r	Rename file
q	Quit
Common Agent Patterns
Daily Journal Automation
# Append a timestamped entry
obsidian daily:append content="## $(date '+%H:%M') — Status Update
- Completed: feature branch merge
- Next: code review for PR #42
- Blocked: waiting on API credentials"
Create Note from Template with Metadata
obsidian create path="projects/new-feature" template="project-template"
obsidian property:set path="projects/new-feature.md" name="status" value="planning"
obsidian property:set path="projects/new-feature.md" name="created" value="$(date -I)"
obsidian daily:append content="- Started [[projects/new-feature|New Feature]]"
Vault Analytics Script
obsidian files total                    # Total file count
obsidian tags counts sort=count         # Most used tags
obsidian tasks | grep "\[ \]"          # Incomplete tasks across vault
obsidian orphans                        # Notes needing integration
obsidian unresolved                     # Broken links to fix
Search and Extract for AI Processing
obsidian search query="meeting notes" format=json | jq '.[]'
obsidian read path="meetings/standup.md" | grep "Action item"
Sync Management
obsidian sync:status                    # Check sync health
obsidian sync:history path="important.md"  # Version history
obsidian sync:restore path="important.md" version=3  # Rollback
Execute Obsidian Commands
# Find a command ID, then execute it
obsidian commands | grep "graph"
obsidian command id="graph:open"

# Open settings, trigger a plugin action
obsidian command id="app:open-settings"
obsidian command id="dataview:dataview-force-refresh-views"
Tips
Paths are vault-relative — use folder/note.md, not absolute filesystem paths.
create paths omit .md — the extension is added automatically.
move requires full target path including .md extension.
Pipe-friendly — plain text output works with grep, awk, sed, jq.
JSON output — use format=json on search for a JSON array of file paths. The files command does not support JSON output.
Stderr noise — GPU/Electron warnings on headless are harmless; filter with 2>/dev/null.
daily:prepend inserts content after frontmatter, not at byte 0.
Use eval to run arbitrary JavaScript against the Obsidian API (app.*).
template:insert inserts into the currently active file in the Obsidian UI — it does not accept a path= parameter. If no file is open, it returns Error: No active editor. Open a file first. To create a file from a template via CLI, use obsidian create path="..." template="..." instead.
property:set stores list values as strings — value="tag1, tag2" writes a literal comma-separated string, not a YAML array. For proper array fields, edit the note's frontmatter directly (e.g. via read → modify → create --force) or use eval to call the Obsidian API.
eval requires single-line JavaScript — multiline JS passed inline fails with a token error. Write the script to a temp file instead:
cat > /tmp/obs.js << 'JS'
var files = app.vault.getMarkdownFiles();
files.length;
JS
obsidian eval code="$(cat /tmp/obs.js)"
Multi-vault targeting may not work in all environments — obsidian "My Vault" command can return Error: Command "My Vault" not found on some setups. If this happens, omit the vault name (CLI targets the most recently active vault) and switch vaults manually in the Obsidian UI.
When colon subcommands are unavailable (e.g. Windows Git Bash without wrapper), prefer non-colon alternatives: use properties instead of property:read, and obsidian daily:path + append instead of daily:append.
Troubleshooting
Problem	Cause	Fix
Empty output / hangs	Obsidian not running, or admin terminal (Windows)	Start Obsidian; use normal-privilege terminal
Command not found	CLI not registered in PATH	Re-enable CLI in Settings; restart terminal
Unicode errors	Fixed in v1.12.2+	Update Obsidian
Wrong vault targeted	Multi-vault ambiguity	Pass vault name as first arg
IPC socket not found (Linux)	PrivateTmp=true in systemd	Set PrivateTmp=false
Snap confinement issues	Snap restricts IPC	Use .deb package instead
Multi-vault "Name" command fails	Vault name matching issue	Omit vault name; target most recent vault
property:set list value is a string	CLI stores value as-is	Edit frontmatter directly or use eval
Colon+params exit 127 (missing .com)	Outdated installer — Obsidian.com absent	Reinstall from obsidian.md/download
Colon+params exit 127 (Git Bash / MSYS2)	Bash resolves obsidian to .exe not .com	Create ~/bin/obsidian wrapper: #!/bin/bash / /c/path/to/Obsidian.com "$@" and add export PATH="$HOME/bin:$PATH" to ~/.bashrc