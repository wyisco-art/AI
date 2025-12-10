"""
Quick start script for Slope AI.
Easy-to-use interface for first-time users.
"""
import sys
import os


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 70)
    print(" " * 20 + "🎮 SLOPE AI QUICK START 🎮")
    print("=" * 70)


def print_menu():
    """Print main menu."""
    print("\nWhat would you like to do?")
    print("\n1. Test Setup (verify game detection)")
    print("2. Train New AI")
    print("3. Continue Training (from checkpoint)")
    print("4. Watch AI Play (use trained model)")
    print("5. Quick Training (100 episodes)")
    print("6. Exit")
    print("\nChoice: ", end="")


def test_setup():
    """Test the setup by detecting game region."""
    print("\n" + "=" * 70)
    print("TESTING SETUP")
    print("=" * 70)
    print("\nMake sure:")
    print("1. Slope game is open in your browser")
    print("2. Game is visible and not minimized")
    print("3. Browser window is reasonably large")
    print("\nPress Enter when ready...", end="")
    input()

    from game_environment import SlopeGameEnvironment

    env = SlopeGameEnvironment()
    success = env.setup(auto_detect=True)

    if success:
        print("\n✓ Setup successful!")
        print("\nShowing what the AI sees for 5 seconds...")
        env.screen_capture.show_capture(duration=5)
        env.close()
        return True
    else:
        print("\n❌ Setup failed!")
        print("\nTroubleshooting tips:")
        print("- Make sure game is fully visible")
        print("- Try maximizing the browser window")
        print("- Ensure game has good contrast")
        return False


def train_new():
    """Start training a new model."""
    print("\n" + "=" * 70)
    print("TRAIN NEW AI")
    print("=" * 70)

    print("\nHow many episodes? (default: 1000): ", end="")
    episodes = input().strip()
    episodes = episodes if episodes else "1000"

    print("\nDisable rendering for faster training? (y/n, default: n): ", end="")
    no_render = input().strip().lower() == 'y'

    print("\n⚠️  Make sure:")
    print("1. Game is open and visible")
    print("2. Game window will stay in focus")
    print("3. You won't use keyboard during training")
    print("\nPress Enter to start training...", end="")
    input()

    # Build command
    cmd = f"python train.py --episodes {episodes}"
    if no_render:
        cmd += " --no-render"

    print(f"\nRunning: {cmd}\n")
    os.system(cmd)


def continue_training():
    """Continue training from checkpoint."""
    print("\n" + "=" * 70)
    print("CONTINUE TRAINING")
    print("=" * 70)

    # List available checkpoints
    if os.path.exists('checkpoints'):
        files = [f for f in os.listdir('checkpoints') if f.endswith('.pth')]
        if files:
            print("\nAvailable checkpoints:")
            for i, f in enumerate(files, 1):
                print(f"{i}. {f}")

            print("\nEnter checkpoint number (or full path): ", end="")
            choice = input().strip()

            try:
                idx = int(choice) - 1
                checkpoint = os.path.join('checkpoints', files[idx])
            except (ValueError, IndexError):
                checkpoint = choice

            print(f"\nHow many more episodes? (default: 500): ", end="")
            episodes = input().strip()
            episodes = episodes if episodes else "500"

            cmd = f"python train.py --load {checkpoint} --episodes {episodes}"
            print(f"\nRunning: {cmd}\n")
            os.system(cmd)
        else:
            print("\n❌ No checkpoints found!")
    else:
        print("\n❌ No checkpoints directory found!")


def watch_play():
    """Watch trained AI play."""
    print("\n" + "=" * 70)
    print("WATCH AI PLAY")
    print("=" * 70)

    # List available checkpoints
    if os.path.exists('checkpoints'):
        files = [f for f in os.listdir('checkpoints') if f.endswith('.pth')]
        if files:
            print("\nAvailable checkpoints:")
            for i, f in enumerate(files, 1):
                print(f"{i}. {f}")

            print("\nEnter checkpoint number (or full path): ", end="")
            choice = input().strip()

            try:
                idx = int(choice) - 1
                checkpoint = os.path.join('checkpoints', files[idx])
            except (ValueError, IndexError):
                checkpoint = choice

            print(f"\nHow many episodes to watch? (default: 5): ", end="")
            episodes = input().strip()
            episodes = episodes if episodes else "5"

            cmd = f"python play.py {checkpoint} --episodes {episodes}"
            print(f"\nRunning: {cmd}\n")
            os.system(cmd)
        else:
            print("\n❌ No checkpoints found! Train a model first.")
    else:
        print("\n❌ No checkpoints directory found! Train a model first.")


def quick_training():
    """Quick training session (100 episodes)."""
    print("\n" + "=" * 70)
    print("QUICK TRAINING (100 episodes)")
    print("=" * 70)

    print("\n⚠️  Make sure:")
    print("1. Game is open and visible")
    print("2. Game window will stay in focus")
    print("\nPress Enter to start...", end="")
    input()

    cmd = "python train.py --episodes 100"
    print(f"\nRunning: {cmd}\n")
    os.system(cmd)


def main():
    """Main function."""
    print_banner()

    print("\n👋 Welcome to Slope AI!")
    print("\nThis AI learns to play the Slope game using Deep Reinforcement Learning.")

    while True:
        print_menu()

        try:
            choice = input().strip()

            if choice == '1':
                test_setup()
            elif choice == '2':
                train_new()
            elif choice == '3':
                continue_training()
            elif choice == '4':
                watch_play()
            elif choice == '5':
                quick_training()
            elif choice == '6':
                print("\n👋 Goodbye!\n")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice! Please enter 1-6.")

            print("\nPress Enter to continue...", end="")
            input()

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nPress Enter to continue...", end="")
            input()


if __name__ == "__main__":
    main()
