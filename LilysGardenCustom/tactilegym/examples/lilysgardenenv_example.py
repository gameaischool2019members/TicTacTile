import gym
import tactilegym
import pandas as pd
import numpy as np
import time

if __name__ == "__main__":
    env = gym.make('lg-v0', level=1)

    obs_space = env.observation_space
    print(obs_space.shape)
    print(env.level)
    # Get action space
    act_space = env.action_space

    # Set seed for reproducibility
    seed = 42
    env.seed(seed)

    # Play games
    steps = 0
    rewards = []
    times = []
    for i in range(100):

        # Reset environment
        obs = env.reset()
        done = False
        start_time = time.time()
        # Take actions as long as game is not done
        while not done:
            # Sample random action type
            action = env.action_space.sample()

            # Gym step function
            obs, reward, done, info = env.step(action)
            steps += 1
            rewards.append(reward)
            # print(reward, env.current_progress, env.valid_steps, env.total_steps, action, )
            time_now = time.time()
            times.append(time_now - start_time)
            # Render
            env.render()

    print(time_now - start_time)

    print(steps, rewards)