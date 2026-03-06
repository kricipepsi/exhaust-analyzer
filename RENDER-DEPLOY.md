# Deploy to Render

This guide covers deploying the 5-Gas Exhaust Analyzer to Render.com.

## Prerequisites

- GitHub repository connected to Render
- Render account (free tier available)

## Steps

### 1. Create a New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository:
   - Repository: `github.com/kricipepsi/exhaust-analyzer`
   - Name: `exhaust-analyzer` (or your choice)
4. Environment: **Python 3**
5. Region: Choose closest to your users
6. Branch: `main` (or your preferred branch)
7. Build Command: `pip install -r requirements.txt`
8. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60`
9. Plan: **Free** (or paid for more resources)

### 2. Environment Variables

Render automatically sets these from `render.yaml` if you use the "Deploy from YAML" option. If using manual setup, add:

- `FLASK_APP` = `app.py`
- `FLASK_ENV` = `production`
- `SECRET_KEY` = (Render will auto-generate if you leave blank)

### 3. Deploy from YAML (Recommended)

Instead of manual setup, you can deploy using the `render.yaml` file:

1. In Render dashboard, click **New +** → **Blueprint**
2. Connect your repository
3. Render will detect `render.yaml` and create the service automatically
4. Click **Apply** to create the web service

### 4. Wait for Deployment

- Build takes ~2-5 minutes on free tier
- Render will assign a URL like: `https://exhaust-analyzer.onrender.com`
- Once deployed, check the health endpoint (`/`) to verify it's running

### 5. Verify PWA Assets

1. Visit your Render URL
2. Open Chrome DevTools → Application
3. Confirm:
   - Manifest loads (`/static/manifest.json`)
   - Service Worker is active
   - Icons are accessible
4. Test the analyzer form to ensure backend works

### 6. Update Bubblewrap Configuration

When initializing Bubblewrap, use your Render URL:

```bash
bubblewrap init --manifest=https://exhaust-analyzer.onrender.com/manifest.json
```

Replace with your actual Render domain.

### 7. Note on Free Tier

- Render free services **sleep after 15 minutes of inactivity**
- First request after sleep may take ~30 seconds (cold start)
- For production mobile app, consider upgrading to paid plan ($7+/month) to keep service always awake
- Alternatively, use a cron job to ping the app every 10 minutes (not recommended for Play Store compliance)

### 8. Custom Domain (Optional)

You can use a custom domain instead of the onrender.com subdomain:

1. Add domain in Render dashboard → Custom Domains
2. Update DNS with CNAME to `your-app.onrender.com`
3. SSL is auto-managed by Render

### 9. Important: AdSense Compatibility

- AdSense works fine on Render (HTTPS)
- Ensure your AdSense code uses the correct `ca-pub-...` and `data-ad-slot`
- Test that ads display on the live Render URL before building Android app

### 10. After Deployment

Once verified:
1. Run Bubblewrap commands
2. Build Android AAB
3. Upload to Google Play Store
4. Monitor Render logs for any issues

---

**Need help?** Render docs: https://render.com/docs
