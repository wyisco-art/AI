# 🎮 Slope AI - Autonomous Game Player

An AI that learns to play the online game **Slope** using Deep Q-Learning (DQN) and computer vision. The AI automatically detects your game region on screen and learns to control the ball using the A and D keys.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Automatic Game Detection**: Detects the Slope game region on your screen
- **Deep Q-Learning**: Uses DQN (Deep Q-Network) for learning optimal strategies
- **Computer Vision**: Processes game frames to understand the environment
- **Real-time Training**: Watch the AI learn in real-time
- **Model Checkpoints**: Save and load trained models
- **Performance Tracking**: Visualize training progress with graphs
- **Interactive Quick Start**: Easy-to-use menu for beginners

## 🧠 How It Works

1. **Screen Capture**: Captures the game region from your screen
2. **Preprocessing**: Converts frames to grayscale and normalizes
3. **Frame Stacking**: Stacks 4 frames to give temporal information
4. **Neural Network**: Processes frames through a convolutional neural network
5. **Q-Learning**: Learns which actions (left/stay/right) maximize rewards
6. **Action Execution**: Sends keyboard commands (A/D) to control the game

### Architecture

```
┌─────────────────┐
│  Screen Capture │
│   (Game Region) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preprocessing  │
│   (84x84 gray)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Frame Stacking │
│   (4 frames)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   DQN Network   │
│  (Conv layers)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Action Selection│
│  (A / Stay / D) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Keyboard Control │
│   (pynput)      │
└─────────────────┘
```

## 🚀 Quick Start

### Installation

```bash
# Navigate to project directory
cd slope-ai

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Option 1: Interactive Quick Start (Easiest!)

```bash
python quickstart.py
```

This will guide you through:
- Testing your setup
- Training your first AI
- Watching it play

#### Option 2: Direct Commands

```bash
# 1. Test setup (make sure Slope game is open and visible)
python game_environment.py

# 2. Train AI (100 episodes - good for first try)
python train.py --episodes 100

# 3. Watch AI play
python play.py checkpoints/dqn_checkpoint_epbest.pth
```

## 📋 Requirements

- Python 3.8+
- PyTorch
- OpenCV
- MSS (for screen capture)
- pynput (for keyboard control)
- A web browser with Slope game open

## 📖 Documentation

- **[Complete Documentation](./slope-ai/README.md)** - Full architecture details, troubleshooting, and customization
- **[Quick Start Guide](./slope-ai/QUICKSTART.md)** - Get up and running in 5 minutes
- **[Training Guide](./slope-ai/README.md#-usage)** - Detailed training instructions

## 🎯 Training Process

### What to Expect

- **Episodes 1-20**: Random exploration, dies quickly (learning basics)
- **Episodes 20-50**: Starts learning patterns, survives longer
- **Episodes 50-100**: Decent player, avoids obvious obstacles
- **Episodes 100-500**: Skilled player, handles complex situations
- **Episodes 500+**: Expert level, can match/exceed human performance

### Training Tips

✅ Game is open and fully visible
✅ Game window is reasonably large (at least 600x400 pixels)
✅ Good contrast between game and background
✅ Computer won't go to sleep during training

## 🎮 Command Reference

### Training Commands

```bash
# Basic training
python train.py --episodes 100

# Fast training (no visualization)
python train.py --episodes 500 --no-render

# Continue from checkpoint
python train.py --load checkpoints/dqn_checkpoint_ep100.pth --episodes 200

# Custom hyperparameters
python train.py --episodes 300 --learning-rate 0.0001 --epsilon-decay 0.99
```

### Playback Commands

```bash
# Play with best model
python play.py checkpoints/dqn_checkpoint_epbest.pth

# Watch multiple episodes
python play.py checkpoints/dqn_checkpoint_epbest.pth --episodes 10
```

## 📊 Project Structure

```
slope-ai/
├── models/
│   ├── __init__.py
│   └── dqn_agent.py         # DQN neural network and agent
├── utils/
│   ├── __init__.py
│   ├── screen_capture.py    # Screen capture and region detection
│   └── keyboard_controller.py # Keyboard control (A/D keys)
├── game_environment.py      # Game environment wrapper
├── train.py                 # Training script
├── play.py                  # Play with trained model
├── quickstart.py            # Interactive menu
├── requirements.txt         # Python dependencies
├── README.md               # Detailed documentation
└── QUICKSTART.md           # Quick start guide
```

## 🔧 Technical Details

- **Neural Network**: CNN with 3 convolutional layers + 2 fully connected layers
- **Algorithm**: Deep Q-Learning (DQN) with experience replay
- **Input**: 84x84 grayscale images, 4-frame stack
- **Actions**: 3 discrete actions (left, stay, right)
- **Framework**: PyTorch
- **Computer Vision**: OpenCV + MSS
- **Control**: pynput for keyboard automation

## 🎓 How Deep Q-Learning Works

1. **Experience Replay**: Stores past experiences and samples randomly to break correlation
2. **Target Network**: Separate network for stable Q-value targets
3. **Epsilon-Greedy**: Balances exploration (random actions) vs exploitation (learned actions)
4. **Reward Shaping**: Custom reward function encourages survival and forward progress

## 🐛 Troubleshooting

### Game region not detected

- Make sure the game is fully visible
- Increase browser window size
- Use manual region selection
- Ensure game has high contrast

### AI keeps dying immediately

- Normal for first 20-30 episodes (it's learning!)
- Train for more episodes
- Check if game is responding to keyboard inputs

### Training is slow

- Use `--no-render` flag to disable visualization
- Use GPU (install CUDA-enabled PyTorch)
- Reduce frame size or action repeat

See the [full documentation](./slope-ai/README.md) for more troubleshooting tips.

## 🤝 Contributing

Ideas for improvements:
- Better game over detection
- More sophisticated reward functions
- Different RL algorithms (A3C, PPO, Rainbow DQN)
- Multi-game support
- Better visualization tools
- Curriculum learning

## 📜 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- Deep Q-Learning algorithm: [Mnih et al., 2015](https://www.nature.com/articles/nature14236)
- PyTorch framework
- OpenAI Gym for environment design patterns

## ⚠️ Disclaimer

This is an educational project for learning about reinforcement learning and computer vision. Use responsibly and respect the terms of service of any games you interact with.

---

**Made with 🧠 for AI and 🎮 for gaming!**

## 📞 Support

Having issues? Check out:
1. [Troubleshooting Guide](./slope-ai/README.md#-troubleshooting)
2. [Quick Start Guide](./slope-ai/QUICKSTART.md)
3. [FAQ](./slope-ai/QUICKSTART.md#-faq)

Happy training! 🚀
