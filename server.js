const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'client/build')));

// Import AI Engine
const AIEngine = require('./ai-engine/adaptive-ai');
const ai = new AIEngine();

// API Routes
app.post('/api/chat', async (req, res) => {
  try {
    const { message, sessionId } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    const response = await ai.processMessage(message, sessionId);
    res.json(response);
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ error: 'Failed to process message' });
  }
});

app.post('/api/feedback', async (req, res) => {
  try {
    const { messageId, rating, correction, sessionId } = req.body;

    await ai.processFeedback({ messageId, rating, correction, sessionId });
    res.json({ success: true, message: 'Feedback received. I\'m learning from this!' });
  } catch (error) {
    console.error('Feedback error:', error);
    res.status(500).json({ error: 'Failed to process feedback' });
  }
});

app.get('/api/stats', async (req, res) => {
  try {
    const stats = ai.getStats();
    res.json(stats);
  } catch (error) {
    console.error('Stats error:', error);
    res.status(500).json({ error: 'Failed to get stats' });
  }
});

app.post('/api/teach', async (req, res) => {
  try {
    const { topic, information, sessionId } = req.body;

    if (!topic || !information) {
      return res.status(400).json({ error: 'Topic and information are required' });
    }

    await ai.learn({ topic, information, sessionId });
    res.json({ success: true, message: 'Thank you for teaching me! I\'ve stored this knowledge.' });
  } catch (error) {
    console.error('Teaching error:', error);
    res.status(500).json({ error: 'Failed to process teaching' });
  }
});

// Serve React app for any other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`🚀 Adaptive Learning AI server running on port ${PORT}`);
  console.log(`📚 Learning mode: ACTIVE`);
});
