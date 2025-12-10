# 🚀 Quick Start Guide

Get your Adaptive Learning AI running in 3 minutes!

## Local Development (Test it first!)

### Step 1: Install Everything
```bash
npm run install-all
```

### Step 2: Start the Backend
Open a terminal and run:
```bash
npm run dev
```
You should see: `🚀 Adaptive Learning AI server running on port 5000`

### Step 3: Start the Frontend
Open a NEW terminal and run:
```bash
cd client
npm start
```

### Step 4: Open Browser
Your browser should automatically open to `http://localhost:3000`

If not, manually visit: http://localhost:3000

## 🎉 Try It Out!

1. **Chat**: Type "Hello" in the chat box
2. **Teach**: Click "📚 Teach Me" and teach it something
3. **Ask**: Ask about what you just taught it
4. **Feedback**: Click "👍👎 Feedback" on any response

Watch the stats bar update as it learns!

## 🌐 Deploy to Internet (FREE!)

Once you've tested locally, deploy it for free:

### Easiest Method: Render (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "My adaptive AI"

   # Create repo on github.com first, then:
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Sign up (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Build Command**: `npm install && npm run install-all && npm run build`
     - **Start Command**: `npm start`
   - Click "Create Web Service"

3. **Add Storage** (So it remembers what it learns!)
   - After deployment, go to "Disks" tab
   - Click "Add Disk"
   - Mount path: `/opt/render/project/src/data`
   - Size: 1 GB
   - Save

4. **Done!** Your AI is live at: `https://your-app.onrender.com`

### Alternative: Replit (Even Easier - No Git!)

1. Go to [replit.com](https://replit.com)
2. Click "Create Repl" → "Import from GitHub"
3. Paste your GitHub URL (or upload files manually)
4. Click "Run"
5. Done! Share the URL with friends!

## 📖 Full Documentation

- **README.md** - Complete feature documentation
- **DEPLOYMENT.md** - All free hosting options explained

## ❓ Troubleshooting

### "Cannot find module" error
```bash
rm -rf node_modules client/node_modules
npm run install-all
```

### Port already in use
Kill the process using port 5000:
```bash
# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### AI forgets everything
Make sure you added persistent disk storage on your hosting platform!

## 🎊 That's It!

You now have a learning AI that anyone can teach and improve!

Share your URL with friends and watch it get smarter! 🧠✨
