import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [sessionId] = useState(`session-${Date.now()}`);
  const [showTeachModal, setShowTeachModal] = useState(false);
  const [showFeedbackModal, setShowFeedbackModal] = useState(false);
  const [selectedMessage, setSelectedMessage] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchStats();
    // Add welcome message
    setMessages([{
      type: 'ai',
      text: 'Hello! I\'m an adaptive learning AI. I learn from every conversation and improve over time. Try talking to me, and don\'t forget to teach me new things!',
      timestamp: new Date().toISOString()
    }]);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      type: 'user',
      text: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: inputMessage,
          sessionId
        })
      });

      const data = await response.json();

      const aiMessage = {
        type: 'ai',
        text: data.response,
        timestamp: new Date().toISOString(),
        messageId: data.messageId,
        knowledgeUsed: data.knowledgeUsed
      };

      setMessages(prev => [...prev, aiMessage]);
      fetchStats();
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage = {
        type: 'ai',
        text: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const openFeedbackModal = (message) => {
    setSelectedMessage(message);
    setShowFeedbackModal(true);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧠 Adaptive Learning AI</h1>
        <p className="tagline">An AI that learns from YOU</p>
      </header>

      {stats && (
        <div className="stats-bar">
          <div className="stat">
            <span className="stat-label">Knowledge:</span>
            <span className="stat-value">{stats.totalKnowledge}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Conversations:</span>
            <span className="stat-value">{stats.totalConversations}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Topics:</span>
            <span className="stat-value">{stats.topicsLearned}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Learned from users:</span>
            <span className="stat-value">{stats.knowledgeGrowth}</span>
          </div>
        </div>
      )}

      <div className="chat-container">
        <div className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-content">
                <div className="message-text">{message.text}</div>
                {message.type === 'ai' && message.messageId && (
                  <div className="message-actions">
                    <button
                      className="feedback-btn"
                      onClick={() => openFeedbackModal(message)}
                      title="Provide feedback"
                    >
                      👍👎 Feedback
                    </button>
                    {message.knowledgeUsed > 0 && (
                      <span className="knowledge-badge">
                        📚 Used {message.knowledgeUsed} knowledge
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message ai">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="input-form" onSubmit={sendMessage}>
          <button
            type="button"
            className="teach-button"
            onClick={() => setShowTeachModal(true)}
            title="Teach me something new"
          >
            📚 Teach Me
          </button>
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !inputMessage.trim()}>
            Send
          </button>
        </form>
      </div>

      {showTeachModal && (
        <TeachModal
          onClose={() => setShowTeachModal(false)}
          sessionId={sessionId}
          onSuccess={() => {
            fetchStats();
            setShowTeachModal(false);
          }}
        />
      )}

      {showFeedbackModal && selectedMessage && (
        <FeedbackModal
          message={selectedMessage}
          onClose={() => {
            setShowFeedbackModal(false);
            setSelectedMessage(null);
          }}
          sessionId={sessionId}
          onSuccess={() => {
            fetchStats();
            setShowFeedbackModal(false);
            setSelectedMessage(null);
          }}
        />
      )}
    </div>
  );
}

function TeachModal({ onClose, sessionId, onSuccess }) {
  const [topic, setTopic] = useState('');
  const [information, setInformation] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!topic.trim() || !information.trim()) return;

    setIsSubmitting(true);
    try {
      const response = await fetch('/api/teach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, information, sessionId })
      });

      if (response.ok) {
        onSuccess();
      }
    } catch (error) {
      console.error('Failed to teach:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>📚 Teach Me Something New</h2>
        <p>Help me learn by teaching me new information!</p>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Topic:</label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g., Python Programming"
              required
            />
          </div>
          <div className="form-group">
            <label>Information:</label>
            <textarea
              value={information}
              onChange={(e) => setInformation(e.target.value)}
              placeholder="e.g., Python is a high-level programming language known for its simple syntax and readability."
              rows="4"
              required
            />
          </div>
          <div className="modal-actions">
            <button type="button" onClick={onClose}>Cancel</button>
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Teaching...' : 'Teach Me'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function FeedbackModal({ message, onClose, sessionId, onSuccess }) {
  const [rating, setRating] = useState(0);
  const [correction, setCorrection] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (rating === 0) return;

    setIsSubmitting(true);
    try {
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messageId: message.messageId,
          rating,
          correction,
          sessionId
        })
      });

      if (response.ok) {
        onSuccess();
      }
    } catch (error) {
      console.error('Failed to send feedback:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>💬 Provide Feedback</h2>
        <p className="feedback-message">"{message.text}"</p>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Rate this response:</label>
            <div className="rating">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  className={`star ${rating >= star ? 'active' : ''}`}
                  onClick={() => setRating(star)}
                >
                  ⭐
                </button>
              ))}
            </div>
          </div>
          <div className="form-group">
            <label>Correction (optional):</label>
            <textarea
              value={correction}
              onChange={(e) => setCorrection(e.target.value)}
              placeholder="If my response was incorrect, please provide the correct information..."
              rows="3"
            />
          </div>
          <div className="modal-actions">
            <button type="button" onClick={onClose}>Cancel</button>
            <button type="submit" disabled={isSubmitting || rating === 0}>
              {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
