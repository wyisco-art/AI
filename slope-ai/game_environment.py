"""
Game environment wrapper for Slope.
Manages game state, rewards, and interaction between AI and game.
"""
import numpy as np
import cv2
import time
from collections import deque
from utils.screen_capture import ScreenCapture
from utils.keyboard_controller import KeyboardController


class SlopeGameEnvironment:
    """Environment wrapper for the Slope game."""

    def __init__(self, frame_stack=4, frame_size=(84, 84), action_repeat=4):
        """
        Initialize game environment.

        Args:
            frame_stack: Number of frames to stack for temporal information
            frame_size: Size to resize frames to (width, height)
            action_repeat: Number of times to repeat each action
        """
        self.frame_stack = frame_stack
        self.frame_size = frame_size
        self.action_repeat = action_repeat

        # Initialize components
        self.screen_capture = ScreenCapture()
        self.controller = KeyboardController()

        # Frame buffer for stacking
        self.frame_buffer = deque(maxlen=frame_stack)

        # Game state
        self.previous_frame = None
        self.game_running = False
        self.episode_steps = 0
        self.episode_reward = 0

        # Stats
        self.total_episodes = 0
        self.best_score = 0

    def setup(self, auto_detect=True, region=None):
        """
        Setup the environment by detecting game region.

        Args:
            auto_detect: Whether to auto-detect game region
            region: Manual region dict if not auto-detecting

        Returns:
            True if setup successful
        """
        print("\n🎮 Setting up Slope Game Environment")
        print("=" * 50)

        if auto_detect:
            detected_region = self.screen_capture.detect_game_region(debug=True)
            if not detected_region:
                print("❌ Failed to detect game region")
                return False
        else:
            if region is None:
                print("❌ No region provided for manual setup")
                return False
            self.screen_capture.set_game_region(region)

        print("✓ Environment setup complete!")
        return True

    def reset(self):
        """
        Reset environment for new episode.

        Returns:
            Initial state (stacked frames)
        """
        # Release all keys
        self.controller.reset()

        # Wait for game to reset (user may need to restart manually)
        print("\n🔄 Resetting... Make sure game is ready!")
        time.sleep(1)

        # Clear frame buffer and fill with initial frame
        initial_frame = self._capture_and_preprocess()
        self.frame_buffer.clear()
        for _ in range(self.frame_stack):
            self.frame_buffer.append(initial_frame)

        self.previous_frame = initial_frame
        self.episode_steps = 0
        self.episode_reward = 0
        self.game_running = True
        self.total_episodes += 1

        return self._get_state()

    def step(self, action):
        """
        Execute action and return next state, reward, done.

        Args:
            action: Action to execute (0=left, 1=stay, 2=right)

        Returns:
            Tuple of (next_state, reward, done, info)
        """
        total_reward = 0

        # Repeat action for smoother control
        for _ in range(self.action_repeat):
            # Execute action
            self.controller.execute_action(action)

            # Small delay for action to take effect
            time.sleep(0.016)  # ~60 FPS

            # Capture new frame
            current_frame = self._capture_and_preprocess()

            # Calculate reward
            reward = self._calculate_reward(current_frame, action)
            total_reward += reward

            # Check if game over
            done = self._is_game_over(current_frame)

            if done:
                self.game_running = False
                break

        # Update frame buffer
        self.frame_buffer.append(current_frame)
        self.previous_frame = current_frame

        # Update stats
        self.episode_steps += 1
        self.episode_reward += total_reward

        # Get next state
        next_state = self._get_state()

        # Info dict
        info = {
            'episode_steps': self.episode_steps,
            'episode_reward': self.episode_reward,
        }

        return next_state, total_reward, done, info

    def _capture_and_preprocess(self):
        """
        Capture and preprocess game frame.

        Returns:
            Preprocessed frame (grayscale, normalized)
        """
        frame = self.screen_capture.capture_game(resize_to=self.frame_size)
        return frame

    def _get_state(self):
        """
        Get current state (stacked frames).

        Returns:
            State as numpy array of shape (frame_stack, height, width)
        """
        return np.array(self.frame_buffer)

    def _calculate_reward(self, current_frame, action):
        """
        Calculate reward based on game state.

        Reward scheme:
        - Small positive reward for surviving each frame
        - Bonus for forward progress (movement)
        - Penalty for staying too far left/right (encourage centering)
        - Large negative reward for game over

        Args:
            current_frame: Current game frame
            action: Action taken

        Returns:
            Reward value
        """
        reward = 0.0

        # Survival reward - just staying alive is good!
        reward += 1.0

        # Movement detection - check if frame changed significantly
        if self.previous_frame is not None:
            frame_diff = np.abs(current_frame - self.previous_frame).mean()

            # If frame is changing, we're probably moving forward (good!)
            if frame_diff > 0.01:
                reward += 0.5
            else:
                # Not moving might mean we hit a wall
                reward -= 0.2

        # Encourage staying centered (analyze frame brightness distribution)
        # Slope game typically has the path in the center
        center_region = current_frame[:, self.frame_size[0]//4:3*self.frame_size[0]//4]
        center_brightness = center_region.mean()

        # If center is bright, we're likely on the path
        if center_brightness > 0.3:
            reward += 0.3

        return reward

    def _is_game_over(self, current_frame):
        """
        Detect if game is over.

        Game over detection strategies:
        1. Check if frame has stopped changing (stuck/died)
        2. Look for game over screen characteristics
        3. Check for sudden brightness change (death flash)

        Args:
            current_frame: Current game frame

        Returns:
            True if game over detected
        """
        if self.previous_frame is None:
            return False

        # Check if frame stopped changing significantly
        frame_diff = np.abs(current_frame - self.previous_frame).mean()

        if frame_diff < 0.005:  # Very little change
            # Frame might be frozen (game over)
            return True

        # Check for very dark or very bright frame (death effect)
        frame_mean = current_frame.mean()
        if frame_mean < 0.05 or frame_mean > 0.95:
            return True

        # Max steps per episode (timeout)
        if self.episode_steps > 10000:
            return True

        return False

    def render(self, state=None, action=None, reward=None):
        """
        Render the current state for visualization.

        Args:
            state: Current state to render
            action: Current action being taken
            reward: Current reward
        """
        if state is None:
            frame = self.screen_capture.capture_game(resize_to=None)
        else:
            # Take the most recent frame from state
            frame = state[-1]
            # Resize for better visibility
            frame = cv2.resize(frame, (400, 400))

        # Convert to BGR for OpenCV display
        if len(frame.shape) == 2:  # Grayscale
            display_frame = cv2.cvtColor((frame * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)
        else:
            display_frame = (frame * 255).astype(np.uint8)

        # Add info overlay
        if action is not None:
            action_text = self.controller.get_action_name(action)
            cv2.putText(display_frame, f"Action: {action_text}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if reward is not None:
            cv2.putText(display_frame, f"Reward: {reward:.2f}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.putText(display_frame, f"Steps: {self.episode_steps}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Slope AI', display_frame)
        cv2.waitKey(1)

    def close(self):
        """Clean up resources."""
        self.controller.reset()
        cv2.destroyAllWindows()

    def get_action_space(self):
        """Get number of possible actions."""
        return self.controller.num_actions()

    def get_observation_space(self):
        """Get shape of observation (state)."""
        return (self.frame_stack, *self.frame_size)


if __name__ == "__main__":
    # Test the environment
    print("Testing Slope Game Environment...")

    env = SlopeGameEnvironment()

    # Setup
    if not env.setup(auto_detect=True):
        print("Setup failed!")
        exit(1)

    print(f"\nObservation space: {env.get_observation_space()}")
    print(f"Action space: {env.get_action_space()}")

    # Test episode
    print("\nTesting episode (5 seconds)...")
    state = env.reset()
    print(f"Initial state shape: {state.shape}")

    for i in range(100):  # ~5 seconds at 60fps with action_repeat=4
        # Random action
        action = np.random.randint(0, env.get_action_space())

        # Step
        next_state, reward, done, info = env.step(action)

        # Render
        env.render(next_state, action, reward)

        if done:
            print(f"\nEpisode finished after {info['episode_steps']} steps")
            print(f"Total reward: {info['episode_reward']:.2f}")
            break

        time.sleep(0.1)

    env.close()
    print("\n✓ Environment test complete!")
