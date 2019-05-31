from gym.envs.registration import register

register(
    id='lg-v0',
    entry_point='tactilegym.envs:LilysGardenEnv',
    kwargs={'level': 1}
)