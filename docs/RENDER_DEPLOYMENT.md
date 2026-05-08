# Render Deployment Guide — 4D App

**Status:** Draft v0.1
**Date:** 2026-05-04
**Owner:** Mutolovsky

This guide explains how to take the **4D Petrol Diagnostic Engine** (currently sitting in `https://github.com/kricipepsi/4Dapp`) and deploy it to Render — analogous to how `exhaust-analyzer` is currently deployed at `https://exhaust-analyzer.onrender.com/`.

It covers V1 first (because the code that lives in `4Dapp` today **is** V1), then notes what changes when V2 is ready.

---

## 0. Quick orientation

| What you have today | Where it lives | URL |
|---|---|---|
| Old `exhaust-analyzer` | `github.com/kricipepsi/exhaust-analyzer` | `exhaust-analyzer.onrender.com` |
| New `4Dapp` repo | `github.com/kricipepsi/4Dapp` | not yet on Render |
| Local working copy | `C:\Users\muto\claude\4DApp\exhaust-analyzer-main\` | — |
| V2 design folder | `C:\Users\muto\claude\4DApp\v2\` | — |

The two GitHub repos are separate. Render lets you connect each to its own service — they will not collide.

---

## 1. Pre-flight: confirm the GitHub repo is in shape

Before connecting Render, the `4Dapp` repo must contain a runnable Streamlit app at the repo root (or in a subfolder Render can be pointed at).

Required files (V1 minimum):

```
4Dapp/
├── app.py                    # Streamlit entry point
├── requirements.txt          # Python deps
├── render.yaml               # (optional but recommended) Render service config
├── engine/                   # the diagnosis engine package
├── schema/                   # nodes.yaml / edges.yaml / thresholds.yaml
├── vref.db                   # (or fetched at build time — see §5.3)
└── tests/                    # not needed for deploy, but keep for CI
```

Verify locally:

```bash
cd C:\Users\muto\claude\4DApp\exhaust-analyzer-main
python -m streamlit run app.py
# should serve at http://localhost:8501
```

Then push to the new repo (instructions in §2).

---

## 2. Push the local code to `github.com/kricipepsi/4Dapp`

The local repo is already initialised (the workspace has a `.git/` folder and remote tracking).

### 2.1 Confirm remotes

```bash
cd C:\Users\muto\claude\4DApp\exhaust-analyzer-main
git remote -v
```

Expected output should include the push URL `https://github.com/kricipepsi/4Dapp.git`. If not:

```bash
git remote set-url origin https://github.com/kricipepsi/4Dapp.git
# OR if no origin exists yet:
git remote add origin https://github.com/kricipepsi/4Dapp.git
```

### 2.2 Branch hygiene

Render watches a specific branch (default `main`). Make sure that's the branch you push:

```bash
git status
git checkout main           # or `git checkout -b main` if it doesn't exist
git add .
git commit -m "v1: bring 4Dapp repo to deployment-ready state"
git push origin main
```

If the local branch is `master` and you want to rename to `main`:

```bash
git branch -m master main
git push -u origin main
git push origin --delete master    # only after Render and GitHub are pointed at main
```

### 2.3 Verify the GitHub side

Open `https://github.com/kricipepsi/4Dapp` in a browser. Confirm:

- `app.py` is at repo root.
- `requirements.txt` is present.
- `render.yaml` is present (recommended — see §3.2).

---

## 3. Hook the new repo to Render

Two ways: **Blueprint (uses `render.yaml`, fully reproducible)** or **Manual** (point-and-click in the dashboard). Blueprint is preferred.

### 3.1 Path A — Blueprint (recommended)

Make sure `4Dapp/render.yaml` looks like this (this is the existing V1 config, lightly adapted):

```yaml
services:
  - type: web
    name: 4dapp                     # this becomes the URL slug → 4dapp.onrender.com
    env: python
    plan: free                      # or `starter` / `standard` for paid tiers
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
    startCommand: |
      streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
    autoDeploy: true                # auto-redeploy on every push to main
    healthCheckPath: /              # Streamlit serves a 200 on the root
    envVars:
      - key: PYTHONUNBUFFERED
        value: "1"
      - key: STREAMLIT_SERVER_ENABLE_CORS
        value: "false"
      - key: STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION
        value: "true"
```

Then in Render dashboard:

1. Sign in at `https://dashboard.render.com/`.
2. Click **New** → **Blueprint**.
3. Click **Connect a repository** and authorise GitHub if you haven't already (GitHub's OAuth screen).
4. Select `kricipepsi/4Dapp`.
5. Render parses `render.yaml`, shows a preview ("1 web service: 4dapp"), click **Apply**.
6. Render creates the service, runs the build, and assigns a URL of the form `https://4dapp.onrender.com/` (or `https://4dapp-<hash>.onrender.com/` if the slug is taken).

The service goes from `building` → `live` in 3–8 minutes for the free plan.

### 3.2 Path B — Manual web-service setup

If you'd rather not commit a `render.yaml`:

1. Sign in to `dashboard.render.com`.
2. **New** → **Web Service**.
3. Click **Connect a repository**, select `kricipepsi/4Dapp` and the `main` branch.
4. Fill the form:
   - **Name:** `4dapp`
   - **Region:** pick the same one as `exhaust-analyzer` for consistency
   - **Branch:** `main`
   - **Root Directory:** leave blank if `app.py` is at root; otherwise set the subdir
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
   - **Plan:** `Free` (or paid)
5. Add the env vars from §3.1.
6. Click **Create Web Service**.

You can move to a Blueprint later by adding `render.yaml` and clicking **Sync** in the service settings.

### 3.3 The two services side by side

After deployment, your dashboard will list both:

| Service | Repo | URL | Status |
|---|---|---|---|
| `exhaust-analyzer` | `kricipepsi/exhaust-analyzer` | `exhaust-analyzer.onrender.com` | running V1 (legacy) |
| `4dapp` | `kricipepsi/4Dapp` | `4dapp.onrender.com` | running V1 (new) |

Each has its own settings page, build log, and env-var list. They do not share secrets.

---

## 4. Auto-deploy behaviour

With `autoDeploy: true` (Blueprint) or "Auto-Deploy: Yes" (manual), Render watches `main` and rebuilds on every push:

```bash
# locally
git add engine/v2/something.py
git commit -m "Add M0 DNA Core (Phase 3 milestone)"
git push origin main
# → Render starts a new build; old version stays live until new one passes health-check
```

You'll get a build log in real time on the service's dashboard page. Failed builds keep the previous version live.

To **pause** auto-deploy (e.g., during P5 schema migration when partial pushes would break the app):

- Service settings → **Auto-Deploy** → toggle off.
- Push to a `v2-dev` branch instead of `main` until P6 dual-run completes; then merge to `main`.

---

## 5. V1 → V2 deployment notes

V2 is an engine rebuild but **the deployment shape stays the same** (Streamlit app, same start command, same Python runtime). Three things that will change:

### 5.1 V2 schema lives in `schema/v2/`

`render.yaml` doesn't need to change — Streamlit picks up whatever the engine imports. But you should ensure the build copies the schema into the deploy bundle:

```yaml
buildCommand: |
  pip install --upgrade pip
  pip install -r requirements.txt
  # no need to copy schema; it's tracked in git already
```

Just `git add schema/v2/*.yaml` and push. Render takes the working tree as-is.

### 5.2 V2 will keep `vref.db` checked in (995 KB — under GitHub's 100 MB limit)

The current `exhaust-analyzer-main/.gitignore` excludes binary files; **make sure `vref.db` is NOT ignored** for the `4Dapp` repo:

```bash
# inspect
grep -n "vref" .gitignore || echo "not ignored — good"

# if ignored, untrack and remove the rule
sed -i '/vref/d' .gitignore
git rm -r --cached vref.db 2>/dev/null || true
git add vref.db .gitignore
git commit -m "Track vref.db so Render can find it at build time"
git push origin main
```

Alternative for V2: download `vref.db` at build time from a release artifact (good if it grows past 50 MB). Add to `render.yaml`:

```yaml
buildCommand: |
  pip install --upgrade pip
  pip install -r requirements.txt
  curl -L https://github.com/kricipepsi/4Dapp/releases/download/vref-v2/vref.db -o engine/v2/vref.db
```

But for now (995 KB), **just commit it**.

### 5.3 V2 will add a CI gate before deploys

Per `01_planning/ROADMAP_v2.md` P0, a GitHub Action (`.github/workflows/v2-layer2.yml`) will run the 400-case corpus on every PR and block merges that drop accuracy by > 1.0 pp.

This is independent of Render — Render still deploys on push to `main`, but PRs cannot merge to `main` if the gate fails. The two systems compose:

```
Developer pushes feature branch
  → opens PR
  → GitHub Actions runs Layer-1 + Layer-2 corpus
  → if green, PR can merge to main
  → on merge, Render auto-deploys main to 4dapp.onrender.com
```

You can attach Render preview environments (paid tier feature) so each PR gets its own URL — useful in P6 dual-run, deferred for now.

---

## 6. Custom domain (optional)

If you want `4d.kricipepsi.com` instead of `4dapp.onrender.com`:

1. Service settings → **Custom Domains** → **Add Custom Domain**.
2. Enter `4d.kricipepsi.com`.
3. Render shows a CNAME target like `4dapp.onrender.com` (or an A record for apex).
4. Add the CNAME at your DNS provider.
5. SSL provisions automatically (Let's Encrypt) within ~5 minutes of DNS propagation.

Same procedure as `exhaust-analyzer.onrender.com` if it has a custom domain.

---

## 7. Common issues + fixes

| Symptom | Cause | Fix |
|---|---|---|
| Build fails: "could not find a version that satisfies the requirement …" | `requirements.txt` lists a package not on PyPI (or a private one) | Pin versions; use only public packages. The V1 file lists `streamlit / plotly / pyyaml / pandas / pytest / vininfo` — all public. |
| Build succeeds but service shows "no open ports" | Streamlit not bound to `$PORT` | Confirm start command includes `--server.port $PORT --server.address 0.0.0.0` |
| Service starts but UI throws "FileNotFoundError: schema/nodes.yaml" | Schema not committed to repo | `git add schema/` and push |
| Service starts but Brettschneider returns NaN | Stale `vref.db` or missing data; not a deploy issue | Update `vref.db` and push |
| Build slow (>10 min) | Free tier is shared CPU; large numpy/pandas wheels | Consider `starter` plan for V2 |
| Service sleeps after 15 min idle (free tier) | Free tier behaviour by design | Upgrade to `starter` for always-on |
| `git push` fails with "remote contains work that you do not have locally" | Repo had an initial commit on GitHub that diverges from local | `git pull origin main --rebase` then re-push |
| GitHub rejects push because file > 100 MB | OPSI raw CSVs in repo | Add to `.gitignore`; use Git LFS for large binaries; or download at build time per §5.2 |

---

## 8. Sanity checklist before you click "deploy"

- [ ] `app.py` runs locally with `streamlit run app.py`.
- [ ] `requirements.txt` lists every import (no implicit deps).
- [ ] `vref.db` is committed (or fetched at build time).
- [ ] `schema/` files are committed.
- [ ] `.gitignore` does **not** exclude any required runtime asset.
- [ ] `render.yaml` (if used) is at repo root.
- [ ] Branch you intend to deploy from is `main` and is up to date.
- [ ] No secrets in the repo (env vars go through Render's secret store, not committed).
- [ ] Confirmed `4Dapp` is the right repo name (case-sensitive on Render's matching).

---

## 9. Decommissioning the old `exhaust-analyzer` service

Optional. Once `4dapp.onrender.com` is verified live:

1. **Don't delete immediately.** Keep `exhaust-analyzer.onrender.com` running for at least 30 days as a fallback.
2. After 30 days: Render dashboard → `exhaust-analyzer` service → **Settings** → **Suspend** (free) or **Delete** (irreversible).
3. The old GitHub repo can stay; archiving it (Settings → Archive) is reversible and signals "this is read-only".

---

## 10. References

- Render Streamlit deploy docs: https://render.com/docs/deploy-streamlit
- Render Blueprint reference: https://render.com/docs/blueprint-spec
- The current V1 `render.yaml`: see `07_deployment/render.yaml.v1_reference` in this folder.
- The V2 deployment plan in: `01_planning/ROADMAP_v2.md` §10.

---

*This guide is V1 today and stays valid for V2 with the §5 deltas. Update as Render's UI / pricing changes; archive at the end of v2.0 ship if the steps no longer match.*
