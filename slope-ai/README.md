# 🎮 Slope AI - Autonomous Game Player

An AI that learns to play the online game **Slope** using Deep Q-Learning (DQN) and computer vision. The AI automatically detects your game region on screen and learns to control the ball using the A and D keys.

## 🌟 Features

- **Automatic Game Detection**: Detects the Slope game region on your screen
- **Deep Q-Learning**: Uses DQN (Deep Q-Network) for learning optimal strategies
- **Computer Vision**: Processes game frames to understand the environment
- **Real-time Training**: Watch the AI learn in real-time
- **Model Checkpoints**: Save and load trained models
- **Performance Tracking**: Visualize training progress with graphs

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

## 📋 Requirements

- Python 3.8+
- PyTorch
- OpenCV
- MSS (for screen capture)
- pynput (for keyboard control)
- A web browser with Slope game open

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   cd slope-ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **For GPU support (optional but recommended)**:
   ```bash
   # Install CUDA-enabled PyTorch
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

## 🎯 Usage

### Step 1: Open the Game

1. Open your web browser
2. Navigate to the Slope game (search "slope game" or use sites like y8.com)
3. Start the game and maximize the browser window
4. The game should be clearly visible on your screen

### Step 2: Train the AI

```bash
python train.py
```

**Training options**:
```bash
# Train for 500 episodes
python train.py --episodes 500

# Train without rendering (faster)
python train.py --no-render

# Continue training from checkpoint
python train.py --load checkpoints/dqn_checkpoint_ep100.pth

# Custom hyperparameters
python train.py --learning-rate 0.0001 --epsilon-decay 0.99
```

The AI will:
1. Automatically detect the game region
2. Start playing and learning
3. Save checkpoints every 10 episodes
4. Display progress in real-time

### Step 3: Watch the Trained AI Play

```bash
# Play with the best model
python play.py checkpoints/dqn_checkpoint_epbest.pth

# Play multiple episodes
python play.py checkpoints/dqn_checkpoint_epbest.pth --episodes 10
```

## 🎮 Manual Region Selection

If automatic detection fails:

```python
from game_environment import SlopeGameEnvironment

env = SlopeGameEnvironment()

# Manually set region (measure your game window)
region = {
    'top': 100,      # Y position from top of screen
    'left': 200,     # X position from left of screen
    'width': 800,    # Width of game area
    'height': 600    # Height of game area
}

env.setup(auto_detect=False, region=region)
```

## 📊 Training Parameters

### Default Hyperparameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Episodes | 1000 | Number of training episodes |
| Learning Rate | 0.00025 | Optimizer learning rate |
| Gamma | 0.99 | Discount factor for future rewards |
| Epsilon Start | 1.0 | Initial exploration rate |
| Epsilon End | 0.1 | Minimum exploration rate |
| Epsilon Decay | 0.995 | Rate of exploration decay |
| Memory Size | 10000 | Replay memory capacity |
| Batch Size | 32 | Training batch size |
| Frame Stack | 4 | Number of frames stacked |
| Frame Size | 84x84 | Input frame dimensions |

### Reward System

- **+1.0**: Survival (each frame alive)
- **+0.5**: Movement detected (forward progress)
- **+0.3**: Staying centered on path
- **-0.2**: No movement (might be stuck)
- **Game Over**: Episode ends

## 🧪 Testing Components

### Test Screen Capture
```bash
python -m utils.screen_capture
```

### Test Keyboard Controller
```bash
python -m utils.keyboard_controller
```

### Test Game Environment
```bash
python game_environment.py
```

### Test DQN Agent
```bash
python -m models.dqn_agent
```

## 📈 Monitoring Training

### Training Progress Plot

After training, check `checkpoints/training_progress.png` for:
- Episode rewards over time
- Moving average rewards
- Episode lengths
- Training loss

### Console Output

During training, you'll see:
```
📍 Episode 42/1000
   Epsilon: 0.847
   Step 0: Reward=1.0, Action=STAY
   Step 100: Reward=115.3, Action=RIGHT
   ...
✓ Episode 42 Complete!
   Duration: 45.2s
   Steps: 234
   Total Reward: 289.50
   Avg Loss: 0.0234
   Memory Size: 2340
   🌟 New Best Reward: 289.50!
   📊 Last 10 Episodes - Avg Reward: 245.32, Avg Length: 198.4
```

## 🔧 Troubleshooting

### Issue: Game region not detected

**Solution**:
- Make sure the game is fully visible
- Increase browser window size
- Use manual region selection
- Ensure game has high contrast (bright path, dark background)

### Issue: AI keeps dying immediately

**Solution**:
- Train for more episodes (AI needs time to learn)
- Check if game is responding to keyboard inputs
- Verify the game window is focused
- Adjust reward function in `game_environment.py`

### Issue: Training is slow

**Solution**:
- Use `--no-render` flag to disable visualization
- Reduce frame size in `SlopeGameEnvironment`
- Use GPU (install CUDA-enabled PyTorch)
- Reduce `action_repeat` parameter

### Issue: Actions not working in game

**Solution**:
- Click on the game window to focus it
- Check if browser/game accepts keyboard input
- Verify keyboard permissions (some OS require accessibility access)
- Try running as administrator (Windows) or with sudo (Linux)

### Issue: Out of memory

**Solution**:
- Reduce `memory_size` parameter
- Reduce `batch_size`
- Use smaller frame size
- Train on CPU instead of GPU

## 🎯 Tips for Better Training

1. **Start Simple**: Train for 100 episodes first to verify everything works
2. **Adjust Rewards**: Modify `_calculate_reward()` in `game_environment.py` based on game behavior
3. **Monitor Progress**: Watch the first few episodes to ensure detection and controls work
4. **Save Often**: Use lower save frequency for longer training sessions
5. **Experiment**: Try different hyperparameters (learning rate, epsilon decay, etc.)
6. **Use Checkpoints**: Resume training from best checkpoint to fine-tune

## 🧬 Customization

### Modify Neural Network Architecture

Edit `models/dqn_agent.py`:
```python
class DQN(nn.Module):
    def __init__(self, input_shape=(4, 84, 84), num_actions=3):
        super(DQN, self).__init__()
        # Add more layers or change architecture
        self.conv1 = nn.Conv2d(input_shape[0], 64, kernel_size=8, stride=4)
        # ...
```

### Adjust Reward Function

Edit `game_environment.py`:
```python
def _calculate_reward(self, current_frame, action):
    reward = 0.0
    # Customize reward logic
    reward += 2.0  # Higher survival reward
    # Add your own reward conditions
    return reward
```

### Change Game Detection

Edit `utils/screen_capture.py`:
```python
def detect_game_region(self, debug=False):
    # Modify detection algorithm
    # Adjust threshold values
    # Change contour filtering
```

## 📝 Project Structure

```
slope-ai/
├── models/
│   └── dqn_agent.py         # DQN neural network and agent
├── utils/
│   ├── screen_capture.py    # Screen capture and region detection
│   └── keyboard_controller.py # Keyboard control (A/D keys)
├── game_environment.py      # Game environment wrapper
├── train.py                 # Training script
├── play.py                  # Play with trained model
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Advanced Features

### Custom Training Loop

```python
from game_environment import SlopeGameEnvironment
from models.dqn_agent import DQNAgent

# Create environment and agent
env = SlopeGameEnvironment()
env.setup()

agent = DQNAgent(
    num_actions=env.get_action_space(),
    input_shape=env.get_observation_space()
)

# Custom training loop
for episode in range(100):
    state = env.reset()
    done = False

    while not done:
        action = agent.select_action(state)
        next_state, reward, done, info = env.step(action)
        agent.store_experience(state, action, reward, next_state, done)
        agent.train_step()
        state = next_state

    agent.update_epsilon()
```

### Transfer Learning

```python
# Load pre-trained model
agent.load('checkpoints/dqn_checkpoint_epbest.pth')

# Continue training with different parameters
agent.epsilon = 0.5  # Start with some exploration
agent.learning_rate = 0.0001  # Lower learning rate for fine-tuning
```

## 🤝 Contributing

Ideas for improvements:
- Better game over detection
- More sophisticated reward function
- Different RL algorithms (A3C, PPO, etc.)
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

If you encounter issues:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Test individual components
4. Ensure game is visible and accepting keyboard input

Happy training! 🚀
