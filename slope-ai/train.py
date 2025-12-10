"""
Main training script for Slope AI.
Trains a DQN agent to learn how to play Slope.
"""
import numpy as np
import time
import argparse
import os
from datetime import datetime
import matplotlib.pyplot as plt

from game_environment import SlopeGameEnvironment
from models.dqn_agent import DQNAgent


class Trainer:
    """Trainer for Slope AI."""

    def __init__(
        self,
        env,
        agent,
        num_episodes=1000,
        max_steps_per_episode=10000,
        save_frequency=10,
        render=True,
        checkpoint_dir='checkpoints'
    ):
        """
        Initialize trainer.

        Args:
            env: Game environment
            agent: DQN agent
            num_episodes: Number of episodes to train
            max_steps_per_episode: Maximum steps per episode
            save_frequency: Save model every N episodes
            render: Whether to render during training
            checkpoint_dir: Directory to save checkpoints
        """
        self.env = env
        self.agent = agent
        self.num_episodes = num_episodes
        self.max_steps_per_episode = max_steps_per_episode
        self.save_frequency = save_frequency
        self.render = render
        self.checkpoint_dir = checkpoint_dir

        # Create checkpoint directory
        os.makedirs(checkpoint_dir, exist_ok=True)

        # Training stats
        self.episode_rewards = []
        self.episode_lengths = []
        self.losses = []

    def train(self):
        """Main training loop."""
        print("\n" + "=" * 70)
        print("🎮 SLOPE AI TRAINING")
        print("=" * 70)
        print(f"Episodes: {self.num_episodes}")
        print(f"Max steps per episode: {self.max_steps_per_episode}")
        print(f"Checkpoint directory: {self.checkpoint_dir}")
        print("=" * 70 + "\n")

        start_time = time.time()
        best_reward = float('-inf')

        try:
            for episode in range(1, self.num_episodes + 1):
                episode_start_time = time.time()

                # Reset environment
                state = self.env.reset()
                episode_reward = 0
                episode_loss = []

                print(f"\n📍 Episode {episode}/{self.num_episodes}")
                print(f"   Epsilon: {self.agent.epsilon:.3f}")

                for step in range(self.max_steps_per_episode):
                    # Select action
                    action = self.agent.select_action(state, training=True)

                    # Take action
                    next_state, reward, done, info = self.env.step(action)

                    # Store experience
                    self.agent.store_experience(state, action, reward, next_state, done)

                    # Train agent
                    loss = self.agent.train_step()
                    if loss is not None:
                        episode_loss.append(loss)

                    # Update state
                    state = next_state
                    episode_reward += reward

                    # Render
                    if self.render:
                        self.env.render(state, action, reward)

                    # Check if done
                    if done:
                        break

                    # Print progress
                    if step % 100 == 0:
                        print(f"   Step {step}: Reward={episode_reward:.1f}, "
                              f"Action={self.env.controller.get_action_name(action)}")

                # Episode finished
                episode_time = time.time() - episode_start_time
                self.episode_rewards.append(episode_reward)
                self.episode_lengths.append(step + 1)

                # Calculate average loss
                avg_loss = np.mean(episode_loss) if episode_loss else 0
                self.losses.append(avg_loss)

                # Update epsilon
                self.agent.update_epsilon()
                self.agent.episodes_done = episode

                # Print episode summary
                print(f"\n✓ Episode {episode} Complete!")
                print(f"   Duration: {episode_time:.1f}s")
                print(f"   Steps: {step + 1}")
                print(f"   Total Reward: {episode_reward:.2f}")
                print(f"   Avg Loss: {avg_loss:.4f}")
                print(f"   Memory Size: {len(self.agent.memory)}")

                # Check if best episode
                if episode_reward > best_reward:
                    best_reward = episode_reward
                    print(f"   🌟 New Best Reward: {best_reward:.2f}!")
                    # Save best model
                    self.agent.save(self.checkpoint_dir, episode='best')

                # Save checkpoint
                if episode % self.save_frequency == 0:
                    self.agent.save(self.checkpoint_dir, episode=episode)
                    self._plot_progress()

                # Print average stats
                if episode >= 10:
                    avg_reward = np.mean(self.episode_rewards[-10:])
                    avg_length = np.mean(self.episode_lengths[-10:])
                    print(f"   📊 Last 10 Episodes - Avg Reward: {avg_reward:.2f}, "
                          f"Avg Length: {avg_length:.1f}")

        except KeyboardInterrupt:
            print("\n\n⚠️  Training interrupted by user!")

        finally:
            # Save final model
            print("\n💾 Saving final model...")
            self.agent.save(self.checkpoint_dir, episode='final')

            # Training summary
            total_time = time.time() - start_time
            print("\n" + "=" * 70)
            print("🏁 TRAINING COMPLETE")
            print("=" * 70)
            print(f"Total Episodes: {episode}")
            print(f"Total Time: {total_time/60:.1f} minutes")
            print(f"Best Reward: {best_reward:.2f}")
            print(f"Final Epsilon: {self.agent.epsilon:.3f}")
            print("=" * 70 + "\n")

            # Plot final results
            self._plot_progress()

            # Cleanup
            self.env.close()

    def _plot_progress(self):
        """Plot training progress."""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))

            # Episode rewards
            axes[0, 0].plot(self.episode_rewards)
            axes[0, 0].set_title('Episode Rewards')
            axes[0, 0].set_xlabel('Episode')
            axes[0, 0].set_ylabel('Total Reward')
            axes[0, 0].grid(True)

            # Moving average of rewards
            if len(self.episode_rewards) >= 10:
                moving_avg = np.convolve(self.episode_rewards,
                                        np.ones(10)/10, mode='valid')
                axes[0, 1].plot(moving_avg)
                axes[0, 1].set_title('Moving Average Reward (window=10)')
                axes[0, 1].set_xlabel('Episode')
                axes[0, 1].set_ylabel('Avg Reward')
                axes[0, 1].grid(True)

            # Episode lengths
            axes[1, 0].plot(self.episode_lengths)
            axes[1, 0].set_title('Episode Lengths')
            axes[1, 0].set_xlabel('Episode')
            axes[1, 0].set_ylabel('Steps')
            axes[1, 0].grid(True)

            # Losses
            if self.losses:
                axes[1, 1].plot(self.losses)
                axes[1, 1].set_title('Training Loss')
                axes[1, 1].set_xlabel('Episode')
                axes[1, 1].set_ylabel('Loss')
                axes[1, 1].grid(True)

            plt.tight_layout()

            # Save plot
            plot_path = os.path.join(self.checkpoint_dir, 'training_progress.png')
            plt.savefig(plot_path)
            print(f"📈 Progress plot saved to {plot_path}")

            plt.close()

        except Exception as e:
            print(f"⚠️  Could not save plot: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Train Slope AI')
    parser.add_argument('--episodes', type=int, default=1000,
                       help='Number of episodes to train (default: 1000)')
    parser.add_argument('--max-steps', type=int, default=10000,
                       help='Maximum steps per episode (default: 10000)')
    parser.add_argument('--no-render', action='store_true',
                       help='Disable rendering during training')
    parser.add_argument('--checkpoint-dir', type=str, default='checkpoints',
                       help='Directory to save checkpoints (default: checkpoints)')
    parser.add_argument('--load', type=str, default=None,
                       help='Load checkpoint from file')
    parser.add_argument('--learning-rate', type=float, default=0.00025,
                       help='Learning rate (default: 0.00025)')
    parser.add_argument('--epsilon-decay', type=float, default=0.995,
                       help='Epsilon decay rate (default: 0.995)')
    parser.add_argument('--memory-size', type=int, default=10000,
                       help='Replay memory size (default: 10000)')

    args = parser.parse_args()

    # Create environment
    print("🎮 Initializing Slope Game Environment...")
    env = SlopeGameEnvironment()

    # Setup environment (detect game region)
    if not env.setup(auto_detect=True):
        print("❌ Failed to setup environment!")
        print("Make sure the Slope game is visible on your screen.")
        return

    # Create agent
    print("\n🤖 Initializing DQN Agent...")
    agent = DQNAgent(
        num_actions=env.get_action_space(),
        input_shape=env.get_observation_space(),
        learning_rate=args.learning_rate,
        epsilon_decay=args.epsilon_decay,
        memory_size=args.memory_size,
    )

    # Load checkpoint if specified
    if args.load:
        agent.load(args.load)

    # Create trainer
    trainer = Trainer(
        env=env,
        agent=agent,
        num_episodes=args.episodes,
        max_steps_per_episode=args.max_steps,
        render=not args.no_render,
        checkpoint_dir=args.checkpoint_dir,
    )

    # Start training
    trainer.train()


if __name__ == "__main__":
    main()
