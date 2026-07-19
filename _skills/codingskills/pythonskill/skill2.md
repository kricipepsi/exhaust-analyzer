Based on the research, the default knowledge of even frontier Large Language Models (LLMs) is insufficient for production-grade coding. Base models frequently suffer from "library hallucinations," recommending non-existent packages in roughly **20%** of generated code.[1, 2] Furthermore, while a base model like Claude 4.5 or GPT-5 might score ~80% on simple, single-file bug fixes (SWE-bench Verified), its performance drops to **23–45%** on complex, multi-file industrial tasks.[3, 4, 5]

Specialized skills solve this by shifting the AI from a "single-shot" generator to a "generate-validate-fix" loop, which research shows can increase resolution rates on complex tasks by **15–20x**.[6, 7]

Below is an optimized `SKILL.md` for Python development, designed to implement the "Deep Agent" patterns identified in the research.[8, 9]

### Optimized Python Expert Skill (`SKILL.md`)

---
name: python-expert-coder
description: Use when writing, reviewing, or refactoring Python code. Enforces PEP 8, security gating with Bandit, and reliability through deterministic execution loops. Prevents library hallucinations and ensures modern (3.10+) Pythonic patterns.
allowed-tools: [read_file, write_file, exec_command, list_files]
---

# Python Expert Coding Protocol

## 1. Strategic Planning (The "Contract-First" Phase)
Before writing any code, you must define the interface and plan. This prevents "vibe coding" and reduces context rot.[10, 11]
- **Step 1:** Create or update a `task_plan.md` in the project root.
- **Step 2:** Define function signatures with PEP 484 type hints before implementation.
- **Step 3:** Verify the existence of libraries before importing to prevent "slopsquatting".[1, 2]

## 2. Deterministic Validation Loop
Never submit code without a "generate-validate-fix" iteration. Run cheap checks first to save tokens.[6, 7]
1. **Syntax Check:** `python -m py_compile <file>` (Milliseconds).
2. **Fast Linting:** Use `ruff check. --fix` for PEP 8 compliance. Ruff is preferred over Pylint for speed and modern rule coverage.
3. **Security Gate:** Run `bandit -r <file>` to detect CWE vulnerabilities.[12]
4. **Type Check:** Use `mypy` or `pyright` to ensure consistency.[6]

## 3. Execution & Testing
- **Reproduce First:** If fixing a bug, write a failing `pytest` test case *before* attempting the fix.
- **Mocking:** Use `pytest-mock` or `unittest.mock` for external API calls to keep tests deterministic.
- **Environment:** Prefer `uv` for dependency management. Fall back to `pip` only if `uv` is missing.

## 4. Pythonic Standards & Anti-Patterns
- **Modern Syntax:** Use Python 3.10+ features: `match` statements, f-strings, and `pathlib` for paths.
- **Error Handling:** Avoid bare `except:` blocks; use specific exceptions or `contextlib.suppress`.
- **Hallucination Prevention:** If you are unsure if a library exists, use `exec_command` to run `pip index versions <package>` or `uv pip show <package>`.[1, 2]

## 5. Iterative Refinement Strategy
If validation fails, you are granted a **max of 5 iterations** to fix the issue.[6]
- Provide only 3–5 specific error messages to the reasoning loop at a time to avoid overwhelming the context window.[12]
- Use "Context Isolation": When performing a complex refactor, summarize findings to a file and clear your active memory.

### Why This Skill is Optimized:
1.  **Deterministic Before Agentic:** It forces the agent to run high-speed linters (`ruff`) and compilers before using expensive LLM reasoning to "guess" if the code is correct.[6, 11]
2.  **Security Integration:** It explicitly includes `Bandit` checks, which the research shows can reduce security vulnerabilities from **40% to 13%**.[12]
3.  **Token Efficiency:** By using "Progressive Disclosure" (Level 1: description; Level 2: SKILL.md), it prevents your main context window from being flooded with 50,000+ tokens of tool definitions until they are actually needed.[13, 9, 14]
4.  **Retrieval-Augmented Logic:** It moves the agent from relying on its internal memory (which is **20%** prone to package hallucinations) to explicitly checking the environment using commands like `pip index`.