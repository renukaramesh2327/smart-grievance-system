# 🚀 Deploy Smart Grievance System to GitHub & Run Online

## Option 1: Push to GitHub

### 1. Create a new repository on GitHub
- Go to [github.com/new](https://github.com/new)
- Name: `smart-grievance-system`
- Choose Public, don't initialize with README

### 2. Push your code
```bash
cd "/Users/santhakumar/Desktop/smart greviance system"

# If not already a git repo
git init

# Add all files
git add .
git commit -m "Smart Grievance System - ready for deployment"

# Add your GitHub repo (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/smart-grievance-system.git

# Push to main
git branch -M main
git push -u origin main
```

---

## Option 2: Deploy on Render.com (Free)

Render hosts the full Flask app with backend. **Free tier** includes 750 hours/month.

### Step 1: Connect GitHub to Render
1. Go to [render.com](https://render.com) and sign up (free)
2. Click **New** → **Web Service**
3. Connect your GitHub account and select `smart-grievance-system` repo

### Step 2: Configure the service
| Setting | Value |
|---------|-------|
| **Name** | smart-grievance-system |
| **Region** | Oregon (or nearest) |
| **Branch** | main |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn "backend.app:create_app()" --bind 0.0.0.0:$PORT` |

### Step 3: Environment variables (optional)
Add in Render Dashboard → Environment:
| Key | Value |
|-----|-------|
| `FLASK_ENV` | production |
| `SECRET_KEY` | (generate a random 32-char string) |
| `DEMO_EMAIL_MODE` | true |

### Step 4: Deploy
Click **Create Web Service**. Render will build and deploy. Your app will be live at:
```
https://smart-grievance-system-xxxx.onrender.com
```

### Step 5: Seed the database (first time)
After first deploy, run the seed script locally against your deployed URL, or add a one-time setup. For demo, you can register a new user and create an admin via the database.

**Quick seed via Render Shell:**
1. In Render Dashboard → Your Service → **Shell**
2. Run: `python -m backend.seed`

---

## Option 3: Deploy with Render Blueprint

If you have `render.yaml` in your repo:

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **Blueprint**
3. Connect your GitHub repo
4. Render will detect `render.yaml` and create the service automatically

---

## Option 4: Run locally (development)

```bash
cd "/Users/santhakumar/Desktop/smart greviance system"
pip install -r requirements.txt
python -m backend.seed   # Create admin/officer accounts
python run.py
```

Open **http://localhost:8000**

**Test accounts:**
- Admin: admin@grievance.gov / admin123
- Officer: electricity@grievance.gov / officer123
- Citizen: citizen@example.com / citizen123

---

## GitHub Pages (Static demo)

The `docs/` folder is a **static demo** (no backend). The full app requires Render or similar.

**Option A — GitHub Actions (recommended):**
1. Repo → Add file → Create new file → name: `.github/workflows/gh-pages.yml`
2. Copy content from the `gh-pages.yml` file in this repo
3. Repo → Settings → Pages → Source: **GitHub Actions**

**Option B — Deploy from branch:**
1. Repo → Settings → Pages → Source: Deploy from branch
2. Branch: main, Folder: /docs

**Note:** Workflow files require PAT with `workflow` scope to push. Add via GitHub web UI if needed.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails | Ensure `requirements.txt` has all deps; check Python 3.11 |
| 502 Bad Gateway | Increase start timeout in Render; check `/health` endpoint |
| Database errors | Free tier uses SQLite (ephemeral); for persistent data add PostgreSQL |
| CORS errors | App uses same-origin; ensure frontend and API are same domain |
