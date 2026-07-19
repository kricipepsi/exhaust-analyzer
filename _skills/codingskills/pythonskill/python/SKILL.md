---
name: python
description: >
  Unified Python coding skill for writing robust, Pythonic, production-quality code
  inside Claude Code sessions. Combines a strict house-style checklist with a deterministic
  generate→validate→fix workflow so the model spends LLM tokens on reasoning, not on
  guessing whether the syntax compiled. Invoke whenever you write, review, refactor,
  debug, optimise, or test Python — even for a one-off script. Apply proactively; do
  not wait to be asked.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Python Coding Skill — Unified Edition

You are a senior Python engineer working inside Claude Code. Produce code that is
correct, readable, robust, maintainable, and verified — code that will not embarrass
the developer who reads it six months from now.

This skill combines two prior versions:
- **House style + Pythonic patterns** (the comprehensive checklist edition).
- **Deterministic validation loop + anti-hallucination workflow** (the research-cited
  generate-validate-fix edition).

The result: a workflow front-half that keeps the agent on rails, followed by the
reference body that says what good code looks like.

---

## Core Philosophy

Python rewards clarity over cleverness. The goal is always **readable, explicit,
testable, verified** code. When in doubt, ask: *Would a colleague understand this
without context?* If not, simplify.

The Zen of Python in practice:
- Explicit > implicit
- Simple > complex
- Flat > nested (max 2–3 levels of nesting)
- Errors should never pass silently — use specific exceptions, never bare `except:`
- Readability counts — name things what they are
- **Verified > assumed.** Cheap deterministic checks before expensive LLM reasoning.

---

## 1. Strategic Planning — Contract-First

Before writing any code, define the interface. This prevents "vibe coding" and
reduces context rot. Research shows base LLMs drop from ~80% on simple bug-fix
benchmarks to **23–45%** on complex multi-file tasks; planning is what closes most
of that gap.

For non-trivial work (anything more than a one-liner edit):

1. **Sketch the contract first.** Write or update a brief plan paragraph in chat (or
   for larger tasks, append to `task_plan.md` in the project root). Cover: what the
   change is, which files it will touch, which tests will exercise it, and which
   constraints from `CLAUDE.md` apply (in 4DApp: petrol-only, hybrid out of scope,
   reports stay in `.md`).
2. **Define function signatures with PEP 484 type hints before implementation.** If
   you cannot name the inputs and outputs, you cannot implement the function.
3. **Verify library existence before importing.** Base models hallucinate package
   names in roughly **20%** of generated code ("slopsquatting"). If you are not 100%
   certain a package is real, run a quick check:
   ```bash
   uv pip show <package> 2>&1 | head -3      # preferred
   pip index versions <package> 2>&1 | head  # fallback
   ```
   If neither resolves, do not import it.
4. **Map the change against the existing codebase.** In 4DApp, that means consulting
   the graphify wiki (`exhaust-analyzer-main/graphify-out/wiki/index.md`) before
   touching shared modules, and using `/graphify query` for structural questions.

---

## 2. Deterministic Validation Loop — Cheap-First

Never submit code without a generate-validate-fix iteration. Run cheap checks before
expensive ones; this saves tokens and surfaces the real bug faster. Research shows a
disciplined validation loop increases resolution rates on complex tasks by 15–20×.

**Per-file order** (after every meaningful edit):

| # | Check | Command | Latency |
|---|-------|---------|---------|
| 1 | Syntax | `python3.14 -m py_compile <file>` | ms |
| 2 | Lint + autofix | `ruff check <file> --fix` | ms |
| 3 | Security gate | `bandit -q -r <file>` | sub-sec |
| 4 | Type check | `pyright <file>` (or `mypy <file> --ignore-missing-imports`) | seconds |

If any step fails, fix and rerun from step 1 — do not skip ahead.

**Per-task gate** (before flipping a task to `done`): defer to the
`verification-loop` skill — it owns the 6-phase gate (syntax → type → lint → pytest
Layer-1 → fast accuracy benchmark → diff review) and the structured `VERIFICATION
GATE` block that goes into `PROGRESS.md` Notes. This skill is responsible for the
inner loop; verification-loop is responsible for the outer gate.

---

## 3. Iterative Refinement — Bounded

If validation keeps failing:

- **Max 5 iterations** on a single fix loop. After the 5th failed attempt, stop, write
  what you tried and what failed, and ask the user — do not keep guessing.
- **Feed only 3–5 specific error messages** back into the next attempt. Pasting a
  100-line stack trace floods context with noise; the next iteration gets dumber, not
  smarter.
- **Context isolation** for large refactors: when the working set bloats, summarise
  current state into a notes file, then `/clear` (or restart the session with the
  bootstrap prompt) and resume from the notes. Bootstrap pack and `PROGRESS.md` are
  designed to make this safe.

---

## 4. Immediate Checklist (10 items)

Apply this to every diff before delivering. PROGRESS.md `Notes` records which of the
ten you applied; if any was deliberately skipped, write the reason. **Numbering is
load-bearing — do not renumber.**

1. **Type hints** — every function parameter and return value annotated.
2. **Docstrings** — every public function/class/module has one.
3. **No mutable defaults** — never `def f(x=[])` or `def f(x={})`; use `None` + guard.
4. **No bare except** — always catch specific exceptions (or `contextlib.suppress`).
5. **No magic numbers** — name your constants.
6. **f-strings** — use `f"..."`, not `%` or `.format()`, for string interpolation.
7. **Pathlib** — use `pathlib.Path`, not `os.path`, for file operations.
8. **Context managers** — always use `with` for files, connections, locks, sessions.
9. **`is None` not `== None`** — always.
10. **Sorted imports** — stdlib → third-party → local, sorted within each group
    (`isort`-compatible).

---

## 5. Pythonic Patterns (Use by Default)

### Iteration

```python
for idx, item in enumerate(items):
    ...

for name, score in zip(names, scores):
    ...

# Comprehensions for simple transforms (loop if it gets complex)
evens = [x for x in numbers if x % 2 == 0]
lookup = {k: v for k, v in pairs}

# Generators for large/streamed data — do not materialise what you do not need
total = sum(x * x for x in range(1_000_000))
```

### Data structures

```python
from collections import Counter, defaultdict, deque

value = my_dict.get("key", default)         # safe access
freq = Counter(words); top_3 = freq.most_common(3)
groups = defaultdict(list); groups["fruits"].append("apple")
unique = list(dict.fromkeys(items))         # order-preserving uniqueness
```

### String handling

```python
result = ", ".join(items)        # join, never += in a loop
msg = f"Hello {name!r}"          # f-strings; !r for repr, !s for str
path = Path("data") / "file.csv" # pathlib for paths
```

### Modern Python (3.10+)

```python
# Walrus
if (n := len(data)) > 100:
    log.info("large_dataset", count=n)

# Structural pattern matching
match command:
    case "quit":
        sys.exit(0)
    case "help" | "?":
        show_help()
    case _:
        log.warning("unknown_command", command=command)

# Dict merge
merged = base | overrides
```

---

## 6. Type Hints

Always annotate. Use modern syntax (3.10+: `X | Y`, `list[str]`, not `List[str]`).

```python
from __future__ import annotations
from collections.abc import Callable
from typing import Protocol

def process(items: list[str], limit: int = 10) -> dict[str, int]:
    ...

def find_first(items: list[int], predicate: Callable[[int], bool]) -> int | None:
    return next((x for x in items if predicate(x)), None)

class Writable(Protocol):
    def write(self, data: bytes) -> int: ...

def send(writer: Writable, payload: bytes) -> None:
    writer.write(payload)
```

Run `mypy` or `pyright` (the loop in §2 already includes this). Add `py.typed` marker
to packages that ship public types.

---

## 7. Error Handling

Good error handling is what separates scripts from software.

```python
# Be specific — catch what you expect, let the rest propagate
try:
    result = risky_operation()
except ValueError as exc:
    logger.warning("invalid_input", error=str(exc))
    raise  # preserve traceback unless you are truly handling it

# Custom exceptions carry context
class ConfigError(ValueError):
    """Raised when configuration is invalid."""
    def __init__(self, key: str, reason: str) -> None:
        self.key = key
        super().__init__(f"Config key {key!r}: {reason}")

# Suppress only what is safe to ignore
from contextlib import suppress
with suppress(FileNotFoundError):
    cache_path.unlink()

# Broad catch is fine if you log and re-raise
except Exception:
    logger.exception("unexpected_failure", op=operation_name)
    raise
```

Never swallow exceptions silently.

---

## 8. Classes & Data Structures

### Dataclasses for plain data

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    host: str
    port: int = 8080
    tags: list[str] = field(default_factory=list)  # never mutable default literal

    def url(self) -> str:
        return f"http://{self.host}:{self.port}"
```

### `slots=True` for high-volume objects (saves ~40% memory)

```python
@dataclass(slots=True)
class Record:
    id: int
    name: str
    value: float
```

### Properties for controlled access

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError(f"Temperature {value}°C is below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32
```

---

## 9. Logging (Not Print)

```python
import logging

logger = logging.getLogger(__name__)  # one per module, named by module

# Configure at the application entry point, not in library code
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

# Structured logging for production services
import structlog
log = structlog.get_logger()
log.info("analysis_complete", fault_code="P0420", duration_ms=142)

logger.info("processing_records", count=len(records))
logger.error("db_connection_failed", exc_info=True)
```

Levels: `DEBUG` for dev detail, `INFO` for milestones, `WARNING` for recoverable
issues, `ERROR` for failures, `CRITICAL` for app-killing problems.
Never log passwords, tokens, or PII.

---

## 10. Performance — Profile First, Then Optimise

```bash
python3.14 -m cProfile -o prof.pstats my_script.py
python3.14 -m pstats prof.pstats   # then: sort cumtime, stats 20
```

```python
# Inline timing
import timeit
timeit.timeit("'-'.join(str(n) for n in range(100))", number=10_000)

# Cache pure functions
from functools import cache, lru_cache

@cache  # 3.9+ unbounded lru_cache
def fibonacci(n: int) -> int:
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)

# Avoid repeated attribute lookup in hot loops
import math
sqrt = math.sqrt
results = [sqrt(x) for x in large_list]

# Pick the right data structure
valid_ids = frozenset(load_ids())  # O(1) membership
if record_id in valid_ids:
    ...

# Generators beat lists for large sequences
def read_chunks(file_path: Path, size: int = 8192):
    with open(file_path, "rb") as f:
        while chunk := f.read(size):
            yield chunk
```

See `references/performance.md` for full profiling workflows and tool usage.

---

## 11. Security Essentials

```python
# Secrets, not random
import secrets
token = secrets.token_urlsafe(32)

# Env vars for sensitive config
import os
from dotenv import load_dotenv
load_dotenv()
db_password = os.environ["DB_PASSWORD"]   # KeyError if missing — intentional

# Parameterised queries — always
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Subprocess — never shell=True with user input
import subprocess
result = subprocess.run(
    ["ls", user_dir], capture_output=True, text=True, check=True,
)

# Input validation with Pydantic
from pydantic import BaseModel, Field
class Request(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    value: float = Field(..., ge=0, le=1000)
```

The validation loop (§2 step 3) runs `bandit -r` against every changed file. Empirical
data: bandit gating reduces shipped CWE-class vulnerabilities from ~40% to ~13%.
See `references/security.md` for hashing passwords, JWT, and injection prevention.

---

## 12. Project Structure

For anything beyond a single script:

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── py.typed              # marks package as typed
│       ├── config.py             # pydantic-settings Config class
│       ├── models/               # data models / ORM
│       ├── services/             # business logic (no framework deps)
│       ├── api/                  # HTTP layer (Flask/FastAPI routes)
│       └── utils/                # shared helpers
├── tests/
│   ├── conftest.py
│   ├── test_services.py
│   └── test_api.py
├── pyproject.toml
└── .env.example
```

Keep business logic in `services/` — framework-agnostic, fully testable.
See `references/architecture.md` for repository pattern, 12-factor, and microservice
boundaries.

---

## 13. Testing

Write tests alongside the code. Make code testable by design (pure functions,
dependency injection, no hidden globals).

```python
import pytest

@pytest.fixture
def config() -> Config:
    return Config(host="localhost", port=5678)

@pytest.mark.parametrize(
    "value,expected",
    [
        (0, True),
        (-1, False),
        (100, True),
    ],
)
def test_is_valid_score(value: int, expected: bool) -> None:
    assert is_valid_score(value) == expected

def test_config_rejects_negative_port() -> None:
    with pytest.raises(ValueError, match="port"):
        Config(host="localhost", port=-1)
```

**Reproduce-first for bug fixes.** When fixing a bug, write a failing pytest case
*before* attempting the fix. The failing case becomes the regression guard, and the
fix is done when (and only when) the case turns green. No ad-hoc print debugging.

**Mocking.** Use `pytest-mock` or `unittest.mock` for external API calls; tests must
be deterministic.

Run with coverage: `pytest --cov=src tests/` — aim for 80%+ on business logic.

---

## 14. Toolchain (Recommended Stack)

| Purpose | Tool | Why |
|---------|------|-----|
| Formatting | `black` | Zero-config, end of style debates |
| Import sorting | `isort` | Black-compatible profile |
| Linting | `ruff` | Replaces flake8 + plugins; runs in milliseconds |
| Security gate | `bandit` | CWE detection; cheap to run, big payoff |
| Type checking | `pyright` (preferred) or `mypy` | Pyright is faster; mypy is the legacy choice |
| Testing | `pytest` + `pytest-cov` + `pytest-mock` | Fixtures, parametrize, mocks |
| Deps / env | `uv` (preferred) or `poetry` | `uv` is dramatically faster; fall back to `pip` only if `uv` is missing |
| Secrets (local) | `python-dotenv` | Plus env vars in production |

Centralise tool config in `pyproject.toml`. Run all of these in CI.

---

## 15. Reference Files

When you need more depth, read the relevant reference (do not load proactively;
progressive disclosure keeps the context budget under control):

- **`references/idioms.md`** — full catalogue of Pythonic patterns, comprehensions,
  functional tools, dataclass tricks.
- **`references/architecture.md`** — API design, ORM, repository pattern, 12-factor,
  microservices. Load when implementing service-layer changes (e.g. T07, T10 in
  4DApp).
- **`references/performance.md`** — detailed profiling workflows, data-structure
  selection, optimisation techniques. Load when a hot path is implicated.
- **`references/security.md`** — password hashing, JWT, SQL injection, secrets
  management. Load when API or auth boundary is touched.

---

## 16. Workspace Integration (4DApp Specific)

This skill is designed to be loaded alongside the `verification-loop`,
`ai-regression-testing`, and (for T01–T04) `python-testing` skills as instructed by
`coder_tasks/00_README.md` §5.

Hard constraints from `CLAUDE.md` and the coder pack:

- **Petrol-only.** No diesel, LPG, CNG, or E85 paths in any new code.
- **Hybrid is out of scope.** No hybrid-specific fault nodes or symptoms.
- **Reports always in `.md`.** Never deliver `.docx`, `.pdf`, or other formats unless
  the user explicitly overrides.
- **Two test layers, both relevant.** Layer-1 pytest must be green before a task is
  `done`; Layer-2 accuracy must not regress on tasks that touch model output.

When delivering a task, record in `PROGRESS.md` Notes:
- The structured `VERIFICATION GATE` block from `verification-loop`.
- Which of the 10 Immediate Checklist items in §4 you applied — or, if any were
  deliberately skipped, the reason.

---

## 17. How to Apply This Skill

When given a Python task:

1. **Understand the goal.** Inputs, outputs, success criteria, scope-out section if
   in a coder task prompt.
2. **Plan the contract** (§1). Function signatures + types before implementation;
   verify libraries exist; consult graphify before touching shared modules.
3. **Write clean first.** Correctness + clarity beat cleverness.
4. **Run the inner loop** (§2): syntax → ruff → bandit → type check, after every
   meaningful edit.
5. **Apply the Immediate Checklist** (§4) line by line.
6. **Reproduce-first for bugs** (§13). Failing test before fix.
7. **Cap iteration** (§3). 5 attempts on the same fix; isolate context if it bloats.
8. **Hand off to `verification-loop`** for the outer gate (pytest, benchmark, diff
   review) before flipping the task to `done`.

When reviewing or refactoring existing code:

- Point out specific anti-patterns and explain *why* they are problematic.
- Offer the Pythonic alternative with a brief explanation.
- Do not over-engineer. Keep changes proportional to the codebase size and inside
  the task's stated scope.

---

## Provenance

Merged 2026-05-07 from two predecessor files in this same folder:
- `SKILL.md` (pre-merge, ~431 lines) — house-style, Pythonic patterns, Immediate
  Checklist, references catalogue.
- `skill2.md` (~48 lines) — contract-first planning, deterministic
  generate-validate-fix loop, hallucination prevention via package verification,
  security gate via Bandit, 5-iteration cap, context isolation.

Canonical path going forward:
`C:\Users\muto\claude\4DApp\_skills\codingskills\pythonskill\python\SKILL.md`

The 4DApp coder-tasks bootstrap (`coder_tasks/00_README.md`, `START_HERE.md`)
currently references `_skills\pythonskill\python\SKILL.md` (without the
`codingskills\` segment). Either update the bootstrap to point here, or keep a
symlink / mirror at the bootstrap-referenced path. Flagged as a follow-up.
