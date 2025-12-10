# 🧠 Adaptive Learning AI

An AI chatbot that **learns from every conversation** and adapts its responses over time based on user interactions, feedback, and teachings.

## 📚 Documentation

- **[📦 Complete Installation Guide](INSTALL.md)** - Step-by-step setup from scratch
- **[⚡ Quick Start](QUICKSTART.md)** - Get running in 3 minutes (for experienced devs)
- **[📖 Full Documentation](#)** - You're reading it!

## ✨ Features

- **Adaptive Learning**: The AI learns from every interaction and improves over time
- **User Teaching**: Anyone can teach the AI new information through the "Teach Me" feature
- **Feedback System**: Rate responses and provide corrections to help the AI learn
- **Knowledge Base**: Stores and retrieves learned information with confidence scoring
- **Conversation Memory**: Remembers context from previous conversations
- **Real-time Stats**: See the AI's learning progress in real-time
- **🌑 Apple-like Dark Mode UI**: Stunning dark theme with glassmorphism effects and smooth animations
- **🎬 Smooth Onboarding**: Beautiful first-time user experience explaining how the AI works
- **Beautiful UI**: Modern, responsive chat interface with premium design

## 🎯 How It Works

### Learning Mechanisms

1. **Direct Teaching**: Users can teach the AI new topics and information through the "Teach Me" button
2. **Feedback Learning**: When users rate responses or provide corrections, the AI adjusts its knowledge confidence
3. **Usage Patterns**: The AI tracks which knowledge is most useful and prioritizes it
4. **Context Awareness**: The AI uses conversation history to provide better responses

### Knowledge System

- **Knowledge Base**: Stores learned information with topics, confidence scores, and usage counts
- **Relevance Scoring**: Matches user queries with the most relevant knowledge
- **Confidence Adjustment**: Positive feedback increases confidence, negative feedback decreases it
- **Continuous Growth**: The knowledge base grows with every teaching and correction

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   npm run install-all
   ```

2. **Start Development Server**
   ```bash
   # Terminal 1 - Start backend
   npm run dev

   # Terminal 2 - Start frontend
   cd client && npm start
   ```

3. **Open Browser**
   Navigate to `http://localhost:3000`

### Production Build

```bash
npm run install-all
npm run build
npm start
```

## 🌐 Free Hosting Options

### Option 1: Render (Recommended - Easiest)

**Why Render?** Free tier includes persistent storage (perfect for the learning AI), automatic deploys, and easy setup.

1. **Create Account**: Go to [render.com](https://render.com) and sign up
2. **New Web Service**: Click "New +" → "Web Service"
3. **Connect Repository**: Connect your GitHub repository
4. **Configuration**:
   - **Name**: adaptive-learning-ai
   - **Environment**: Node
   - **Build Command**: `npm install && npm run install-all && npm run build`
   - **Start Command**: `npm start`
   - **Plan**: Free
5. **Add Disk**:
   - Go to "Disks" in your service settings
   - Click "Add Disk"
   - **Name**: ai-data
   - **Mount Path**: `/opt/render/project/src/data`
   - **Size**: 1 GB (free)
6. **Deploy**: Click "Create Web Service"

Your AI will be live at: `https://your-app-name.onrender.com`

### Option 2: Railway

**Why Railway?** Great free tier, simple deployment, includes storage.

1. **Create Account**: Go to [railway.app](https://railway.app)
2. **New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select Repository**: Choose your repository
4. **Add Variables**:
   - `NODE_ENV`: production
   - `PORT`: 5000
5. **Deploy**: Railway will automatically build and deploy

Your AI will be live at: `https://your-app.railway.app`

### Option 3: Replit (Easiest - No GitHub Required)

**Why Replit?** Simplest option, no git required, instant deployment.

1. **Create Account**: Go to [replit.com](https://replit.com)
2. **Import Repository**: Click "Create Repl" → "Import from GitHub"
3. **Paste URL**: Paste your repository URL
4. **Run**: Click the "Run" button
5. **Share**: Click the share button to get your public URL

### Option 4: Vercel + MongoDB Atlas

**Why This Combo?** Best for scalability, but requires external database.

**Note**: Vercel's free tier has serverless functions, so you'll need to store data externally.

1. **Setup MongoDB Atlas** (Free):
   - Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Create free cluster
   - Get connection string

2. **Deploy to Vercel**:
   ```bash
   npm i -g vercel
   vercel
   ```

3. **Add Environment Variable**:
   - In Vercel dashboard, add `MONGODB_URI` with your connection string

## 🎨 UI Features

### Dark Mode Design
- **Apple-inspired aesthetics** with true black backgrounds (#000000)
- **Glassmorphism effects** with backdrop blur for modern look
- **Smooth animations** with cubic-bezier easing curves
- **Gradient accents** using blue-purple color scheme
- **Custom scrollbars** that match the dark theme
- **Hover effects** with elevation changes on all interactive elements
- **Responsive design** that looks great on all devices

### Onboarding Experience
- **First-time visitors** see a beautiful onboarding screen
- **Three key features** highlighted with smooth animations
- **Staggered animations** for feature cards
- **Floating icon** animation for visual appeal
- **Get Started button** to begin using the AI
- Onboarding preference saved in localStorage (shows only once)

### Reset Onboarding
To see the onboarding screen again:
1. Open browser console (F12)
2. Type: `localStorage.removeItem('hasSeenOnboarding')`
3. Refresh the page

## 💡 Usage Guide

### Chatting with the AI

1. Type your message in the input box
2. The AI will respond based on its learned knowledge
3. If it doesn't know something, it will ask you to teach it!

### Teaching the AI

1. Click the **"📚 Teach Me"** button
2. Enter a topic (e.g., "JavaScript")
3. Enter information (e.g., "JavaScript is a programming language...")
4. Click "Teach Me"
5. The AI now knows this information!

### Providing Feedback

1. After receiving a response, click the **"👍👎 Feedback"** button
2. Rate the response (1-5 stars)
3. Optionally provide a correction if the response was wrong
4. The AI will learn from your feedback!

### Monitoring Learning

- Check the **stats bar** at the top to see:
  - Total knowledge entries
  - Number of conversations
  - Topics learned
  - Knowledge growth from users

## 🔧 Technical Details

### Architecture

```
┌─────────────────┐
│  React Frontend │
│   (Port 3000)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Express Server │
│   (Port 5000)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   AI Engine     │
│  (adaptive-ai)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JSON Storage   │
│   (/data/*.json)│
└─────────────────┘
```

### Data Storage

The AI stores data in three JSON files:

- **knowledge.json**: All learned information with confidence scores
- **conversations.json**: Complete conversation history
- **feedback.json**: All feedback and ratings

### API Endpoints

- `POST /api/chat`: Send a message to the AI
- `POST /api/teach`: Teach the AI new information
- `POST /api/feedback`: Provide feedback on a response
- `GET /api/stats`: Get learning statistics

### Knowledge Structure

```javascript
{
  id: "unique-id",
  topic: "JavaScript",
  information: "JavaScript is a programming language...",
  source: "session-id",
  timestamp: "2024-01-01T00:00:00.000Z",
  confidence: 1.0,
  useCount: 5
}
```

## 🎨 Customization

### Modify AI Personality

Edit `/ai-engine/adaptive-ai.js` → `generateResponse()` method to change how the AI responds.

### Adjust Learning Behavior

In `/ai-engine/adaptive-ai.js`:
- `findRelevantKnowledge()`: Modify how knowledge is matched
- `processFeedback()`: Change how feedback affects confidence
- Confidence boost/reduction values

### Style Customization

Edit `/client/src/App.css` to change colors, layout, and styling.

## 📊 Example Interactions

### Teaching Example

**User**: "I want to teach you about Python"
**AI**: "I'm ready to learn! Please use the 'Teach Me' button..."

*User clicks "Teach Me" button*
- Topic: "Python"
- Information: "Python is a high-level programming language known for readability"

**AI**: "Thank you for teaching me! I've stored this knowledge."

### Learning Example

**User**: "Tell me about Python"
**AI**: "Based on what I've learned: Python is a high-level programming language known for readability"

### Feedback Example

*After AI responds*

User clicks "Feedback" → Rates 5 stars
**AI**: "Feedback received. I'm learning from this!"

## 🛡️ Data Privacy

- All data is stored locally in the `/data` folder
- No external AI APIs required (unless you add them)
- Sessions are identified by random IDs
- No personal information is collected

## 🚧 Future Enhancements

Potential improvements you can add:

- [ ] Integration with OpenAI/Anthropic APIs for better responses
- [ ] User authentication and personal learning profiles
- [ ] Export/import knowledge base
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Knowledge graph visualization
- [ ] Admin panel for knowledge management
- [ ] Advanced search and filtering
- [ ] Topic clustering and organization
- [ ] Collaborative learning features

## 📝 Development Notes

### Adding External AI Integration

To integrate with OpenAI or Anthropic:

1. Install SDK: `npm install openai` or `npm install @anthropic-ai/sdk`
2. Add API key to `.env`
3. Modify `generateResponse()` in `/ai-engine/adaptive-ai.js`
4. Use learned knowledge as context in prompts

### Scaling Considerations

For production at scale:
- Replace JSON storage with a real database (PostgreSQL, MongoDB)
- Add caching layer (Redis)
- Implement rate limiting
- Add authentication
- Use message queues for async processing

## 🤝 Contributing

Feel free to fork, modify, and enhance this project! Some ideas:

- Add new learning mechanisms
- Improve the UI/UX
- Implement new features
- Optimize the knowledge matching algorithm
- Add testing

## 📄 License

MIT License - Feel free to use this project however you'd like!

## 🙏 Support

If you encounter issues:
1. Check that all dependencies are installed
2. Ensure the `/data` folder has write permissions
3. Check console for error messages
4. Verify your hosting platform supports persistent storage

## 🎉 Have Fun!

This AI learns from YOU. The more you interact with it, teach it, and provide feedback, the smarter it becomes. Create something amazing!

---

**Made with ❤️ for learning and experimentation**
