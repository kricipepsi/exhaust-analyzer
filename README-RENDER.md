# Deploy Exhaust Analyzer to Render

This guide covers deploying the 5‑Gas Exhaust Analyzer to Render and connecting your Namecheap domain.

---

## 1. Prepare Your Project

Ensure you have the following files in the `exhaust-analyzer` project root:

- `app.py`
- `requirements.txt`
- `Dockerfile`
- `render.yaml`
- `knowledge/`, `engine/`, `static/`, `templates/` (all project folders)

---

## 2. Sign Up on Render

1. Go to https://render.com and create an account (GitHub/GitLab/Bitbucket integration recommended).
2. Once logged in, go to **Dashboard** → **New +** → **Web Service**.

---

## 3. Create a New Web Service

You can connect a Git repository or upload files manually.

### Option A: Connect a Git Repository (recommended)
- Push the `exhaust-analyzer` folder to a GitHub repo.
- In Render: choose **Build and deploy from a Git repo**.
- Select your repository and branch.
- Render will auto-detect `render.yaml`.

### Option B: Manual Upload (if you don’t want Git)
- Choose **Build and deploy from a ZIP file**.
- Zip the entire `exhaust-analyzer` folder (include all files).
- Upload the ZIP in Render.
- Set **Build Command** to: (leave blank if using Dockerfile)
- Set **Start Command** to: (leave blank if using Dockerfile)

Since we use Docker, Render will build from the `Dockerfile`.

---

## 4. Configure the Service

- **Name**: `exhaust-analyzer` (or your preferred name)
- **Environment**: `Docker`
- **Plan**: Free (or paid for more resources)
- **Branch**: main (or your chosen branch)
- **Root Directory**: leave blank (your repo root is the Docker context)
- **Dockerfile Path**: `Dockerfile`
- **Health Check Path**: `/`
- **Environment Variables**:
  Render will use `render.yaml` to set:
  - `FLASK_APP=app.py`
  - `FLASK_ENV=production`
  - `SECRET_KEY` (auto‑generated)

You can add more if needed.

---

## 5. Deploy

Click **Create Web Service**. Render will build the Docker image and deploy.

Once done, you’ll get a URL like:
```
https://exhaust-analyzer.onrender.com
```

Test the URL – the analyzer should load.

---

## 6. Connect Your Custom Domain (Namecheap)

### 6.1 In Render Dashboard
- Go to your service → **Settings** → **Custom Domains** → **Add Custom Domain**.
- Enter `www.5-gasanalyzermot.com` (or the full domain).
- Render will show you a **CNAME target**, e.g.:
  ```
  exhaust-analyzer.onrender.com
  ```
   (sometimes it shows something like `exhaust-analyzer.rtn.py.foobar.com` – use exactly what Render gives you)

Copy that target.

### 6.2 In Namecheap
Log in → **Domain List** → Manage `5-gasanalyzermot.com` → **Advanced DNS** → **Host Records**:

**Delete old records:**
- Remove CNAME `www → parkingpage.namecheap.com.`
- Remove URL Redirect `@ → http://www.5-gasanalyzermot.com/`

**Add new records:**

1. **CNAME** for `www`:
   - **Host**: `www`
   - **Value**: *Paste the Render CNAME target* (e.g., `exhaust-analyzer.onrender.com`)
   - **TTL**: `Automatic`

2. **Optional – naked domain** (`5-gasanalyzermot.com`):
   - Render does not provide static IPs. To support the root domain, add an **A record** pointing to one of Render’s current IPs (check Render docs for latest; they may change).
   - Or simpler: add a **URL Redirect**:
     - **Host**: `@`
     - **Value**: `https://www.5-gasanalyzermot.com`
     - **Type**: `301 (Permanent)`

**Save changes.**

### 6.3 Wait for DNS
Propagation usually minutes.

---

## 7. HTTPS (SSL)

Render automatically provisions a free **SSL certificate** via Let’s Encrypt for your custom domain after DNS points correctly. It may take a few minutes after DNS propagation.

Once ready, both `http` and `https` will work (Render redirects to https automatically).

---

## 8. Verify

Open `https://www.5-gasanalyzermot.com` – you should see the 5‑Gas Analyzer.

Test with sample data to confirm it runs.

---

## 9. Embedding on Your Site

Use an iframe on your pages:

```html
<iframe src="https://www.5-gasanalyzermot.com/" width="100%" height="800" frameborder="0" style="border:1px solid #ddd; border-radius:8px;"></iframe>
```

Adjust `height` as needed.

---

## 10. Troubleshooting

**“Application Error” on Render**
- Check Render logs: service → **Logs** tab.
- Ensure `Dockerfile` copies all project files and runs `python app.py` or uses `gunicorn`.
- Verify `requirements.txt` includes `Flask>=3.0`.

**Domain not pointing**
- Double-check Namecheap CNAME target matches exactly what Render provided.
- Ensure old records removed.

**SSL not active**
- Wait up to 30 min after DNS points. Ensure no A records conflicting with CNAME for `www`. Root domain can be a redirect to `www`.

---

That’s it. Your analyzer will be live on your domain.
