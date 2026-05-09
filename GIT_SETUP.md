# Git Setup Instructions

The repo is initialised and has its initial commit. Due to a sandbox filesystem
restriction, the `.git/config.lock` file cannot be deleted from within the
build environment. Run these commands once on your local machine to complete
the git setup and push to GitHub:

```bash
cd C:\Users\muto\claude\4DApp\v2\4D-Diagnostic-Engine-v2

# Remove the stale lock file
del .git\config.lock

# Set remote and push
git remote set-url origin https://github.com/kricipepsi/v2-diagnostic-app.git
git branch -M main
git push -u origin main
```

The initial commit contains: repo scaffold, corpus v6 baseline (281 cases),
V1 schema reference, master guides, pyproject.toml, requirements.txt.
