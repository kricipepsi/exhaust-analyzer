# Exhaust Analyzer - PythonAnywhere Deployment Guide

## Overview
This guide covers deploying the 5-Gas Exhaust Analyzer Flask app to PythonAnywhere and connecting your Namecheap domain.

## Prerequisites
- PythonAnywhere account (free tier works)
- Namecheap domain (BasicDNS)
- Your project files ready

---

## 1. PythonAnywhere Setup

### 1.1 Create a New Web App
1. Log in to PythonAnywhere
2. Go to **Web** tab → **Add a new web app**
3. Choose:
   - **Manual configuration** (not Django/Flask preset)
   - Python 3.11 (or latest available)
4. Note your **Web app URL** (e.g., `yourusername.pythonanywhere.com`)

### 1.2 Upload Files
Use the PythonAnywhere **Files** tab or SFTP to upload the entire `exhaust-analyzer` folder to:

```
/var/www/yourusername_pythonanywhere_com_wsgi.py
/var/www/yourusername_pythonanywhere_com/
    ├── app.py
    ├── requirements.txt
    ├── knowledge/
    ├── engine/
    ├── static/
    ├── templates/
    └── ... (all project files)
```

**Important:** The folder name should match your web app’s domain structure. If your web app is `yourusername.pythonanywhere.com`, the folder is typically `/var/www/yourusername_pythonanywhere_com/`.

### 1.3 Install Dependencies
Open a **Bash console** in PythonAnywhere and run:

```bash
cd /var/www/yourusername_pythonanywhere_com
pip3.11 install --user -r requirements.txt
```

If `requirements.txt` is minimal (only `flask>=3.0`), you may need to install additional dependencies mentioned in `app.py` imports:
- `pydantic` (if used)
- `numpy`, `pandas` (if used in knowledge base — actually not needed; see note below)

**Note:** The analyzer’s knowledge base is pure Python with only dataclasses. No heavy ML deps are required at runtime. Only Flask is essential. If you later add pandas/numpy for stats, install them too.

### 1.4 WSGI Configuration
In the **Web** tab, click **WSGI configuration file**. Replace its contents with:

```python
import sys
import os

# Add your project directory to the Python path
project_home = '/var/www/yourusername_pythonanywhere_com'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set Flask app
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'production'
# Optional: set a random secret key (or keep default for demo)
os.environ['SECRET_KEY'] = 'change-me-to-random-32-char-string'

from app import app as application  # noqa
```

**Replace** `yourusername_pythonanywhere_com` with your actual folder name.

Save the file.

---

## 2. Static Files (Optional but Recommended)

In the **Web** tab → **Static files**, add a mapping:

| URL | Directory |
|-----|-----------|
| `/static/` | `/var/www/yourusername_pythonanywhere_com/static/` |

Click **Reload** to apply.

---

## 3. Test the Deployment

1. In PythonAnywhere **Web** tab, click **Reload**.
2. Visit `https://yourusername.pythonanywhere.com`
3. You should see the 5‑Gas Analyzer form.

If you get an error, check the **Error log** in the Web tab.

Common fixes:
- Ensure `app.py` is at the project root (same level as `knowledge/`, `engine/`, `templates/`).
- Ensure `templates/index.html` exists.
- Verify Python path in WSGI matches your folder.

---

## 4. Connect Namecheap Domain

### 4.1 In PythonAnywhere
Get your app’s URL: `yourusername.pythonanywhere.com`

### 4.2 In Namecheap
1. Log in → **Domain List** → Manage your domain
2. Go to **Advanced DNS** → **Host Records**
3. Add a **CNAME** record:
   - Host: `www` (or `@` for root, but CNAME on root is not allowed; use A record if needed)
   - Value: `yourusername.pythonanywhere.com`
   - TTL: Automatic
4. (Optional) Add an **A record** for the naked domain if you want:
   - Host: `@`
   - Value: PythonAnywhere’s IP (check their docs for current IPs, e.g., `185.199.108.153` etc.) OR use a URL redirect to `www`.

Simpler: Use `www` CNAME only, and set default to redirect `@` to `www` in Namecheap.

5. Save changes. DNS propagation may take minutes to hours.

### 4.3 Verify
After propagation, `www.yourdomain.com` should load your analyzer.

---

## 5. Security & Production Notes

- Change the `SECRET_KEY` to a random 32‑character string (generate with `openssl rand -hex 32` or Python `secrets.token_hex(32)`).
- PythonAnywhere free tier has CPU limits; for heavier traffic consider a paid plan or Render.
- For HTTPS, PythonAnywhere provides a free cert automatically after you add your custom domain (requires A records pointing to their IPs). Follow PythonAnywhere’s “SSL” setup guide.

---

## 6. Embedding Widget (Optional)

If you want to embed the analyzer into another page via iframe, use:

```html
<iframe src="https://www.yourdomain.com/" width="100%" height="800" frameborder="0" style="border: 1px solid #ccc; border-radius: 8px;"></iframe>
```

Adjust height as needed.

---

## 7. Troubleshooting

**Error: `ImportError: No module named flask`**
→ Dependencies not installed. Run `pip3.11 install --user -r requirements.txt` again.

**Error: `TemplateNotFound`**
→ Ensure `templates/index.html` exists and the path is correct. Flask expects `templates/` in the app root.

**Error logs show 500**
→ Check that the WSGI `project_home` path is correct and that `app.py` is importable.

**Static files not loading**
→ Add static file mapping in PythonAnywhere Web tab.

---

That’s it. Your 5‑gas analyzer will be live and accessible via your domain.
