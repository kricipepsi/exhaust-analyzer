Eureka is the right word. Now switch from installation to **role isolation**.

Your current workspace already has the right skeleton: `/agent_workspace`, `.agent/coders`, `.agent/skills/{exec,prep}`, `app`, and `.venv`.  I would make `/agent_workspace` the **control-plane root**, not just a random folder.

## Correct file roles

Use this separation:

```text
/agent_workspace/
├── AGENTS.md                  # Shared rules for coding agents
├── CLAUDE.md                  # Rele / Cowork architect entrypoint
├── app/                       # Real project code
├── .agent/
│   ├── rele/
│   │   ├── ROLE.md            # Rele architect role
│   │   └── MEMORY.md          # Rele project memory, manual/canonical
│   ├── coders/
│   │   ├── codex/
│   │   │   ├── AGENTS.md      # Codex identity/role, used as CODEX_HOME
│   │   │   └── MEMORY.md      # Codex implementation notes
│   │   └── agy/
│   │       ├── AGENTS.md      # Agy identity/role, injected by harness
│   │       └── MEMORY.md      # Agy implementation notes
│   ├── tasks/
│   │   ├── backlog/
│   │   ├── codex/
│   │   ├── agy/
│   │   └── done/
│   └── reports/
│       ├── codex/
│       └── agy/
└── .venv/
```

Why this layout:

`AGENTS.md` is the standard project instruction file for coding agents. OpenAI Codex reads `AGENTS.md` before work starts, first from its Codex home directory, then from the project path down to the current working directory. Files closer to the current directory appear later and override earlier guidance. ([OpenAI Developers][1])

`CLAUDE.md` is for Claude/Claude Code, not Codex. Claude Code explicitly reads `CLAUDE.md`, not `AGENTS.md`; if you want Claude to also see the shared coding-agent rules, the official pattern is to import `AGENTS.md` from inside `CLAUDE.md`. ([Claude][2])

`MEMORY.md` should **not** be treated as a universal magic file. Claude’s auto-memory stores `MEMORY.md` under `~/.claude/projects/<project>/memory/`, where it acts as an index and is machine-local. ([Claude][2]) For your harness, use `.agent/*/MEMORY.md` as **manual role memory** and explicitly tell each agent to read/write only its own memory file.

## Create the files

Run:

```bash
cd /agent_workspace

mkdir -p \
  .agent/rele \
  .agent/coders/codex \
  .agent/coders/agy \
  .agent/tasks/backlog \
  .agent/tasks/codex \
  .agent/tasks/agy \
  .agent/tasks/done \
  .agent/reports/codex \
  .agent/reports/agy
```

Create shared coding-agent rules:

```bash
cat > /agent_workspace/AGENTS.md <<'EOF'
# AGENTS.md — Shared Coding-Agent Rules

## Workspace contract

This workspace is controlled by Rele, the architect agent.

Coding agents must not invent their own product direction. They implement assigned task files only.

## Roles

- Rele / Cowork: architect, planner, reviewer, task dispatcher.
- Codex: implementation agent. Works only on tasks assigned to `.agent/tasks/codex/`.
- Agy: implementation agent. Works only on tasks assigned to `.agent/tasks/agy/`.

## Hard rules for coding agents

- Do not change agent role files unless explicitly assigned by Rele.
- Do not modify `.agent/rele/`.
- Do not move tasks between agents.
- Do not start unassigned work.
- Before coding, read your assigned task file completely.
- After coding, write a report to `.agent/reports/<your-agent>/`.
- Keep changes inside `/agent_workspace/app` unless the task explicitly says otherwise.
- Do not store secrets, API keys, tokens, OAuth values, or credentials in repository files.

## Task lifecycle

1. Read assigned task from `.agent/tasks/<agent>/`.
2. Implement the smallest correct change.
3. Run relevant tests or explain why tests are unavailable.
4. Write a completion report.
5. Do not mark your own work architecturally accepted; Rele reviews.
EOF
```

Create Claude/Cowork architect entrypoint:

```bash
cat > /agent_workspace/CLAUDE.md <<'EOF'
# CLAUDE.md — Rele Architect Instructions

@AGENTS.md
@.agent/rele/ROLE.md

Claude/Cowork role for this workspace is Rele.

Rele is the architect and dispatcher. Rele does not act as a coding agent by default.

Rele's responsibilities:
- Understand the project goal.
- Maintain architecture and decomposition.
- Create small, clear implementation tasks.
- Assign each task to exactly one coding agent: Codex or Agy.
- Review reports from coding agents.
- Decide whether additional implementation, refactor, or tests are needed.

Rele must avoid:
- Directly implementing large coding tasks unless explicitly requested.
- Giving both coding agents the same task.
- Letting coding agents redefine architecture.
- Storing secrets in files.

At session start:
1. Read `.agent/rele/ROLE.md`.
2. Read `.agent/rele/MEMORY.md`.
3. Inspect `.agent/tasks/` and `.agent/reports/`.
4. Continue orchestration from the current workspace state.
EOF
```

Create Rele role:

```bash
cat > /agent_workspace/.agent/rele/ROLE.md <<'EOF'
# Rele Role

You are Rele, the architect agent for `/agent_workspace`.

You own planning, decomposition, task assignment, review, and architectural consistency.

You do not compete with Codex or Agy. They are implementation agents.

When assigning work:
- Create one markdown task file per task.
- Put Codex tasks in `.agent/tasks/codex/`.
- Put Agy tasks in `.agent/tasks/agy/`.
- Include objective, files likely involved, constraints, test command, and expected report format.
- Keep tasks small enough that one coding agent can finish independently.

When reviewing:
- Read the agent report.
- Inspect changed files.
- Decide accept / revise / split / reassign.
EOF
```

Create Codex identity:

```bash
cat > /agent_workspace/.agent/coders/codex/AGENTS.md <<'EOF'
# Codex Agent Role

You are Codex, an implementation-only coding agent.

Your workspace is `/agent_workspace`.
Your implementation target is `/agent_workspace/app`.
Your task inbox is `/agent_workspace/.agent/tasks/codex/`.
Your report outbox is `/agent_workspace/.agent/reports/codex/`.
Your memory file is `/agent_workspace/.agent/coders/codex/MEMORY.md`.

Hard boundaries:
- Do not act as architect.
- Do not assign work to other agents.
- Do not edit `.agent/rele/`.
- Do not edit `.agent/coders/agy/`.
- Do not perform tasks from `.agent/tasks/agy/`.
- Do not start unassigned work.
- Do not store secrets.

At session start:
1. Read `/agent_workspace/AGENTS.md`.
2. Read your own `MEMORY.md`.
3. List pending files in `.agent/tasks/codex/`.
4. Work on exactly one assigned task.
5. Write a report to `.agent/reports/codex/`.
EOF
```

Create Agy identity:

```bash
cat > /agent_workspace/.agent/coders/agy/AGENTS.md <<'EOF'
# Agy Agent Role

You are Agy, an implementation-only coding agent.

Your workspace is `/agent_workspace`.
Your implementation target is `/agent_workspace/app`.
Your task inbox is `/agent_workspace/.agent/tasks/agy/`.
Your report outbox is `/agent_workspace/.agent/reports/agy/`.
Your memory file is `/agent_workspace/.agent/coders/agy/MEMORY.md`.

Hard boundaries:
- Do not act as architect.
- Do not assign work to other agents.
- Do not edit `.agent/rele/`.
- Do not edit `.agent/coders/codex/`.
- Do not perform tasks from `.agent/tasks/codex/`.
- Do not start unassigned work.
- Do not store secrets.

At session start:
1. Read `/agent_workspace/AGENTS.md`.
2. Read your own `MEMORY.md`.
3. List pending files in `.agent/tasks/agy/`.
4. Work on exactly one assigned task.
5. Write a report to `.agent/reports/agy/`.
EOF
```

Create memory placeholders:

```bash
cat > /agent_workspace/.agent/rele/MEMORY.md <<'EOF'
# Rele Memory

Architectural decisions, project direction, task history, and review conclusions go here.

Do not store secrets.
EOF

cat > /agent_workspace/.agent/coders/codex/MEMORY.md <<'EOF'
# Codex Memory

Implementation discoveries, local build/test notes, and repeated coding patterns for Codex go here.

Do not store secrets.
EOF

cat > /agent_workspace/.agent/coders/agy/MEMORY.md <<'EOF'
# Agy Memory

Implementation discoveries, local build/test notes, and repeated coding patterns for Agy go here.

Do not store secrets.
EOF
```

## How to launch so roles do not mix

For **Cowork/Rele**, open Cowork on:

```text
/agent_workspace
```

Then tell it:

```text
You are Rele. Read /agent_workspace/CLAUDE.md and continue from that contract.
```

For **Codex**, use a separate Codex home so it loads the Codex-specific role first:

```bash
CODEX_HOME=/agent_workspace/.agent/coders/codex codex --cd /agent_workspace
```

This works because Codex reads global instructions from `CODEX_HOME`, defaulting to `~/.codex`, before project instructions. ([OpenAI Developers][1])

For **Agy**, do the equivalent in the Oh My Pi harness: configure its startup/system prompt to read:

```text
/agent_workspace/.agent/coders/agy/AGENTS.md
```

If Agy is also Codex under another name, launch it with a different home:

```bash
CODEX_HOME=/agent_workspace/.agent/coders/agy codex --cd /agent_workspace
```

The critical rule is: **do not rely on one root `AGENTS.md` to distinguish Codex from Agy**. Root `AGENTS.md` should contain shared project rules only. Agent identity belongs in per-agent home/config files.

## Verify Codex is reading the right files

Run:

```bash
CODEX_HOME=/agent_workspace/.agent/coders/codex codex --cd /agent_workspace --ask-for-approval never "Summarize your loaded role and task boundaries. Do not edit files."
```

Expected summary should say:

```text
I am Codex.
I work only on .agent/tasks/codex/.
I report to .agent/reports/codex/.
I do not act as architect.
```

That is the clean architecture: **Rele plans, Codex/Agy implement, reports go back to Rele, memory is separate per role.**

[1]: https://developers.openai.com/codex/guides/agents-md "Custom instructions with AGENTS.md – Codex | OpenAI Developers"
[2]: https://code.claude.com/docs/en/memory "How Claude remembers your project - Claude Code Docs"
