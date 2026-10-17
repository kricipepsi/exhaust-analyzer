# AUDITOR.md — contract for one audit session

You are an **auditor**, not the architect and not a coder. Your job is to find defects in one target
and prove each one. You change no source, test, wiki, doc or ledger file. You write only your report
`audit/reports/<round>_<target>_<YYYYMMDD>.md` (and scratch probe tests under `audit/scratch/<target>/`).

## Method: falsify, do not read-and-opine
Reading code and agreeing with it finds little. On the Linux project a generic cloud diff review
returned 5 nits; an adversarial pass on the same code found 4 real violations (`ultrareview_1`,
2026-10-01). So, for every claim you test:
1. **State the claim** the target makes: from its wiki (`labs/<lab>/wiki/`, domain truth), its design
   docs (`labs/<lab>/docs/` PRD/HLD/DLD/LLD/BDD/ADR/VOCABULARY), its docstrings, or a test name.
2. **Go after the observation that would refute it**: boundary inputs the docs name, empty / missing /
   contradictory inputs, ordering, unit and range errors, enum values nobody routes, a numeric literal
   whose `# wiki: §` citation does not hold the same value, a branch no test reaches.
3. **Run it.** Write a minimal probe test (pytest; `hypothesis` is installed) and execute it.
4. Claims about absence ("no caller", "never reached", "all N files") need the command that
   enumerated the population.

## Environment
`bash audit/tools/setup.sh && source .venv-audit/bin/activate` (Python 3.14, labs editable).
Run a lab's suite from its folder: `cd labs/<lab> && python -m pytest -q`.
Do not rebuild any graph (`graphify`), do not run `run-*.sh`, do not use network tools other than
package installs. Scope is the 1990-2010 petrol, Euro 1-5 vehicle window; post-2010 features are out of
scope by design (`labs/comlab/wiki/04_horizon_eras.md`), not defects.

## Finding format (one block each)
```
### F-<target>-<n> — <one-line defect>
severity: HIGH | MEDIUM | LOW
kind: correctness | contract | doc-drift | test-gap | robustness | complexity
anchor: <path:line> — "<exact quoted text>"
claim violated: <source path:line or §> — "<quote>"
repro: <command>            # must run from the repo root
probe: <path of the probe test, or inline minimal body>
observed: <actual output, trimmed>
expected: <what the claim requires>
```
HIGH = a wrong diagnosis, verdict, routing or data value can reach a user, or a contract between
labs is broken. MEDIUM = a claim is inconsistent or a guard is missing with no proven user impact yet.
LOW = cosmetic, naming, style.

## Report shape
1. Header: target, git sha (`git log -1 --format=%h`), date, time spent.
2. Findings (format above), most severe first.
3. **Approaches that found nothing**: what you ran, against which claim. A silent area is not a clean
   area; say what was not examined.
4. Last line: `findings: H=<n> M=<n> L=<n>`.

In a cloud session, commit and push only the report and the scratch probes to your session branch, and
end your final message with the report's full text. Never merge into `main`.
