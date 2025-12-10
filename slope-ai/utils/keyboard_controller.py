"""
Keyboard controller for Slope game.
Handles A and D key presses for left/right movement.
"""
import time
from pynput.keyboard import Controller, Key


class KeyboardController:
    """Controls keyboard inputs for the game."""

    # Action constants
    ACTION_LEFT = 0
    ACTION_STAY = 1
    ACTION_RIGHT = 2

    def __init__(self):
        self.keyboard = Controller()
        self.current_key = None
        self.last_action_time = time.time()

    def press_key(self, key):
        """
        Press a key.

        Args:
            key: Character to press ('a' or 'd')
        """
        self.keyboard.press(key)

    def release_key(self, key):
        """
        Release a key.

        Args:
            key: Character to release ('a' or 'd')
        """
        self.keyboard.release(key)

    def release_all(self):
        """Release all currently pressed keys."""
        if self.current_key:
            self.release_key(self.current_key)
            self.current_key = None

    def execute_action(self, action):
        """
        Execute a game action.

        Args:
            action: Integer action code (0=left, 1=stay, 2=right)
        """
        # Release previous key
        self.release_all()

        # Execute new action
        if action == self.ACTION_LEFT:
            self.press_key('a')
            self.current_key = 'a'
        elif action == self.ACTION_RIGHT:
            self.press_key('d')
            self.current_key = 'd'
        elif action == self.ACTION_STAY:
            # No key pressed, just released previous
            pass

        self.last_action_time = time.time()

    def tap_key(self, key, duration=0.05):
        """
        Tap a key briefly.

        Args:
            key: Character to tap ('a' or 'd')
            duration: How long to hold the key
        """
        self.press_key(key)
        time.sleep(duration)
        self.release_key(key)

    def reset(self):
        """Reset controller state, releasing all keys."""
        self.release_all()

    @staticmethod
    def get_action_name(action):
        """Get human-readable action name."""
        names = {
            0: "LEFT",
            1: "STAY",
            2: "RIGHT"
        }
        return names.get(action, "UNKNOWN")

    @staticmethod
    def num_actions():
        """Get total number of possible actions."""
        return 3


if __name__ == "__main__":
    # Test the keyboard controller
    controller = KeyboardController()

    print("Testing keyboard controller...")
    print("Make sure a text editor or game is focused!")
    time.sleep(3)

    # Test sequence
    print("Pressing LEFT (a)")
    controller.execute_action(KeyboardController.ACTION_LEFT)
    time.sleep(0.5)

    print("Pressing RIGHT (d)")
    controller.execute_action(KeyboardController.ACTION_RIGHT)
    time.sleep(0.5)

    print("Releasing all (STAY)")
    controller.execute_action(KeyboardController.ACTION_STAY)

    print("Test complete!")
    controller.reset()
