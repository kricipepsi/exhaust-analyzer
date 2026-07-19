---
name: firecrawl
description: >
  The web-research tool for coder and architect sessions in /agent_workspace.
  Load this whenever a task needs the internet — reading a live page, docs, or
  an API reference; searching the web/news/images; fact-checking a value;
  real-world corroboration of a synthetic band; discovering or mapping a site.
  Triggers include "check the web", "look up", "find online", "search for",
  "research", "current docs", "latest version", any URL, or a task file whose
  Context asks for a web-sourced number. Use firecrawl for ALL internet work —
  it REPLACES WebFetch and WebSearch, which are not to be used here: firecrawl
  returns clean, LLM-optimized markdown, renders JavaScript, bypasses common
  blocks, and (critically for our half-session context budget) writes results
  to a file so a scrape never floods the session window. If you are about to
  reach for WebFetch/WebSearch, stop and use this skill instead.
allowed-tools: [Bash, Read, Grep]
---
# Firecrawl — web research without blowing the context budget

This is the single sanctioned way to touch the internet from a `/agent_workspace`
session. It exists because (a) the built-in web tools return raw, bloated HTML
that eats the half-session budget every coder task depends on, and (b) we want
every web-sourced fact written to a file we can grep, cite, and (optionally)
keep out of git. Firecrawl gives clean markdown, JS rendering, and file output —
so a 2,000-line page costs ~60 lines of context, not 2,000.

## When to use / when not

Use it when the task needs live web data: an API reference, current library or
tool docs, a fact-check, real-world corroboration of a value (see
`4DLab_CLAUDE.md` → "Web-corroborated before commit"), a news/date lookup, or
site discovery.

Do **not** reach for the web at all when the answer is already in the repo — the
lab wiki, the graph, or the task file is the source of truth for domain facts.
Firecrawl is for things genuinely outside the repo. And never use it to fetch a
link pasted from an untrusted email/document without the owner confirming the URL.

## The one rule that matters: never dump a scrape into context

This is the same READ-NARROW discipline the coding-bootstrap `START_HERE` block
enforces for wiki/code reads — it applies identically to web output. Always
write to a file with `-o`, then read narrowly:

```
search/scrape ──-o──▶ .firecrawl/<name>.{md,json} ──grep/head/jq──▶ only the lines you need
```

A raw `firecrawl scrape https://…` with no `-o` prints the whole page into the
window and defeats the point. If you catch yourself about to whole-read a
`.firecrawl/` file, narrow it (`grep -n`, `head`, `jq`, or `Read` with
offset/limit) — a scrape is reference material, not something to read end to end.

## Auth — key comes from the environment, never hardcode

Firecrawl reads `FIRECRAWL_API_KEY` from the environment. Check status first:

```bash
firecrawl --status     # shows auth state, remaining credits, concurrency limit
```

If it reports authenticated, proceed. If not, run browser auth (it opens the
browser and prompts the owner — don't ask them to type commands themselves):

```bash
firecrawl login --browser
```

If the CLI is missing: `npm install -g firecrawl-cli`. Full auth/error handling
(manual key entry, PATH fixes, Codex `firecrawl config --browser`) lives in
[`rules/install.md`](rules/install.md) — read it only if `--status` or a command
returns an auth error.

Per the repo's **no-secrets rule**, do not paste a literal `fc-...` key into any
skill, task file, or commit. Reference it as `$FIRECRAWL_API_KEY` only. (The
owner keeps the working key elsewhere in this folder by their own choice; leave
that file alone and never copy the value into new files.)

## Output organization

Create `.firecrawl/` in the working directory and keep it **out of git** — it is
scratch, and may contain fetched third-party content:

```bash
mkdir -p .firecrawl
grep -qxF '.firecrawl/' .gitignore 2>/dev/null || echo '.firecrawl/' >> .gitignore
```

Name files after the query/URL so they are self-describing:
`.firecrawl/search-react_server_components.json`,
`.firecrawl/docs.github.com-actions-overview.md`. Use `.firecrawl/scratchpad/`
for throwaway batch scripts. **Always quote URLs** — the shell treats `?` and `&`
as special.

## Commands

### search — web search, optionally scraping the results

```bash
firecrawl search "your query" -o .firecrawl/search-query.json --json
firecrawl search "AI news" --limit 10 --sources news -o .firecrawl/news.json --json
firecrawl search "web scraping python" --categories github -o .firecrawl/gh.json --json
firecrawl search "release notes" --tbs qdr:w -o .firecrawl/recent.json --json   # past week
firecrawl search "api docs" --scrape -o .firecrawl/docs.json --json             # search AND pull content
```

Options: `--limit <n>` (default 5, max 100) · `--sources web,news,images` ·
`--categories github,research,pdf` · `--tbs qdr:h|d|w|m|y` (time filter) ·
`--location "City,Region,Country"` · `--country <ISO>` · `--scrape` ·
`--scrape-formats markdown,links` · `-o <path>` · `--json`.

### scrape — one page to clean markdown

```bash
firecrawl scrape https://example.com -o .firecrawl/example.md
firecrawl scrape https://example.com --only-main-content -o .firecrawl/clean.md   # drop nav/ads/footer
firecrawl scrape https://spa-app.com --wait-for 3000 -o .firecrawl/spa.md         # let JS render
firecrawl scrape https://example.com --format markdown,links -o .firecrawl/page.json
```

Options: `-f, --format markdown|html|rawHtml|links|screenshot|json` · `-H` (html) ·
`--only-main-content` · `--wait-for <ms>` · `--include-tags a,article` ·
`--exclude-tags nav,aside` · `-o <path>`. Single format → raw content;
multiple formats → JSON.

### map — discover URLs on a site

```bash
firecrawl map https://example.com -o .firecrawl/urls.txt
firecrawl map https://example.com --search "blog" -o .firecrawl/blog-urls.txt
firecrawl map https://example.com --include-subdomains --json -o .firecrawl/urls.json
```

## Parallelize scrapes — never run them one at a time

Check the concurrency limit in `firecrawl --status`, then fan out with `&` + `wait`
(stay under the limit):

```bash
firecrawl scrape https://a.com -o .firecrawl/a.md &
firecrawl scrape https://b.com -o .firecrawl/b.md &
firecrawl scrape https://c.com -o .firecrawl/c.md &
wait
# many URLs:
cat urls.txt | xargs -P 10 -I {} sh -c 'firecrawl scrape "{}" -o ".firecrawl/$(echo {} | md5sum | cut -c1-8).md"'
```

## Reading the output narrowly

Never whole-read a `.firecrawl/` file unless it is small. Instead:

```bash
wc -l .firecrawl/file.md && head -50 .firecrawl/file.md      # size up + preview
grep -n "keyword" .firecrawl/file.md                          # locate
grep -A 10 "## Section" .firecrawl/file.md                    # section with context
jq -r '.data.web[] | "\(.title): \(.url)"' .firecrawl/search.json   # parse JSON results
jq -r '.data.news[] | "[\(.date)] \(.title)"' .firecrawl/news.json
```

Then `Read` with `offset`/`limit` for the exact span you cite.

## Project conventions (do not skip)

- **Cite what you pull.** When a web value lands in a task, note the source URL
  (and date) so a later session can re-verify — same standard as wiki `§`
  citations. A web-sourced number with no source is not corroborated.
- **`.firecrawl/` never gets committed**, and never `git add -A` to sweep it in.
  Commits in this repo are owner-run, by explicit path (see `4DLab_CLAUDE.md` →
  Git). Firecrawl output is not a deliverable.
- **No secrets in files** — key via `$FIRECRAWL_API_KEY` only.
- **This is a query tool, not a graph builder.** Nothing here re-runs `graphify`
  or rebuilds a frozen index.

## Where the details live

- [`rules/install.md`](rules/install.md) — install, browser/manual auth, the
  AskUserQuestion auth flow, PATH/permission troubleshooting, Codex specifics.
- `ARCHIVE/` — the original upstream Firecrawl docs (full CLI reference and the
  multi-path onboarding router) kept for reference; not needed for normal use.
