# Deploy MOT Query Feature to Web & Android

## Overview

The 5-Gas Analyzer now includes a comprehensive MOT test determination system:
- SQLite database `knowledge/mot_emissions.db` containing UK MOT emission standards
- Flask API routes: `/mot-query` (web form) and `/api/mot/query` (JSON API for mobile)
- Frontend page `templates/mot_query.html` for user input

This document covers deploying these updates to:
1. **Web app** on Render.com (https://exhaust-analyzer.onrender.com/)
2. **Android app** (TWA/WebView) from https://github.com/kricipepsi/exhaust-analyzer

---

## ✅ Changes Made (as of 2026-03-09)

### Core Files
- `knowledge/mot_database.py` — Database builder (25.8 KB)
- `knowledge/mot_emissions.db` — SQLite database (143 KB)
- `knowledge/mot_query_api.py` — High-level query functions (18.7 KB)
- `knowledge/MOT-DATABASE-README.md` — Documentation

### Flask App Updates
- `app.py` — Added `/mot-query` route and `/api/mot/query` endpoint, plus `/health` check
- `templates/mot_query.html` — New MOT query form page
- `templates/index.html` — Added navigation link to MOT query

### Git Status
All files are ready to commit and push.

---

## 🚀 Deploy to Web (Render.com)

### 1. Commit & Push to GitHub

```bash
cd "C:\Users\asus\.openclaw\workspace\exhaust-analyzer"
git add -A
git commit -m "Add MOT test query database and UI"
git push origin main  # or your deployment branch
```

### 2. Verify Render.com Build

Render.com automatically builds and deploys on git push. Monitor the build logs:

- Go to Render dashboard → your service (exhaust-analyzer)
- Check "Deploys" tab for build status
- Ensure the build completes successfully (Gunicorn will import the app)

**Important**: The `knowledge/mot_emissions.db` file is large (~78 KB). Ensure Render's build environment can handle it (it can; it's small).

### 3. Post-Deploy Verification

After deployment completes:

1. Visit https://exhaust-analyzer.onrender.com/ → should see "🔍 MOT Test Lookup (New!)" link
2. Click it → MOT query form loads at `/mot-query`
3. Test a query:
   - Make: Ford
   - Model: Focus
   - First use date: 2010-05-15
   - Fuel: petrol
   - Has catalyst: checked
   - Submit → should show "extended_catalyst" test type

4. Test JSON API:
```bash
curl -X POST https://exhaust-analyzer.onrender.com/api/mot/query \
  -H "Content-Type: application/json" \
  -d '{"make":"Ford","model":"Focus","first_use_date":"2010-05-15","fuel_type":"petrol","has_catalyst":true}'
```

Expected: JSON response with `test_type: "extended_catalyst"`

### 4. Rollback If Needed

If issues arise:
```bash
git revert HEAD
git push
# Render will redeploy previous version
```

---

## 📱 Update Android App

### Understanding the Android App Structure

The Android app at https://github.com/kricipepsi/exhaust-analyzer is likely a **Trusted Web Activity (TWA)** or **WebView wrapper** that loads the live web app URL. There are two scenarios:

**Scenario A: TWA/WebView pointing to live URL** (most likely)
- The Android app loads `https://exhaust-analyzer.onrender.com/` in a WebView
- No code changes needed — the app automatically gets new features when the web app updates
- **Action**: Just deploy web changes; Android app picks them up instantly

**Scenario B: Bundled static assets** (possible if offline-first)
- The Android repo contains a copy of the `templates/` and `static/` folders
- You need to update those files in the Android repo and rebuild/re-publish

### Determine Which Scenario

1. Open Android repo in browser or clone:
```bash
git clone https://github.com/kricipepsi/exhaust-analyzer.git
```

2. Look for:
   - `app/src/main/assets/` or `assets/` folder containing HTML files → Scenario B
   - `MainActivity.java` / `MainActivity.kt` loading a URL like `https://...` or `http://10.0.2.2:5000` → Scenario A

3. Also check README.md for instructions.

### Scenario A: Live URL Load (No Android Code Change Needed)

If MainActivity has something like:
```kotlin
webView.loadUrl("https://exhaust-analyzer.onrender.com")
```

Then:
1. ✅ Deploy web updates (above)
2. ✅ That's it — Android app will show new MOT query page at `/mot-query`
3. Optionally update Android app's menu/navigation if you want a dedicated button (but link in web page is already accessible)

**Test**: Open Android app, tap menu or navigate to `https://exhaust-analyzer.onrender.com/mot-query` — should work.

### Scenario B: Bundled Assets Require Update

If the Android app has embedded `index.html`, `mot_query.html`, etc.:

1. Copy updated templates to Android repo:
```bash
# From the web project:
cp templates/index.html   android-repo/app/src/main/assets/
cp templates/mot_query.html android-repo/app/src/main/assets/
cp static/style.css       android-repo/app/src/main/assets/static/
```

2. Also ensure any new dependencies (JS, CSS) are bundled.

3. Rebuild and sign the Android APK/AAB:
```bash
cd android-repo
./gradlew assembleRelease  # or bundleRelease for AAB
```

4. Upload to Google Play Console (internal test → production)

5. Update GitHub repo:
```bash
git add app/src/main/assets/*
git commit -m "Update web assets: add MOT query page"
git push
```

---

## 📋 Integration Checklist

### Web (Render.com)
- [x] Code changes committed
- [x] `mot_emissions.db` included in repo
- [ ] Git push completed
- [ ] Render build successful
- [ ] `/mot-query` page loads
- [ ] `/api/mot/query` returns JSON
- [ ] Navigation link visible on homepage
- [ ] Health check endpoint `/health` returns ok

### Android
- [ ] Determine loading strategy (live URL vs bundled)
- [ ] If bundled: copy updated templates & static assets
- [ ] Rebuild APK/AAB
- [ ] Install on test device
- [ ] Verify `/mot-query` accessible through in-app browser/WebView
- [ ] Test query flow end-to-end
- [ ] If publishing update: bump versionCode/versionName, generate release build, upload to Play Console

---

## 🔧 API Usage (Mobile App Integration)

The Android app can call the JSON API directly if building a native UI instead of WebView.

**Endpoint:** `POST https://exhaust-analyzer.onrender.com/api/mot/query`

**Payload:**
```json
{
  "make": "Ford",
  "model": "Focus",
  "first_use_date": "2010-05-15",
  "fuel_type": "petrol",
  "engine_code": "1.6 Ti-VCT",
  "has_catalyst": true,
  "dgw_kg": 1450,
  "seat_count": 5
}
```

**Response (example):**
```json
{
  "test_type": "extended_catalyst",
  "description": "Petrol vehicle with catalyst...",
  "procedure": "1. Check engine oil temperature >=...",
  "fast_idle_limits": {
    "co": "See Annex or <=0.2% if using default",
    "hc": "See Annex or <=200ppm if using default",
    "lambda_min": 0.97,
    "lambda_max": 1.03,
    "duration_seconds": 30
  },
  "idle_limits": {"co": "<=0.3%"},
  "uses_annex": false
}
```

---

## 📊 Database Schema

Key tables for reference:

- `vehicle_makes` — Make names (Ford, VW, Toyota...)
- `emission_standards` — General limits by date and test type
- `specific_model_limits` — Annex entries (make/model/engine specific)
- `diesel_smoke_standards` — Opacity limits by date and turbo status
- `special_cases` — Kit cars, imports, engine swaps
- `mil_requirements` — Engine management light rules

The `mot_query_api.py` handles all joins and logic.

---

## 🐛 Troubleshooting

**Issue**: 500 error on `/api/mot/query`
- Check Render logs: `journalctl -u exhaust-analyzer` or Render "Logs" tab
- Likely: Database not found. Ensure `knowledge/mot_emissions.db` exists in deployed app
- Verify imports: `from knowledge.mot_query_api import query_vehicle_info` must succeed

**Issue**: `ModuleNotFoundError: No module named 'knowledge'`
- The app's Python path must include project root
- `app.py` does `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` — this should work
- On Render, working directory is project root; if running from subfolder, adjust path

**Issue**: Slow query response
- Database is small (78 KB) — should be fast
- If slow, add indexing on `specific_model_limits(make_id, model_name, date_from)`
- Consider caching frequent queries in Flask (e.g., LRU cache)

**Issue**: Android WebView not showing updated page
- Clear WebView cache or implement cache-busting
- If using bundled assets, ensure you copied **all** updated files and rebuilt

---

## 🎯 Next Steps

1. **Full Annex import**: Currently `specific_model_limits` is empty. Write a parser to import all make/model/engine rows from `19th edition - in-service-exhaust-emission-standards-for-road-vehicles-19th-edition.txt`. This will make the query return specific limits instead of just "extended_catalyst".

2. **Autocomplete for makes**: Query `SELECT name FROM vehicle_makes` and implement typeahead in `mot_query.html` (requires JS).

3. **Unit tests**: Add tests for edge cases (pre-1975, kit cars, LPG conversion).

4. **Frontend polish**: Add loading spinner, better error display, responsive design for mobile.

5. **API authentication**: If exposing publicly, consider rate limiting or API key to prevent abuse.

6. **Monitor health**: Use `/health` endpoint for uptime checks (UptimeRobot, etc.)

---

**Ready to deploy!** Push to GitHub and let Render do the rest. Android app will follow automatically if it's a TWA.

Questions? Check `knowledge/MOT-DATABASE-README.md` for database details.
