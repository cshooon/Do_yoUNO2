from collections import Counter

from matplotlib import pyplot as plt
from tqdm import tqdm

import config
from envs.uno_env import UNOEnv
import numpy as np


def main():

    env = UNOEnv()

    rewards = []
    episode_lengths = []
    coverage = []
    cumulative_wins = {'AI': [], 'Human': []}
    ai_wins = 0
    human_wins = 0
    iterations = 10000

    # Training loop
    for episode in tqdm(range(iterations), desc="Training Episodes"):
        state = env.reset()
        done = False
        total_reward = 0
        steps = 0
        if config.params['algorithm'] == 'q-learning':
            env.agent.initial_rewards()

        while not done:

            # action 선택, 수행, update, reward 포함
            next_state, reward, terminated, truncated, info = env.step(action=None)
            done = terminated or truncated

            total_reward += reward
            steps += 1

            env.render()

        if config.params['algorithm'] == 'monte-carlo':
            env.player_1.identify_state(env.turn.card_open)
            env.agent.update(env.player_1.state, env.player_1.action)

        winner = env.winner
        rewards.append(total_reward)
        episode_lengths.append(steps)
        coverage.append((env.agent.q != 0).values.sum())
        cumulative_wins['AI'].append(ai_wins)
        cumulative_wins['Human'].append(human_wins)

        # 승리 횟수 업데이트
        if winner == 'AI':
            ai_wins += 1
        elif winner == 'Human':
            human_wins += 1

        # Output training results
        print("Training completed.")
        print("Average reward:", np.mean(rewards))
        print("Average episode length:", np.mean(episode_lengths))

    # Plot results
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(rewards, label='Rewards')
    plt.title('Rewards per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(episode_lengths, label='Episode Length')
    plt.title('Episode Lengths per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Length')
    plt.legend()

    plt.tight_layout()
    plt.savefig('reward_episode_length.png')
    plt.show()

    # 승리 추이 시각화
    plt.figure(figsize=(12, 6))
    episode_numbers = range(1, len(cumulative_wins['AI']) + 1)
    win_rate_ai = np.array(cumulative_wins['AI']) / episode_numbers
    win_rate_human = np.array(cumulative_wins['Human']) / episode_numbers
    plt.plot(episode_numbers, win_rate_ai, label='AI Win Rate')
    plt.plot(episode_numbers, win_rate_human, label='Human Win Rate')
    plt.xlabel('Episode')
    plt.ylabel('Win Rate')
    plt.title('Win Rate per Player Over Episodes')
    plt.legend()
    plt.savefig('win_rate.png')
    plt.show()

    # Coverage 시각화
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, iterations + 1), coverage, marker='o', linestyle='-', color='b')
    plt.title('Q-table Coverage Over Episodes')
    plt.xlabel('Episode')
    plt.ylabel('Number of Non-Zero Entries in Q-table')
    plt.grid(True)
    plt.savefig('coverage.png')
    plt.show()


if __name__ == "__main__":
    main()
