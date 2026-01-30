# Deploy to Vercel

## Option 1: Deploy from Vercel Dashboard (recommended)

1. **Push your code to GitHub** (already done: https://github.com/TheShakSpace/Samyak).

2. **Go to [vercel.com](https://vercel.com)** and sign in (GitHub).

3. **Import project**
   - Click **Add New…** → **Project**
   - Select **TheShakSpace/Samyak** (or your fork)
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `./` (leave default)
   - Click **Deploy**

4. **Environment variables** (after first deploy, go to Project → Settings → Environment Variables):
   - `NEXT_PUBLIC_GEMINI_API_KEY` – for the Voice Agent (frontend chatbot). Get key: https://aistudio.google.com/apikey
   - `NEXT_PUBLIC_API_URL` – (optional) your backend URL in production, e.g. `https://your-backend.railway.app` or `https://your-backend.onrender.com`. If not set, `/api/*` rewrites go to `http://localhost:8000` (only works in dev).

5. **Redeploy** after adding env vars (Deployments → ⋮ → Redeploy).

Your app will be at `https://samyak-xxx.vercel.app` (or your custom domain).

---

## Option 2: Deploy with Vercel CLI

1. **Fix npm cache** (if you see EPERM):
   ```bash
   sudo chown -R $(whoami) ~/.npm
   ```

2. **Install and login:**
   ```bash
   npm i -g vercel
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd "/Users/dhruv_insights/Documents/Hackathons Project/samyak"
   vercel
   ```
   For production: `vercel --prod`

4. **Set env vars** in [Vercel Dashboard](https://vercel.com/dashboard) → your project → Settings → Environment Variables (same as above).

---

## Backend in production

The frontend can run **without a backend** if you set `NEXT_PUBLIC_GEMINI_API_KEY` (Voice Agent works as a frontend chatbot).

To use **tasks, hours, productivity** in production, deploy the backend (e.g. Railway, Render, Fly.io) and set `NEXT_PUBLIC_API_URL` in Vercel to that URL.
