# 🚀 Deployment Guide - Free Hosting

This guide will help you deploy your Adaptive Learning AI on **100% FREE** hosting platforms.

## 🏆 Best Free Hosting Options (Ranked)

### 1. 🥇 Render (RECOMMENDED)

**Best for**: Persistent storage, reliability, ease of use

**Free Tier Includes**:
- ✅ 750 hours/month (enough for 24/7)
- ✅ 1 GB persistent disk storage (PERFECT for learning AI!)
- ✅ Auto-deploy from GitHub
- ✅ Custom domains
- ✅ SSL certificates

**Deployment Steps**:

1. **Prepare Your Code**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Render**
   - Visit [render.com](https://render.com)
   - Click "Sign Up" and connect GitHub

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Select your repository
   - Configure:
     ```
     Name: adaptive-learning-ai
     Environment: Node
     Build Command: npm install && npm run install-all && npm run build
     Start Command: npm start
     Instance Type: Free
     ```

4. **Add Persistent Disk** (CRITICAL for learning!)
   - After service is created, go to "Disks" tab
   - Click "Add Disk"
   - Name: `ai-data`
   - Mount Path: `/opt/render/project/src/data`
   - Size: 1 GB
   - Click "Save"

5. **Deploy**
   - Click "Manual Deploy" → "Deploy latest commit"
   - Wait 5-10 minutes for build
   - Your AI will be live! 🎉

**Your URL**: `https://adaptive-learning-ai-xxxx.onrender.com`

**⚠️ Important**: Free tier sleeps after 15 min of inactivity. First request after sleep takes ~30 seconds.

---

### 2. 🥈 Railway

**Best for**: Quick deployment, modern interface

**Free Tier Includes**:
- ✅ $5 credit/month (enough for small apps)
- ✅ Persistent storage
- ✅ Auto-deploy
- ✅ Easy to use

**Deployment Steps**:

1. **Prepare Your Code**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Railway**
   - Visit [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Deploy**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Node.js!

4. **Configure** (optional)
   - Click your service → "Variables"
   - Add if needed:
     ```
     NODE_ENV=production
     PORT=5000
     ```

5. **Generate Domain**
   - Go to "Settings" → "Generate Domain"
   - Your AI is live! 🎉

**Your URL**: `https://your-app.up.railway.app`

---

### 3. 🥉 Replit (Easiest - No Git Required!)

**Best for**: Absolute beginners, no terminal knowledge needed

**Free Tier Includes**:
- ✅ Unlimited public Repls
- ✅ Built-in code editor
- ✅ Instant deployment
- ✅ No Git needed!

**Deployment Steps**:

1. **Go to Replit**
   - Visit [replit.com](https://replit.com)
   - Sign up (free)

2. **Create Repl**
   - Click "Create Repl"
   - Choose "Import from GitHub"
   - Paste your repository URL
   - OR manually upload files

3. **Install Dependencies**
   - Replit will auto-detect `package.json`
   - Click "Run" - it handles everything!

4. **Keep It Alive** (Important!)
   - Free Repls sleep when inactive
   - Use [UptimeRobot](https://uptimerobot.com) (free) to ping your Repl every 5 minutes

**Your URL**: `https://your-repl-name.your-username.repl.co`

**Keeping it Running 24/7** (Free):
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Add new monitor
3. Type: HTTP(s)
4. URL: Your Repl URL
5. Interval: 5 minutes

---

### 4. 🌟 Vercel + MongoDB Atlas

**Best for**: Scalability (but more complex setup)

**Free Tier Includes**:
- ✅ Unlimited deployments
- ✅ Auto-scaling
- ✅ Global CDN
- ⚠️ Serverless (needs external database)

**Deployment Steps**:

1. **Setup MongoDB Atlas** (For persistent data)
   - Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Create free account
   - Create free cluster (M0)
   - Create database user
   - Whitelist all IPs: `0.0.0.0/0`
   - Get connection string

2. **Modify Code for MongoDB** (you'll need to update the AI engine)
   ```javascript
   // Install: npm install mongodb
   // Replace JSON file storage with MongoDB
   ```

3. **Deploy to Vercel**
   ```bash
   npm i -g vercel
   vercel login
   vercel
   ```

4. **Add Environment Variables**
   - Go to Vercel dashboard
   - Select your project → Settings → Environment Variables
   - Add: `MONGODB_URI=your_connection_string`

**Your URL**: `https://your-project.vercel.app`

---

### 5. 💚 Heroku Alternative: Fly.io

**Best for**: Heroku users looking for free alternative

**Free Tier Includes**:
- ✅ 3 shared-cpu VMs
- ✅ 3GB persistent storage
- ✅ 160GB data transfer

**Deployment Steps**:

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Launch App**
   ```bash
   fly launch
   ```
   - Follow prompts
   - Choose region near you
   - Don't deploy yet

4. **Create Volume** (for persistent data)
   ```bash
   fly volumes create ai_data --size 1
   ```

5. **Add to fly.toml**
   ```toml
   [mounts]
     source = "ai_data"
     destination = "/data"
   ```

6. **Deploy**
   ```bash
   fly deploy
   ```

**Your URL**: `https://your-app.fly.dev`

---

## 📊 Comparison Table

| Platform | Setup Difficulty | Persistent Storage | Auto-Sleep | Best For |
|----------|------------------|-------------------|------------|----------|
| **Render** | ⭐⭐ Easy | ✅ Yes (1GB) | ⚠️ Yes (15 min) | **BEST OVERALL** |
| **Railway** | ⭐ Very Easy | ✅ Yes | ❌ No | Quick deploys |
| **Replit** | ⭐ Easiest | ✅ Yes | ⚠️ Yes | Absolute beginners |
| **Vercel** | ⭐⭐⭐ Hard | ⚠️ Needs external DB | ❌ No | Scalability |
| **Fly.io** | ⭐⭐⭐ Medium | ✅ Yes (3GB) | ❌ No | Advanced users |

---

## 🎯 Quick Start (Render - Recommended)

The absolute fastest way to get your AI online:

```bash
# 1. Initialize git
git init
git add .
git commit -m "Initial commit"

# 2. Push to GitHub
# (Create new repo on github.com first)
git remote add origin https://github.com/yourusername/adaptive-ai.git
git push -u origin main

# 3. Go to render.com
# 4. Click "New" → "Web Service"
# 5. Connect GitHub repo
# 6. Use these settings:
#    Build: npm install && npm run install-all && npm run build
#    Start: npm start
# 7. After deploy, add disk:
#    Disks → Add Disk → Mount at /opt/render/project/src/data
# 8. Done! 🎉
```

---

## 🛠️ Troubleshooting

### Data Not Persisting

**Problem**: AI forgets everything after restart

**Solutions**:
- **Render**: Make sure you added a persistent disk
- **Railway**: Data persists automatically
- **Replit**: Data persists in your Repl
- **Vercel**: Must use external database (MongoDB Atlas)

### App Sleeps When Inactive

**Problem**: First request takes 30+ seconds

**Solution**: Use a free uptime monitor
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Create free account
3. Add HTTP(s) monitor with your URL
4. Set interval to 5 minutes
5. Your app stays awake! ⏰

### Build Fails

**Common issues**:
```bash
# Missing dependencies
npm run install-all

# Port issues
# Make sure server.js uses process.env.PORT

# Build command issues
# Use: npm install && npm run install-all && npm run build
```

### "Module not found" errors

```bash
# Delete node_modules and reinstall
rm -rf node_modules client/node_modules
npm run install-all
```

---

## 💰 Cost Summary

All options above are **100% FREE** for small-scale use:

- ✅ **Render**: Free forever (with sleep mode)
- ✅ **Railway**: $5/month credit (enough for small apps)
- ✅ **Replit**: Free forever (public Repls)
- ✅ **Vercel**: Free forever (with limits)
- ✅ **Fly.io**: Free tier (3 VMs)

---

## 🎉 You're Ready!

Choose your platform and get your AI online in minutes. I recommend **Render** for the best balance of ease and features.

Your AI will be accessible worldwide at your custom URL! 🌍

Need help? Check the main [README.md](README.md) for more details.
