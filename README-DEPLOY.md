# Exhaust Analyzer - Deployment Guide

This guide explains how to deploy the 5-Gas Exhaust Analyzer in production and how to embed the widget on external websites.

## 📦 What's Included

- `Dockerfile` – Production container image using Gunicorn
- `nginx.conf` – Optional reverse proxy configuration
- `.env.example` – Environment variable template
- `start.sh` – Startup script for non-Docker deployment
- `widget.html` – Embeddable widget for external sites
- `README-DEPLOY.md` – This file

The core application files (`app.py`, `engine/`, `knowledge/`, `templates/`, `static/`) should be present in your project directory alongside these deployment files.

---

## 🚀 Quick Start (Docker)

1. **Prerequisites**: Docker and Docker Compose installed.

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env and set a strong SECRET_KEY
   ```

3. **Build the image**:
   ```bash
   docker build -t exhaust-analyzer:latest .
   ```

4. **Run the container**:
   ```bash
   docker run -d \
     --name exhaust-analyzer \
     --env-file .env \
     -p 5000:5000 \
     --restart unless-stopped \
     exhaust-analyzer:latest
   ```

5. **Access**: Open `http://localhost:5000` in your browser.

6. **Test widget**: Visit `http://localhost:5000/static/widget.html` (if you copied widget.html into the static folder) or serve it from your web server.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default / Required |
|----------|-------------|--------------------|
| `FLASK_APP` | Flask entry point | `app.py` |
| `FLASK_ENV` | Environment (`production` recommended) | `production` |
| `SECRET_KEY` | Flask secret for session/flash messages | **Required, change!** |
| `GUNICORN_WORKERS` | Number of worker processes | `2` |
| `GUNICORN_TIMEOUT` | Worker timeout (seconds) | `60` |
| `GUNICORN_BIND` | Bind address | `0.0.0.0:5000` |

Generate a strong secret key:
```bash
openssl rand -hex 32
```

### Using `start.sh` (Non-Docker)

For direct deployment on a VM or bare server:

```bash
# 1. Install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# edit .env

# 3. Start the service
./start.sh 5000
```

Consider using a process manager (systemd, supervisor) to keep it running.

---

## 🔧 Reverse Proxy with Nginx (Optional)

If you want to serve the analyzer on port 80/443 with HTTPS:

1. Install Nginx.
2. Copy `nginx.conf` to `/etc/nginx/sites-available/exhaust-analyzer` and symlink to `sites-enabled`.
3. Update `server_name` to your domain.
4. (Optional) Uncomment the `location /static/` block and adjust the path if you serve static files directly.
5. Test config: `nginx -t`.
6. Reload: `systemctl reload nginx`.

You can also add SSL with Certbot.

---

## 🎨 Embeddable Widget

The `widget.html` file provides a ready-to-embed version of the analyzer. It displays the tool inside an iframe and includes demo buttons for testing.

### Deployment Options

**Option A: Iframe Embed (recommended)**

Host `widget.html` on the same domain as the analyzer (e.g., `https://analyzer.example.com/static/widget.html`) and embed it in external pages:

```html
<iframe src="https://analyzer.example.com/static/widget.html"
        width="100%" height="950" frameborder="0"
        title="Exhaust Analyzer">
</iframe>
```

**Option B: Direct Include**

You can also copy the contents of `widget.html` into your page, but ensure the iframe `src` points to the analyzer's root URL. This method allows CSS integration with your site.

### Sample Data Buttons

The widget includes buttons ("Rich Mixture", "Lean Condition", "Misfire", "Normal") that automatically fill the analyzer form and submit it. **These only work when the widget is served from the same origin as the analyzer** (i.e., both on the same domain). This is typically true if you host `widget.html` alongside the Flask app (e.g., placed in the `static/` folder). Cross-origin embedding will still display the analyzer, but the buttons will be disabled due to browser security policies.

### Styling

The widget uses responsive CSS that adapts to mobile and desktop. You can customize colors by editing the `:root` variables in `widget.html`.

---

## 🔒 Security Considerations

- Change the `SECRET_KEY` to a random, high-entropy string in production.
- If the analyzer is publicly accessible, consider adding rate limiting (e.g., via nginx) to prevent abuse.
- The current Flask app does not require authentication. If you need to restrict access, add HTTP basic auth or an API key check in `app.py`.
- Enable HTTPS in production (use Nginx + Let's Encrypt).

---

## 🐛 Troubleshooting

**Gunicorn not found**: Ensure you installed `gunicorn` (`pip install gunicorn`). The `start.sh` falls back to `python app.py` if gunicorn is missing (development only).

**Static files not loading**: In Docker, ensure `templates/` and `static/` are copied into the image (the Dockerfile does this). If you change the folder structure, update the Dockerfile accordingly.

**Widget buttons not working**: The widget uses JavaScript to access the iframe's DOM. This only works if the iframe is same-origin. Check browser console for errors.

**Cannot import engine/assessor**: The Flask app expects the project structure with `engine/` and `knowledge/` directories. Maintain relative imports.

---

## 📊 Monitoring & Logs

- **Docker logs**: `docker logs exhaust-analyzer`
- **Gunicorn access/error logs**: By default printed to stdout; configure with `--access-logfile` and `--error-logfile` in the Dockerfile's CMD if needed.
- **Health check**: Access `/` and verify HTTP 200.

---

## 📝 Notes

- This analyzer is designed for petrol engines from the 1990s–2000s. It provides diagnostic suggestions only, not a substitute for professional mechanic judgment.
- Dependencies are minimal: Flask (and optionally Flask-CORS if you modify the app to expose a public API).
- The engine and knowledge modules are pure Python and require no external services.

---

## 🛠️ Customization

- To modify diagnostic rules, edit `knowledge/knowledge_base.py`.
- To change the UI, edit `templates/index.html` and `static/style.css`. The widget inherits the app's UI inside the iframe.

---

**Enjoy your deployed Exhaust Analyzer!** For issues, refer to the main project README.
