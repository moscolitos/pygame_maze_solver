# Maze Game
## Description
This Python program implements a maze game using Pygame. The game generates a random maze using the depth-first search algorithm, and allows a player to navigate a blue ball from the starting point to the end goal. The game offers two modes of play: a single player mode where the user manually moves the ball through the maze, and a player versus AI mode where the user competes against an AI to solve the maze.

In the AI mode, the AI uses the A* algorithm to find the shortest path through the maze. The A* algorithm employs a heuristic to guess the distance from each cell to the end goal and uses these estimates to choose the most promising path to follow.

## Installation

Ensure that you have Python 3 installed on your machine.

Install Pygame by running the following command in your terminal:

pip install pygame

Download and extract the project files.

## Usage
To start the game, navigate to the directory containing the game files and run the following command in your terminal:

python maze_game.py

After the game has started, you will be prompted to choose a game mode. To select single player mode, press 1. To select player versus AI mode, press 2.

In single player mode, use the arrow keys to move the blue ball through the maze.

In player versus AI mode, use the arrow keys to move the blue ball while the red ball, controlled by the AI, moves automatically.

The game ends when the blue ball reaches the end of the maze.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
