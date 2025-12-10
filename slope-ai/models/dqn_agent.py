"""
Deep Q-Network (DQN) agent for learning to play Slope.
Uses convolutional neural network to process game frames.
"""
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque, namedtuple
import os


# Experience tuple for replay memory
Experience = namedtuple('Experience', ['state', 'action', 'reward', 'next_state', 'done'])


class DQN(nn.Module):
    """Deep Q-Network architecture for processing game frames."""

    def __init__(self, input_shape=(4, 84, 84), num_actions=3):
        """
        Initialize DQN.

        Args:
            input_shape: Shape of input (channels, height, width)
            num_actions: Number of possible actions
        """
        super(DQN, self).__init__()

        self.conv1 = nn.Conv2d(input_shape[0], 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)

        # Calculate size after convolutions
        def conv2d_size_out(size, kernel_size, stride):
            return (size - kernel_size) // stride + 1

        convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(input_shape[1], 8, 4), 4, 2), 3, 1)
        convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(input_shape[2], 8, 4), 4, 2), 3, 1)
        linear_input_size = convw * convh * 64

        self.fc1 = nn.Linear(linear_input_size, 512)
        self.fc2 = nn.Linear(512, num_actions)

    def forward(self, x):
        """Forward pass through network."""
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class ReplayMemory:
    """Experience replay memory for DQN."""

    def __init__(self, capacity=10000):
        """
        Initialize replay memory.

        Args:
            capacity: Maximum number of experiences to store
        """
        self.memory = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """Add experience to memory."""
        self.memory.append(Experience(state, action, reward, next_state, done))

    def sample(self, batch_size):
        """Sample a batch of experiences."""
        return random.sample(self.memory, batch_size)

    def __len__(self):
        """Get current memory size."""
        return len(self.memory)


class DQNAgent:
    """DQN agent that learns to play Slope."""

    def __init__(
        self,
        num_actions=3,
        input_shape=(4, 84, 84),
        learning_rate=0.00025,
        gamma=0.99,
        epsilon_start=1.0,
        epsilon_end=0.1,
        epsilon_decay=0.995,
        memory_size=10000,
        batch_size=32,
        target_update=1000,
        device=None
    ):
        """
        Initialize DQN agent.

        Args:
            num_actions: Number of possible actions
            input_shape: Shape of input frames
            learning_rate: Learning rate for optimizer
            gamma: Discount factor for future rewards
            epsilon_start: Starting exploration rate
            epsilon_end: Minimum exploration rate
            epsilon_decay: Decay rate for exploration
            memory_size: Size of replay memory
            batch_size: Batch size for training
            target_update: Steps between target network updates
            device: Device to run on (cuda/cpu)
        """
        self.num_actions = num_actions
        self.input_shape = input_shape
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update = target_update

        # Device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = device

        print(f"🖥️  Using device: {self.device}")

        # Networks
        self.policy_net = DQN(input_shape, num_actions).to(self.device)
        self.target_net = DQN(input_shape, num_actions).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        # Optimizer
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=learning_rate)

        # Replay memory
        self.memory = ReplayMemory(memory_size)

        # Training stats
        self.steps_done = 0
        self.episodes_done = 0
        self.total_reward = 0
        self.losses = []

    def select_action(self, state, training=True):
        """
        Select action using epsilon-greedy policy.

        Args:
            state: Current state (numpy array or torch tensor)
            training: Whether in training mode (uses exploration)

        Returns:
            Action index
        """
        if training and random.random() < self.epsilon:
            # Random action (exploration)
            return random.randrange(self.num_actions)
        else:
            # Greedy action (exploitation)
            with torch.no_grad():
                if isinstance(state, np.ndarray):
                    state = torch.FloatTensor(state).unsqueeze(0).to(self.device)

                q_values = self.policy_net(state)
                return q_values.max(1)[1].item()

    def store_experience(self, state, action, reward, next_state, done):
        """Store experience in replay memory."""
        self.memory.push(state, action, reward, next_state, done)

    def train_step(self):
        """Perform one training step (batch update)."""
        if len(self.memory) < self.batch_size:
            return None

        # Sample batch
        experiences = self.memory.sample(self.batch_size)
        batch = Experience(*zip(*experiences))

        # Convert to tensors
        state_batch = torch.FloatTensor(np.array(batch.state)).to(self.device)
        action_batch = torch.LongTensor(batch.action).unsqueeze(1).to(self.device)
        reward_batch = torch.FloatTensor(batch.reward).unsqueeze(1).to(self.device)
        next_state_batch = torch.FloatTensor(np.array(batch.next_state)).to(self.device)
        done_batch = torch.FloatTensor(batch.done).unsqueeze(1).to(self.device)

        # Compute Q(s, a)
        q_values = self.policy_net(state_batch).gather(1, action_batch)

        # Compute V(s') for all next states
        with torch.no_grad():
            next_q_values = self.target_net(next_state_batch).max(1)[0].unsqueeze(1)
            expected_q_values = reward_batch + (1 - done_batch) * self.gamma * next_q_values

        # Compute loss
        loss = F.smooth_l1_loss(q_values, expected_q_values)

        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        # Clip gradients
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 1.0)
        self.optimizer.step()

        # Update target network
        self.steps_done += 1
        if self.steps_done % self.target_update == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        self.losses.append(loss.item())
        return loss.item()

    def update_epsilon(self):
        """Decay exploration rate."""
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)

    def save(self, path, episode=None):
        """
        Save model checkpoint.

        Args:
            path: Directory to save to
            episode: Optional episode number
        """
        os.makedirs(path, exist_ok=True)

        filename = f"dqn_checkpoint_ep{episode}.pth" if episode else "dqn_checkpoint.pth"
        filepath = os.path.join(path, filename)

        checkpoint = {
            'policy_net_state_dict': self.policy_net.state_dict(),
            'target_net_state_dict': self.target_net.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'steps_done': self.steps_done,
            'episodes_done': self.episodes_done,
        }

        torch.save(checkpoint, filepath)
        print(f"💾 Model saved to {filepath}")

    def load(self, filepath):
        """
        Load model checkpoint.

        Args:
            filepath: Path to checkpoint file
        """
        if not os.path.exists(filepath):
            print(f"⚠️  Checkpoint not found: {filepath}")
            return False

        checkpoint = torch.load(filepath, map_location=self.device)

        self.policy_net.load_state_dict(checkpoint['policy_net_state_dict'])
        self.target_net.load_state_dict(checkpoint['target_net_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint['epsilon']
        self.steps_done = checkpoint['steps_done']
        self.episodes_done = checkpoint['episodes_done']

        print(f"✓ Model loaded from {filepath}")
        print(f"  Episodes: {self.episodes_done}, Steps: {self.steps_done}, Epsilon: {self.epsilon:.3f}")
        return True

    def get_stats(self):
        """Get training statistics."""
        return {
            'episodes': self.episodes_done,
            'steps': self.steps_done,
            'epsilon': self.epsilon,
            'memory_size': len(self.memory),
            'avg_loss': np.mean(self.losses[-100:]) if self.losses else 0,
        }


if __name__ == "__main__":
    # Test the agent
    print("Testing DQN Agent...")

    agent = DQNAgent()
    print(f"\n📊 Agent initialized:")
    print(f"  Actions: {agent.num_actions}")
    print(f"  Input shape: {agent.input_shape}")
    print(f"  Device: {agent.device}")

    # Test forward pass
    dummy_state = np.random.random((4, 84, 84)).astype(np.float32)
    action = agent.select_action(dummy_state)
    print(f"\n🎮 Action selected: {action}")

    # Test experience storage
    agent.store_experience(dummy_state, action, 1.0, dummy_state, False)
    print(f"📝 Experience stored. Memory size: {len(agent.memory)}")

    print("\n✓ Agent test complete!")
