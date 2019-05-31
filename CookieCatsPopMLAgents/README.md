# Cookie Cats Pop - Unity ml-agents

We integrated the Unity ml-agents toolkit into our bubble shooter Cookie Cats Pop.

The strategy we used is adapted from https://blogs.unity3d.com/2019/04/15/unity-ml-agents-toolkit-v0-8-faster-training-on-real-games/ :
* The observation is a 42x84 camera with the culling mask set to see only the bubbles
* The action space is a discrete value in the range [0,19] mapped to a firing angle from -80 to +80 degrees off vertical
* The reward/penalties are:
** -0.2 per turn taken
** +1 for completing the level
** -1 for losing the level (running out of moves)
** A progressive reward for clearing a cluster, scaled between 0.3 to 0.6 based on how far up the screen the hit was made
** A progressive penalty for placing a bubble lower than the current lowest row, starting at -0.1 with an additional -0.1 for each level below the original lowest row

To maximize the steps per second, the editor is run at 20x time scale, and also all animations of the bubble traveling up the screen were skipped.

The training hyperparameters are the same as the GridWorld example from the toolkit.

The level used for the first phase of training is very easy with the bubble colors being fixed as well as the position of the goal (kitten). Once the agent was able to reliably complete the level, the curriculum was expanded to include a variant where the position of the goal was random along the top row; however it didn't take long for the agent to adapt to this since clearing all clusters will lead to discovering the goal fairly quickly.
