# 🚀 Slope AI - Quick Start Guide

Get up and running with Slope AI in 5 minutes!

## ⚡ Quick Installation

```bash
# Navigate to slope-ai directory
cd slope-ai

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Basic Usage

### Option 1: Interactive Quick Start (Easiest!)

```bash
python quickstart.py
```

This will guide you through:
- Testing your setup
- Training your first AI
- Watching it play

### Option 2: Direct Commands

#### 1. Test Setup
```bash
# Make sure Slope game is open and visible, then run:
python game_environment.py
```

#### 2. Train AI (100 episodes - good for first try)
```bash
python train.py --episodes 100
```

#### 3. Watch AI Play
```bash
python play.py checkpoints/dqn_checkpoint_epbest.pth
```

## 📝 Step-by-Step First Run

### 1. Prepare the Game

1. Open your web browser
2. Search for "slope game" (try sites like y8.com or other game sites)
3. Click to start the game
4. **Important**: Make sure the game window is visible and not minimized!

### 2. Test Detection

```bash
python quickstart.py
```

Select option `1. Test Setup` to verify the AI can see your game.

### 3. Start Training

In the quickstart menu, select option `5. Quick Training` for a fast 100-episode session.

Or manually:
```bash
python train.py --episodes 100
```

**What to expect:**
- The AI will detect your game region (you'll see a green box)
- Training will start - you'll see episodes counting up
- The AI starts by exploring randomly (lots of mistakes!)
- After ~20 episodes, you'll start seeing improvement
- After ~50 episodes, it should be pretty decent!

### 4. Watch Your AI Play

```bash
python play.py checkpoints/dqn_checkpoint_epbest.pth --episodes 3
```

## 🎯 Tips for First-Time Users

### Before Training:
✅ Game is open and fully visible
✅ Game window is reasonably large (at least 600x400 pixels)
✅ Good contrast between game and background
✅ You won't need to use keyboard during training
✅ Computer won't go to sleep during training

### During Training:
- Don't minimize the game window!
- Don't click on other windows (keep game focused)
- Let it run - 100 episodes takes about 20-30 minutes
- Watch the reward numbers go up over time

### Troubleshooting:
- **"Game region not detected"**: Make game window bigger, ensure it's visible
- **"AI keeps dying immediately"**: Normal! It needs ~20 episodes to learn basics
- **"Keys not working"**: Click on game window to focus it
- **"Training is slow"**: Use `--no-render` flag for faster training

## 🎓 Next Steps

Once you've completed your first training:

1. **Train Longer**: Try 500 or 1000 episodes for better performance
   ```bash
   python train.py --episodes 500
   ```

2. **Continue Training**: Resume from your best checkpoint
   ```bash
   python train.py --load checkpoints/dqn_checkpoint_epbest.pth --episodes 200
   ```

3. **Experiment**: Try different hyperparameters
   ```bash
   python train.py --episodes 300 --learning-rate 0.0001 --epsilon-decay 0.99
   ```

4. **Customize**: Edit the reward function in `game_environment.py` to change how the AI learns

## 📊 Understanding Results

### Good Signs:
- Episode rewards increasing over time
- AI surviving longer in each episode
- Less random movements, more purposeful control
- Loss values decreasing

### Normal for First Episodes:
- AI dies immediately (it's exploring!)
- Random-looking movements
- Low rewards (0-50 range)

### After ~50 Episodes:
- Should survive 100+ steps
- Rewards around 100-300
- Smoother control

### After ~200 Episodes:
- Can play for 500+ steps
- Rewards 500+
- Almost human-like play!

## 🎮 Command Reference

### Training
```bash
# Basic training
python train.py --episodes 100

# Fast training (no visualization)
python train.py --episodes 500 --no-render

# Continue from checkpoint
python train.py --load checkpoints/dqn_checkpoint_ep100.pth --episodes 200

# Custom learning
python train.py --episodes 300 --learning-rate 0.0001
```

### Playing
```bash
# Play with best model
python play.py checkpoints/dqn_checkpoint_epbest.pth

# Watch multiple episodes
python play.py checkpoints/dqn_checkpoint_epbest.pth --episodes 10
```

### Testing
```bash
# Test environment
python game_environment.py

# Test screen capture
python -m utils.screen_capture

# Test keyboard
python -m utils.keyboard_controller
```

## ❓ FAQ

**Q: How long does training take?**
A: 100 episodes: ~20-30 minutes, 500 episodes: ~2 hours, 1000 episodes: ~4 hours

**Q: Can I pause training?**
A: Yes! Press Ctrl+C to stop. Your last checkpoint will be saved. Resume with `--load` flag.

**Q: Does it work on Mac/Linux/Windows?**
A: Yes! Tested on all platforms. Note: Some OSes may require accessibility permissions for keyboard control.

**Q: Do I need a GPU?**
A: No, but it helps! Training on CPU works fine, just a bit slower.

**Q: Can I train while doing other things?**
A: Not really - the AI needs the game window to stay focused and visible. Use `--no-render` for slightly less intensive training.

**Q: How good can the AI get?**
A: With enough training (1000+ episodes), it can match or exceed human performance!

**Q: Can I use this for other games?**
A: The code is generalizable! You'd need to modify reward functions and detection logic.

## 🆘 Getting Help

If you run into issues:

1. Check `README.md` for detailed troubleshooting
2. Verify all dependencies are installed: `pip list`
3. Test components individually (see Testing section above)
4. Make sure game is visible and accepting keyboard input

## 🎉 You're Ready!

Now run:
```bash
python quickstart.py
```

And let the AI learning begin! 🚀

---

**Happy training!** 🎮🧠
