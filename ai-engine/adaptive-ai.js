const fs = require('fs').promises;
const path = require('path');

class AdaptiveAI {
  constructor() {
    this.knowledgeBase = [];
    this.conversations = [];
    this.feedback = [];
    this.dataDir = path.join(__dirname, '../data');
    this.initialize();
  }

  async initialize() {
    try {
      await fs.mkdir(this.dataDir, { recursive: true });
      await this.loadKnowledge();
      await this.loadConversations();
      await this.loadFeedback();
    } catch (error) {
      console.error('Initialization error:', error);
    }
  }

  async loadKnowledge() {
    try {
      const data = await fs.readFile(path.join(this.dataDir, 'knowledge.json'), 'utf-8');
      this.knowledgeBase = JSON.parse(data);
      console.log(`📚 Loaded ${this.knowledgeBase.length} knowledge entries`);
    } catch (error) {
      this.knowledgeBase = this.getDefaultKnowledge();
      await this.saveKnowledge();
    }
  }

  async loadConversations() {
    try {
      const data = await fs.readFile(path.join(this.dataDir, 'conversations.json'), 'utf-8');
      this.conversations = JSON.parse(data);
      console.log(`💬 Loaded ${this.conversations.length} conversations`);
    } catch (error) {
      this.conversations = [];
    }
  }

  async loadFeedback() {
    try {
      const data = await fs.readFile(path.join(this.dataDir, 'feedback.json'), 'utf-8');
      this.feedback = JSON.parse(data);
      console.log(`⭐ Loaded ${this.feedback.length} feedback entries`);
    } catch (error) {
      this.feedback = [];
    }
  }

  async saveKnowledge() {
    try {
      await fs.writeFile(
        path.join(this.dataDir, 'knowledge.json'),
        JSON.stringify(this.knowledgeBase, null, 2)
      );
    } catch (error) {
      console.error('Failed to save knowledge:', error);
    }
  }

  async saveConversations() {
    try {
      await fs.writeFile(
        path.join(this.dataDir, 'conversations.json'),
        JSON.stringify(this.conversations, null, 2)
      );
    } catch (error) {
      console.error('Failed to save conversations:', error);
    }
  }

  async saveFeedback() {
    try {
      await fs.writeFile(
        path.join(this.dataDir, 'feedback.json'),
        JSON.stringify(this.feedback, null, 2)
      );
    } catch (error) {
      console.error('Failed to save feedback:', error);
    }
  }

  getDefaultKnowledge() {
    return [
      {
        id: 'intro-1',
        topic: 'introduction',
        information: 'I am an adaptive learning AI. I learn from every conversation and improve over time.',
        source: 'system',
        timestamp: new Date().toISOString(),
        confidence: 1.0,
        useCount: 0
      },
      {
        id: 'intro-2',
        topic: 'learning',
        information: 'I can learn new information when you teach me or provide feedback on my responses.',
        source: 'system',
        timestamp: new Date().toISOString(),
        confidence: 1.0,
        useCount: 0
      }
    ];
  }

  findRelevantKnowledge(message) {
    const messageLower = message.toLowerCase();
    const words = messageLower.split(/\s+/);

    const scored = this.knowledgeBase.map(entry => {
      let score = 0;
      const entryText = (entry.topic + ' ' + entry.information).toLowerCase();

      // Exact topic match
      if (messageLower.includes(entry.topic.toLowerCase())) {
        score += 5;
      }

      // Word matching
      words.forEach(word => {
        if (word.length > 3 && entryText.includes(word)) {
          score += 1;
        }
      });

      // Boost by confidence and use count
      score *= entry.confidence;
      score += Math.min(entry.useCount * 0.1, 2);

      return { entry, score };
    });

    return scored
      .filter(item => item.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 5)
      .map(item => item.entry);
  }

  async processMessage(message, sessionId = 'default') {
    const messageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const relevantKnowledge = this.findRelevantKnowledge(message);

    // Get conversation history
    const sessionHistory = this.conversations
      .filter(c => c.sessionId === sessionId)
      .slice(-5);

    // Generate response based on learned knowledge
    const response = this.generateResponse(message, relevantKnowledge, sessionHistory);

    // Update use count for used knowledge
    relevantKnowledge.forEach(entry => {
      entry.useCount++;
    });

    // Store conversation
    const conversation = {
      messageId,
      sessionId,
      timestamp: new Date().toISOString(),
      userMessage: message,
      aiResponse: response,
      knowledgeUsed: relevantKnowledge.map(k => k.id)
    };

    this.conversations.push(conversation);
    await this.saveConversations();
    await this.saveKnowledge();

    return {
      messageId,
      response,
      knowledgeUsed: relevantKnowledge.length,
      totalKnowledge: this.knowledgeBase.length
    };
  }

  generateResponse(message, relevantKnowledge, history) {
    const messageLower = message.toLowerCase();

    // Check for greetings
    if (messageLower.match(/^(hi|hello|hey|greetings)/)) {
      const historyCount = this.conversations.filter(c => c.sessionId === history[0]?.sessionId).length;
      if (historyCount > 0) {
        return `Welcome back! I've learned from ${this.knowledgeBase.length} pieces of information so far. How can I help you today?`;
      }
      return `Hello! I'm an adaptive learning AI. I learn from every conversation. The more you interact with me and teach me, the smarter I become. What would you like to talk about?`;
    }

    // Check for questions about itself
    if (messageLower.includes('who are you') || messageLower.includes('what are you')) {
      return `I'm an adaptive learning AI that grows smarter with every interaction. I currently know about ${this.knowledgeBase.length} topics and have learned from ${this.conversations.length} conversations. Unlike traditional AI, I remember what people teach me and adjust my responses based on feedback.`;
    }

    // Check for learning requests
    if (messageLower.includes('teach you') || messageLower.includes('learn about')) {
      return `I'm ready to learn! Please use the "Teach Me" button or tell me what you'd like me to know. You can teach me facts, concepts, opinions, or anything you think I should know.`;
    }

    // Use learned knowledge to generate response
    if (relevantKnowledge.length > 0) {
      const primaryKnowledge = relevantKnowledge[0];
      let response = `Based on what I've learned: ${primaryKnowledge.information}`;

      if (relevantKnowledge.length > 1) {
        response += `\n\nI also know that: ${relevantKnowledge[1].information}`;
      }

      // Add confidence indicator
      if (primaryKnowledge.confidence < 0.7) {
        response += `\n\n(Note: I'm still learning about this topic, so please correct me if I'm wrong!)`;
      }

      return response;
    }

    // Check conversation history for context
    if (history.length > 0) {
      const lastConversation = history[history.length - 1];
      if (messageLower.includes('what') && messageLower.includes('you') && messageLower.includes('say')) {
        return `I said: "${lastConversation.aiResponse}"`;
      }
    }

    // Default response when no knowledge is found
    return `I don't have information about that yet, but I'd love to learn! You can teach me by using the "Teach Me" button or by providing feedback. The more people interact with me, the more knowledgeable I become. What would you like to teach me about this?`;
  }

  async learn({ topic, information, sessionId = 'default' }) {
    const entry = {
      id: `kb-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      topic: topic.trim(),
      information: information.trim(),
      source: sessionId,
      timestamp: new Date().toISOString(),
      confidence: 1.0,
      useCount: 0
    };

    this.knowledgeBase.push(entry);
    await this.saveKnowledge();

    console.log(`📚 Learned new knowledge: ${topic}`);
  }

  async processFeedback({ messageId, rating, correction, sessionId }) {
    const feedbackEntry = {
      id: `fb-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      messageId,
      sessionId,
      rating,
      correction,
      timestamp: new Date().toISOString()
    };

    this.feedback.push(feedbackEntry);
    await this.saveFeedback();

    // If correction provided, learn from it
    if (correction && correction.trim()) {
      const conversation = this.conversations.find(c => c.messageId === messageId);
      if (conversation) {
        // Reduce confidence of used knowledge if negative feedback
        if (rating < 3) {
          conversation.knowledgeUsed.forEach(knowledgeId => {
            const entry = this.knowledgeBase.find(k => k.id === knowledgeId);
            if (entry) {
              entry.confidence = Math.max(0.1, entry.confidence - 0.2);
            }
          });
        }

        // Add correction as new knowledge
        await this.learn({
          topic: conversation.userMessage.split(' ').slice(0, 3).join(' '),
          information: correction,
          sessionId
        });
      }
    } else if (rating >= 4) {
      // Boost confidence of used knowledge if positive feedback
      const conversation = this.conversations.find(c => c.messageId === messageId);
      if (conversation) {
        conversation.knowledgeUsed.forEach(knowledgeId => {
          const entry = this.knowledgeBase.find(k => k.id === knowledgeId);
          if (entry) {
            entry.confidence = Math.min(1.0, entry.confidence + 0.1);
          }
        });
      }
    }

    await this.saveKnowledge();
    console.log(`⭐ Received feedback for message ${messageId}: ${rating}/5`);
  }

  getStats() {
    const totalConversations = this.conversations.length;
    const totalKnowledge = this.knowledgeBase.length;
    const totalFeedback = this.feedback.length;
    const avgRating = this.feedback.length > 0
      ? this.feedback.reduce((sum, f) => sum + (f.rating || 0), 0) / this.feedback.filter(f => f.rating).length
      : 0;

    const topicsLearned = [...new Set(this.knowledgeBase.map(k => k.topic))];

    return {
      totalConversations,
      totalKnowledge,
      totalFeedback,
      averageRating: avgRating.toFixed(2),
      topicsLearned: topicsLearned.length,
      knowledgeGrowth: this.knowledgeBase.filter(k => k.source !== 'system').length
    };
  }
}

module.exports = AdaptiveAI;
