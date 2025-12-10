"""
Play script for Slope AI.
Uses a trained model to play the game.
"""
import argparse
import time
from game_environment import SlopeGameEnvironment
from models.dqn_agent import DQNAgent


def play(checkpoint_path, episodes=5, render=True):
    """
    Play Slope using a trained agent.

    Args:
        checkpoint_path: Path to model checkpoint
        episodes: Number of episodes to play
        render: Whether to render the game
    """
    print("\n" + "=" * 70)
    print("🎮 SLOPE AI - PLAY MODE")
    print("=" * 70 + "\n")

    # Create environment
    print("🎮 Initializing environment...")
    env = SlopeGameEnvironment()

    # Setup environment
    if not env.setup(auto_detect=True):
        print("❌ Failed to setup environment!")
        return

    # Create agent
    print("\n🤖 Loading trained agent...")
    agent = DQNAgent(
        num_actions=env.get_action_space(),
        input_shape=env.get_observation_space(),
    )

    # Load checkpoint
    if not agent.load(checkpoint_path):
        print("❌ Failed to load checkpoint!")
        return

    # Set epsilon to 0 for pure exploitation
    agent.epsilon = 0.0

    print(f"\n▶️  Starting playback ({episodes} episodes)...")
    print("Press Ctrl+C to stop\n")

    try:
        for episode in range(1, episodes + 1):
            print(f"\n{'='*50}")
            print(f"Episode {episode}/{episodes}")
            print(f"{'='*50}")

            # Reset environment
            state = env.reset()
            episode_reward = 0
            step = 0

            while True:
                # Select action (no exploration)
                action = agent.select_action(state, training=False)

                # Take action
                next_state, reward, done, info = env.step(action)

                # Update
                state = next_state
                episode_reward += reward
                step += 1

                # Render
                if render:
                    env.render(state, action, reward)

                # Print progress
                if step % 100 == 0:
                    print(f"  Step {step}: Reward={episode_reward:.1f}, "
                          f"Action={env.controller.get_action_name(action)}")

                # Check if done
                if done:
                    break

            # Episode summary
            print(f"\n✓ Episode Complete!")
            print(f"  Steps: {step}")
            print(f"  Total Reward: {episode_reward:.2f}")

            # Wait before next episode
            if episode < episodes:
                print("\nStarting next episode in 3 seconds...")
                time.sleep(3)

    except KeyboardInterrupt:
        print("\n\n⚠️  Playback stopped by user!")

    finally:
        env.close()
        print("\n👋 Thanks for watching!\n")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Play Slope with trained AI')
    parser.add_argument('checkpoint', type=str,
                       help='Path to checkpoint file')
    parser.add_argument('--episodes', type=int, default=5,
                       help='Number of episodes to play (default: 5)')
    parser.add_argument('--no-render', action='store_true',
                       help='Disable rendering')

    args = parser.parse_args()

    play(
        checkpoint_path=args.checkpoint,
        episodes=args.episodes,
        render=not args.no_render
    )


if __name__ == "__main__":
    main()
