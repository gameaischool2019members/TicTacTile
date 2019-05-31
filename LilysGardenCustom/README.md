# Lily's Garden - Custom

An OpenAI gym setup for our Lily's Garden game.

The gyms can be runs using a local simulation, preferably in a docker container. The gym interface can then connect with it using http requests.

# Simulator Docker Container
See the `Simulator/README.md` file for instructions on getting the Lily's Garden simulator started.

# Setup Gym VirtualEnv
To get VirtualEnv setup and all dependencies installed run

    ./setup_venv.sh

# Activate Gym VirtualEnv

To activate the virtualenv, run

    source ./tactilegym/venv/bin/activate

# Lily's Garden OpenAI Gym
## Env
Lily's Garden is a match-3 type game. It consists of a flat gameboard of size (13, 9), with various. In order to complete a level, various collect goals have to be fulfilled.

The rewards are:

* +1 per objective collected (typically 40 per level)
* +10 for completing level
* -0.5 per turn taken
* +0.01 for valid action taken

A playthrough with a random agent can be tested with the following command:

    ./run-random-agent.sh

## Player agent

The goal of the player agent is to play through the levels. For this we use a Deep-Q Network (DQN) approach (see https://keon.io/deep-q-learning/).

We represent the gameboard in a (x, y, n_entities) array. This is then fed into a CNN in the DQN, and hopefully the agent will learn how to play the various levels.

The agent can be trained using the following command:

    ./train-agent.sh