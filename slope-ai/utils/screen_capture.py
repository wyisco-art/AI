"""
Screen capture and game region detection for Slope game.
"""
import mss
import numpy as np
import cv2
from PIL import Image
import time


class ScreenCapture:
    """Captures screen and detects game region."""

    def __init__(self):
        self.sct = mss.mss()
        self.game_region = None
        self.monitor = None

    def capture_screen(self, region=None):
        """
        Capture screen or specific region.

        Args:
            region: Dict with {'top', 'left', 'width', 'height'} or None for full screen

        Returns:
            numpy array of captured image in RGB
        """
        if region is None:
            region = self.sct.monitors[1]  # Primary monitor

        screenshot = self.sct.grab(region)
        img = np.array(screenshot)

        # Convert BGRA to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        return img

    def detect_game_region(self, debug=False):
        """
        Automatically detect the game region on screen.

        The Slope game typically has a distinctive dark background with a bright
        triangular play area. This function looks for those characteristics.

        Args:
            debug: If True, shows detection visualization

        Returns:
            Dict with game region coordinates or None if not found
        """
        print("🔍 Detecting game region...")
        print("Please make sure the Slope game is visible on your screen!")
        time.sleep(2)

        # Capture full screen
        screen = self.capture_screen()

        # Convert to grayscale for detection
        gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

        # Look for bright regions (the game area is typically bright)
        _, binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour (likely the game area)
        if not contours:
            print("❌ Could not detect game region automatically")
            return None

        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Filter out too small or too large regions
        screen_area = screen.shape[0] * screen.shape[1]
        contour_area = w * h

        if contour_area < screen_area * 0.1 or contour_area > screen_area * 0.95:
            print("⚠️  Detected region seems incorrect, using manual selection fallback")
            return self._manual_region_selection(screen)

        # Add some padding
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(screen.shape[1] - x, w + 2 * padding)
        h = min(screen.shape[0] - y, h + 2 * padding)

        region = {
            'top': y,
            'left': x,
            'width': w,
            'height': h
        }

        if debug:
            # Draw rectangle on screen
            debug_img = screen.copy()
            cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.imshow('Detected Game Region', cv2.cvtColor(debug_img, cv2.COLOR_RGB2BGR))
            cv2.waitKey(2000)
            cv2.destroyAllWindows()

        print(f"✓ Game region detected: {w}x{h} at ({x}, {y})")

        self.game_region = region
        return region

    def _manual_region_selection(self, screen):
        """
        Fallback method for manual region selection.

        Args:
            screen: Screenshot to select from

        Returns:
            Dict with game region coordinates
        """
        print("\n📍 Manual Region Selection")
        print("Click and drag to select the game area, then press ENTER")
        print("Press 'r' to reset, 'q' to quit")

        # This would open an interactive window
        # For now, return a default centered region
        h, w = screen.shape[:2]
        default_width = int(w * 0.6)
        default_height = int(h * 0.7)
        default_x = (w - default_width) // 2
        default_y = (h - default_height) // 2

        region = {
            'top': default_y,
            'left': default_x,
            'width': default_width,
            'height': default_height
        }

        print(f"Using default centered region: {default_width}x{default_height}")
        return region

    def capture_game(self, resize_to=(84, 84)):
        """
        Capture the game region and preprocess for AI.

        Args:
            resize_to: Tuple (width, height) to resize to

        Returns:
            Preprocessed game frame as numpy array
        """
        if self.game_region is None:
            self.detect_game_region()

        # Capture game region
        frame = self.capture_screen(self.game_region)

        # Preprocess: resize and normalize
        if resize_to:
            frame = cv2.resize(frame, resize_to, interpolation=cv2.INTER_AREA)

        # Convert to grayscale to reduce dimensionality
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Normalize to [0, 1]
        frame = frame.astype(np.float32) / 255.0

        return frame

    def set_game_region(self, region):
        """
        Manually set the game region.

        Args:
            region: Dict with {'top', 'left', 'width', 'height'}
        """
        self.game_region = region
        print(f"✓ Game region set: {region['width']}x{region['height']} at ({region['left']}, {region['top']})")

    def show_capture(self, duration=5):
        """
        Display what the AI sees for debugging.

        Args:
            duration: How long to show in seconds
        """
        if self.game_region is None:
            print("⚠️  No game region detected yet")
            return

        print(f"Showing capture for {duration} seconds...")
        start_time = time.time()

        while time.time() - start_time < duration:
            frame = self.capture_game(resize_to=None)

            # Display
            cv2.imshow('AI Vision', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Test the screen capture
    capture = ScreenCapture()

    # Try to detect game region
    region = capture.detect_game_region(debug=True)

    if region:
        # Show what the AI sees
        capture.show_capture(duration=5)

        # Capture and show preprocessed frame
        frame = capture.capture_game()
        print(f"Preprocessed frame shape: {frame.shape}")
        print(f"Frame value range: [{frame.min():.2f}, {frame.max():.2f}]")
