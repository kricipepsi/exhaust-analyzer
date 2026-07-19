# Task Handoff — comlab (pick up here)

_Not auto-loaded. Read this once at the start of the session, then continue the task below._

## Where the task stands
- **Goal:** run the capture across **all 24 rows**, then run the **full test suite**.
- **Status:** blocked last session on environment confusion only — NO code work was lost.
- The previous agent ran in **Git Bash** and tried to execute a **Linux** binary
  (`.sandbox-py/bin/python3.14`) on Windows. It got `Exec format error` and looped
  hunting for an interpreter until it ran out of tokens. The interpreter it needed
  was already present (see below).

## The environment already exists — do NOT rebuild or hunt
There are two ready Windows venvs in the project root, both Python 3.14.6 with
`comlab` editable-installed + pydantic + pytest:

```
.venv-comlab\Scripts\python.exe   <- USE THIS (fuller env, 62 packages)
.venv-host\Scripts\python.exe        leaner alt (35 packages), fallback only
```

Canonical interpreter for this task:
```
C:\Workspace\labs\comlab\.venv-comlab\Scripts\python.exe
```

## Do this
Run in **PowerShell 7** (not Git Bash), from the project root:

```powershell
cd C:\Workspace\labs\comlab
$py = ".\.venv-comlab\Scripts\python.exe"

# 1. sanity check the interpreter (should print OK)
& $py -c "import comlab, pydantic, pytest; print('comlab', comlab.__file__); print('OK')"

# 2. run the 24-row capture
#    (use the project's capture entrypoint here)

# 3. run the full suite
& $py -m pytest
```

## Hard rules (this is what cost the last session)
1. Use `.\.venv-comlab\Scripts\python.exe`. Don't go looking for any other interpreter.
2. Ignore `.sandbox-py` entirely — it's a **Linux** binary and cannot run on Windows.
3. Run in **PowerShell 7**, not Git Bash (Git Bash looks like Linux but runs Windows
   binaries, which is exactly what caused the `Exec format error` loop).
4. If `import comlab` ever fails, re-install into THIS venv with
   `& $py -m pip install -e .` — do not start probing other Pythons.
