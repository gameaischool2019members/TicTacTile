# TicTacTile

## Overview

Tactile Games produce a number of popular F2P puzzle games. These games all receive new levels on a weekly basis which means that new levels need to be designed and play-tested to ensure that they provide the wanted difficulty level. This means that level designers are required to play each level numerous times to tweak the number of available moves provided in a level. 

One way to improve this significant on-going production cost would be to have AI based player agents that could perform play testing of levels to provide a difficulty benchmark for newly produced levels.

Inspired by the talks given during the Game AI summer school we have attempted a couple of different ways of implementing player agents for 2 of our games.

### Cookie Cats Pop - Unity ml-agents

- [Google Play](https://play.google.com/store/apps/details?id=dk.tactile.cookiecatspop&hl=en_US)
- [App Store](https://itunes.apple.com/us/app/cookie-cats-pop/id1159705605)

Cookie Cats Pop is a bubble shooter puzzle game. For this game it is not possible for us to easily decouple the graphics from the logic, so we have attempted to make a solution using ml-agents

### Lily's Garden - Custom

- [Google Play](https://play.google.com/store/apps/details?id=dk.tactile.lilysgarden&hl=en_US)
- [App Store](https://itunes.apple.com/us/app/lilys-garden/id1437783446)

Lily's Garden is a collapse-style puzzle game. For this game we are able to completely decouple the logic from the graphics and just execute the game board simulation without any graphics. We have exploited this by creating a special Linux build of Lily's Garden where the game runs a simple HTTP web server that allows an external agent to interface with the game by performing HTTP requests againt the game.

We have written a OpenAI Gym based environment in Python that communicates with the simulator and we have then written an agent that uses the Lily's Garden Gym environment.

### Lily's Garden - Unity ml-agents

To contrast the custom solution, we have also attempted to create a solution based on Unity ml-agents for Lily's Garden.