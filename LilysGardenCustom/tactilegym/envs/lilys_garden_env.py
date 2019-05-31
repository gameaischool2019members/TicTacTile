import colorsys
import json
import math
import numpy as np
import pandas as pd
import tkinter as tk
import time
import gym

from gym import error, spaces, utils
from gym.utils import seeding
from .simulator import Simulator


class LilysGardenEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, board_size=(13, 9), level=1):
        """The gym environment for Lily's Garden.
        Example of starting env: env = gym.make('lg-v0', level=1)


        Parameters
        ----------
        board_size: tuple
            game board size, (x, y)
        level: int

        Returns
        -------

        """
        self._sessionId = None
        self.board_state = None
        self._seed = None
        self.level = level
        self.board_size = board_size
        self.current_progress = 0
        self.valid_steps = 0
        self.total_steps = 0
        self.last_action = None
        self.entity_layer = self._create_entity_layer()

        self.root = None
        self._simulator = Simulator('http://localhost:8090')

        max_entity_hp = 20

        self.observation_space = spaces.Box(low=0,
                                            high=max_entity_hp,
                                            shape=(board_size[0], board_size[1], len(self.entity_layer) + 1),
                                            dtype=np.uint8)
        self.action_space = spaces.Discrete(board_size[0] * board_size[1])
        self.last_observation = None
        self.layer_colors = self._get_n_hex_colors(self.observation_space.shape[-1])

        self.timings = {x: [] for x in ['actcoord',
                                        'actjson',
                                        'response',
                                        'setstates',
                                        'getobs',
                                        'calcprog']}

    def step(self, action):
        time_start = time.time()
        coords = self._action_to_coord(action)
        time_now = time.time()
        self.timings['actcoord'].append(time_now - time_start)
        time_now = time.time()

        result = self._simulator.session_click(self._session_id, coords['x'], coords['y'])

        self.timings['response'].append(time.time() - time_now)
        time_now = time.time()

        self.valid_steps += 1 * (result['clickSuccessful'])
        self.total_steps += 1
        self.last_action = action
        self.board_state = json.loads(result['sparseState'])
        self.timings['setstates'].append(time.time() - time_now)
        time_now = time.time()
        observation = self._observation_from_state()
        self.timings['getobs'].append(time.time() - time_now)

        time_now = time.time()
        new_progress = self._calculate_progress()
        self.timings['calcprog'].append(time.time() - time_now)

        reward = -(new_progress - self.current_progress) - 0.1 + 0.2 * (result['clickSuccessful'])
        self.current_progress = new_progress

        goal_reached = self.current_progress >= 1.0

        self.last_observation = observation

        # print([f"{x}: {y[-1]}" for x, y in self.timings.items()])

        return observation, reward, goal_reached, {}

    def reset(self):
        if (self._sessionId != None):
            print("destroying sesssion - sessionId={0}".format(self._sessionId))
            result = self._simulator.session_destroy(self._sessionId)
            print("destroyed={0}".format(result['destroyed']))
            self._sessionId = None

        self.valid_steps = 0

        result = self._simulator.load(0, self._seed)

        # print(result["state"])
        # print(result["sparseState"])

        board_state_full = json.loads(result['state']);
        self.board_state = json.loads(result['sparseState']);

        self.current_progress = self._calculate_progress()

        result = self._simulator.session_create(board_state_full)
        self._session_id = result['sessionId']

        return self._observation_from_state()

    def render(self, mode='human', feature_layers=True):

        square_size = 32
        square_size_fl = 8
        top_bar_height = 42
        bot_bar_height = 80
        layer_text_height = 26

        if self.root is None:
            self.root = tk.Tk()
            self.root.title("LG Gym")
            self.game_width = max(500, self.board_size[0] * square_size)
            self.game_height = self.board_size[1] * square_size + top_bar_height + bot_bar_height
            if feature_layers:
                self.cols = math.floor(math.sqrt(self.observation_space.shape[2]))
                self.rows = math.ceil(math.sqrt(self.observation_space.shape[2]))
                self.fl_width = (self.board_size[0] + 1) * self.cols * square_size_fl + square_size_fl
                self.fl_height = ((self.board_size[1] + 1) * square_size_fl + layer_text_height) * \
                                 self.rows + square_size_fl
                self.cv = tk.Canvas(width=max(self.game_width, self.fl_width),
                                    height=self.fl_height + self.game_height,
                                    master=self.root)
            else:
                self.cv = tk.Canvas(width=self.game_width, height=self.game_height, master=self.root)

        self.cv.pack(side='top', fill='both', expand='yes')
        self.cv.delete("all")
        self.root.configure(background='black')

        x_size = self.board_size[0]
        y_size = self.board_size[1]

        if self.last_observation is not None:
            # Squares
            for y in range(y_size):
                for x in range(x_size):
                    self.cv.create_rectangle(square_size * x,
                                             square_size * y + top_bar_height,
                                             square_size * x + square_size,
                                             square_size * y + square_size + top_bar_height,
                                             fill='#000000',
                                             outline='#ffffff')

            self.cv.create_line(self.board_size[0] * square_size / 2.0 - 1,
                                top_bar_height,
                                self.board_size[0] * square_size / 2.0 - 1,
                                self.board_size[1] * square_size + top_bar_height,
                                fill='#000000', width=2)

            # Non-spatial
            self.cv.create_text(x_size * square_size / 2.0, 10,
                                text=f'{self._action_to_coord(self.last_action)}',
                                fill='black')

        # Feature layers
        if feature_layers:
            row = 0
            col = 0
            for layer_idx in range(self.observation_space.shape[-1]):
                if layer_idx > 0:
                    name = list(self.entity_layer.keys())[layer_idx - 1]
                else:
                    name = "Base layer"
                # for name, grid in self.last_obs['board'].items():
                grid_x = col * (x_size + 1) * square_size_fl + square_size_fl
                grid_y = row * (y_size + 1) * square_size_fl + self.game_height + square_size_fl + (
                        (row + 1) * layer_text_height)

                self.cv.create_text(grid_x + (x_size * square_size_fl) / 2,
                                    grid_y - layer_text_height / 2, text=name)
                self.cv.create_rectangle(grid_x,
                                         grid_y,
                                         grid_x + x_size * square_size_fl,
                                         grid_y + y_size * square_size_fl,
                                         fill='black', outline='#000000', width=2)
                for y in range(y_size):
                    for x in range(x_size):
                        value = 1 - self.last_observation[x][y][layer_idx]
                        fill = '#%02x%02x%02x' % (int(value * 255), int(value * 255), int(value * 255))
                        self.cv.create_rectangle(square_size_fl * x + grid_x,
                                                 square_size_fl * y + grid_y,
                                                 square_size_fl * x + grid_x + square_size_fl,
                                                 square_size_fl * y + grid_y + square_size_fl,
                                                 fill=fill, outline='#000000')
                        if value == 0:
                            self.cv.create_rectangle(square_size * x,
                                                     square_size * y + top_bar_height,
                                                     square_size * x + square_size,
                                                     square_size * y + square_size + top_bar_height,
                                                     fill=self.layer_colors[layer_idx],
                                                     outline='#ffffff')
                if self.last_action is not None:
                    action = self._action_to_index(self.last_action)
                    self.cv.create_rectangle(square_size_fl * action['idx'] + grid_x,
                                             square_size_fl * action['idy'] + grid_y,
                                             square_size_fl * action['idx'] + grid_x + square_size_fl / 2,
                                             square_size_fl * action['idy'] + grid_y + square_size_fl / 2,
                                             fill='#ffffff',
                                             outline='#ffffff')
                col += 1
                if col >= self.cols:
                    col = 0
                    row += 1

        if self.last_action is not None:
            action = self._action_to_index(self.last_action)
            self.cv.create_rectangle(square_size * action['idx'],
                                     square_size * action['idy'] + top_bar_height,
                                     square_size * action['idx'] + square_size / 2,
                                     square_size * action['idy'] + square_size / 2 + top_bar_height,
                                     fill='#ffffff',
                                     outline='#ffffff')
        self.root.update_idletasks()
        self.root.update()

    def close(self):
        ...

    def seed(self, seed=None):
        if seed is None:
            self._seed = seeding.hash_seed(np.random.randint(0, 2 ** 31))
        np.random.seed(self._seed)
        return [self._seed]

    def _action_to_coord(self, action):
        indexes = self._action_to_index(action)
        return {'x': int(indexes['idx'] - self.board_size[0] // 2), 'y': int(indexes['idy'] - self.board_size[1] // 2)}

    def _action_to_index(self, action):
        return {'idx': action % self.board_size[0], 'idy': action // self.board_size[0]}

    def _coord_to_index(self, x, y):
        return {'idx': x + self.board_size[0] // 2, 'idy': y + self.board_size[1] // 2}

    def _coord_to_action(self, x, y):
        return self._index_to_action(**self._coord_to_index(x, y))

    def _index_to_action(self, idx, idy):
        return idx + idy * self.board_size[0]

    def _index_to_coord(self, idx, idy):
        return {'x': idx - self.board_size[0] // 2, 'y': idy - self.board_size[1] // 2}

    def _observation_from_state(self):
        observation = np.zeros(self.observation_space.shape)
        idx = 0
        for pieces in self.board_state['board']:
            idxs = self._action_to_index(idx)
            if pieces:
                observation[idxs['idx'], idxs['idy'], 0] = 1
                for piece in pieces:
                    layer_idx = self.entity_layer[piece]
                    observation[idxs['idx'], idxs['idy'], layer_idx] = 1

            idx += 1
        return observation

    def _calculate_progress(self):
        progress = sum(self.board_state['goal'].values())
        return progress

    def _create_entity_layer(self):
        entities = [
            'Bomb',
            'CookieRed',
            'CookieGreen',
            'CookieBlue',
            'CookieYellow',
            'CookiePink',
            'CookiePurple',
            'MagicRed',
            'MagicGreen',
            'MagicBlue',
            'MagicYellow',
            'MagicPink',
            'MagicPurple',
            'RocketHorizontal'
            'RocketVertical',
        ]

        entity_layer = {entities[idx]: idx + 1 for idx in range(len(entities))}
        return entity_layer

    def _get_n_hex_colors(self, n=5):
        HSV_tuples = [(x * 1.0 / n, 1.0, 1.0) for x in range(n)]
        hex_values = []
        for rgb in HSV_tuples:
            rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
            hex_values.append('#%02x%02x%02x' % tuple(rgb))
            np.random.shuffle(hex_values)
        return hex_values
