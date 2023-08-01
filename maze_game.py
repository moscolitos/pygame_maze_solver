# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 20:58:49 2023

@author: Mosco


This Python script generates a maze using Pygame, and allows the user to navigate a ball through it. 
The user can choose between single player mode and player vs AI mode.

In single player mode, the user navigates the ball through the maze using the arrow keys. 

In player vs AI mode, the user navigates their own ball through the maze using the arrow keys 
while an AI navigates its own ball through the maze following the shortest path.

The maze is generated using a depth-first search algorithm, 
and the shortest path is determined using the A* search algorithm.

"""
import pygame
import random
import sys

# Screen dimensions
WIDTH = 800
HEIGHT = 800

# Maze dimensions
ROWS = 20
COLS = 20

# Cell dimensions
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialize Pygame
# pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


class Cell:
    """
    The Cell class represents a cell in the maze. Each cell knows its row and column index in the grid, 
    whether it has walls on each side, and whether it has been visited in the maze generation algorithm.
    """

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def draw(self):
        x = self.col * CELL_WIDTH
        y = self.row * CELL_HEIGHT

        if self.walls["top"]:
            pygame.draw.line(SCREEN, WHITE, (x, y), (x + CELL_WIDTH, y))
        if self.walls["right"]:
            pygame.draw.line(SCREEN, WHITE, (x + CELL_WIDTH, y),
                             (x + CELL_WIDTH, y + CELL_HEIGHT))
        if self.walls["bottom"]:
            pygame.draw.line(SCREEN, WHITE, (x + CELL_WIDTH,
                             y + CELL_HEIGHT), (x, y + CELL_HEIGHT))
        if self.walls["left"]:
            pygame.draw.line(SCREEN, WHITE, (x, y + CELL_HEIGHT), (x, y))

    def get_neighbours(self, grid):
        neighbours = []

        if self.row > 0 and not self.walls["top"]:
            neighbours.append(grid[self.row - 1][self.col])
        if self.col < COLS - 1 and not self.walls["right"]:
            neighbours.append(grid[self.row][self.col + 1])
        if self.row < ROWS - 1 and not self.walls["bottom"]:
            neighbours.append(grid[self.row + 1][self.col])
        if self.col > 0 and not self.walls["left"]:
            neighbours.append(grid[self.row][self.col - 1])

        return neighbours

# We'll continue from here...


class Ball:
    """
    The Ball class represents the ball that navigates through the maze. 
    The ball knows its x and y coordinates 
    on the screen, which grid it belongs to, its color, and how many moves it has made.
    """

    def __init__(self, x, y, grid, color):
        self.x = x
        self.y = y
        self.grid = grid
        self.radius = CELL_WIDTH // 2 - 1
        self.color = color
        self.moves = 0  # New attribute

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)

    def can_move(self, dx, dy):
        # Get the current cell and the neighboring cell in the direction of the move
        cell = self.grid[self.y // CELL_HEIGHT][self.x // CELL_WIDTH]
        if dx > 0:
            neighbour = self.grid[cell.row][min(cell.col + 1, COLS - 1)]
            return not cell.walls["right"] and not neighbour.walls["left"]

        elif dx < 0:
            neighbour = self.grid[cell.row][max(cell.col - 1, 0)]
            return not cell.walls["left"] and not neighbour.walls["right"]
        elif dy > 0:
            neighbour = self.grid[min(cell.row + 1, ROWS - 1)][cell.col]
            return not cell.walls["bottom"] and not neighbour.walls["top"]
        elif dy < 0:
            neighbour = self.grid[max(cell.row - 1, 0)][cell.col]
            return not cell.walls["top"] and not neighbour.walls["bottom"]


class MazeSolver:
    """
    The MazeSolver class is responsible for finding the shortest path from the start cell to the goal 
    cell. It uses the A* search algorithm.
    """

    def __init__(self, start, goal, grid):
        self.start = start
        self.goal = goal
        self.grid = grid
        self.open_set = [start]
        self.closed_set = []
        self.came_from = {}
        self.g_score = {cell: float("inf") for row in grid for cell in row}
        self.g_score[start] = 0
        self.f_score = {cell: float("inf") for row in grid for cell in row}
        self.f_score[start] = self.heuristic(start)

    def heuristic(self, cell):
        return abs(cell.row - self.goal.row) + abs(cell.col - self.goal.col)

    def reconstruct_path(self):
        path = []
        current = self.goal
        while current in self.came_from:
            path.append(current)
            current = self.came_from[current]
        return path[::-1]  # Reverse path

    def solve(self):
        while len(self.open_set) > 0:
            # Get the cell in the open set with the lowest f_score
            current = min(self.open_set, key=lambda x: self.f_score[x])
            if current == self.goal:
                return self.reconstruct_path()

            self.open_set.remove(current)
            self.closed_set.append(current)

            for neighbour in current.get_neighbours(self.grid):
                if neighbour in self.closed_set:
                    continue

                tentative_g_score = self.g_score[current] + 1

                if neighbour not in self.open_set:
                    self.open_set.append(neighbour)
                elif tentative_g_score >= self.g_score[neighbour]:
                    continue

                self.came_from[neighbour] = current
                self.g_score[neighbour] = tentative_g_score
                self.f_score[neighbour] = self.g_score[neighbour] + \
                    self.heuristic(neighbour)

        return None


def check_neighbours(cell, grid):
    """
    This function checks the neighbours of a given cell in the grid. 
    Neighbours are defined as the cells that are directly horizontally or vertically adjacent.
    """
    neighbours = []
    # Check the neighboring cells
    if cell.row > 0:
        top = grid[cell.row - 1][cell.col]
        if not top.visited:
            neighbours.append(top)
    if cell.col < COLS - 1:
        right = grid[cell.row][cell.col + 1]
        if not right.visited:
            neighbours.append(right)
    if cell.row < ROWS - 1:
        bottom = grid[cell.row + 1][cell.col]
        if not bottom.visited:
            neighbours.append(bottom)
    if cell.col > 0:
        left = grid[cell.row][cell.col - 1]
        if not left.visited:
            neighbours.append(left)
    if len(neighbours) > 0:
        return random.choice(neighbours)
    else:
        return None


def remove_walls(cell, next):
    """
    This function removes the wall between two adjacent cells in the grid.
    """
    # Check the relative position of the two cells and remove the wall between them
    dx = cell.col - next.col
    if dx == 1:
        cell.walls["left"] = False
        next.walls["right"] = False
    elif dx == -1:
        cell.walls["right"] = False
        next.walls["left"] = False
    dy = cell.row - next.row
    if dy == 1:
        cell.walls["top"] = False
        next.walls["bottom"] = False
    elif dy == -1:
        cell.walls["bottom"] = False
        next.walls["top"] = False


def generate_maze():
    """
    This function generates a maze using a depth-first search algorithm.
    """
    # Create a grid of cells
    grid = [[Cell(i, j) for j in range(COLS)] for i in range(ROWS)]
    stack = []

    # Start with a random cell
    start = random.choice(random.choice(grid))
    start.visited = True
    stack.append(start)

    while len(stack) > 0:
        cell = stack[-1]
        next_cell = check_neighbours(cell, grid)
        if next_cell:
            next_cell.visited = True
            remove_walls(cell, next_cell)
            stack.append(next_cell)
        else:
            stack.pop()

    return grid


def draw_maze(grid):
    """
    This function draws the maze onto the Pygame window.
    """
    for row in grid:
        for cell in row:
            cell.draw()


def main():
    """
    The main function of the script. It handles the Pygame window, user input, and game logic.
    """
    pygame.init()
    clock = pygame.time.Clock()
    # Prepare the instruction text
    font = pygame.font.Font(None, 36)
    instruction_text = [
        "Press 1 for single player mode",
        "Press 2 for player vs AI mode",
    ]
    text_surfaces = [font.render(text, True, WHITE)
                     for text in instruction_text]

    # Display the instruction text
    for i, text_surface in enumerate(text_surfaces):
        SCREEN.blit(text_surface, (WIDTH // 2 - text_surface.get_width() //
                    2, HEIGHT // 2 + i * text_surface.get_height()))

    pygame.display.update()

    # Wait for the user to select a mode
    mode = None
    while mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "1"
                elif event.key == pygame.K_2:
                    mode = "2"

        # Clear the screen once the mode has been selected
    SCREEN.fill(BLACK)

    grid = generate_maze()

    # Create the ball at the center of the starting cell
    start_cell = grid[0][0]
    ball = Ball(start_cell.col * CELL_WIDTH + CELL_WIDTH // 2,
                start_cell.row * CELL_HEIGHT + CELL_HEIGHT // 2, grid, BLUE)

    # Define the goal as the bottom right cell
    goal_cell = grid[ROWS - 1][COLS - 1]

    # Ask the user for the game mode
    # mode = input("Enter game mode (1 - single player, 2 - player vs AI): ")
    if mode == "2":
        solver = MazeSolver(start_cell, goal_cell, grid)
        ai_path = solver.solve()
        ai_ball = Ball(start_cell.col * CELL_WIDTH + CELL_WIDTH // 2,
                       start_cell.row * CELL_HEIGHT + CELL_HEIGHT // 2, grid, RED)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Control the ball with the arrow keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and ball.can_move(0, -CELL_HEIGHT):
                    ball.y -= CELL_HEIGHT
                    ball.moves += 1
                elif event.key == pygame.K_DOWN and ball.can_move(0, CELL_HEIGHT):
                    ball.y += CELL_HEIGHT
                    ball.moves += 1
                elif event.key == pygame.K_LEFT and ball.can_move(-CELL_WIDTH, 0):
                    ball.x -= CELL_WIDTH
                    ball.moves += 1  # Increment moves
                elif event.key == pygame.K_RIGHT and ball.can_move(CELL_WIDTH, 0):
                    ball.x += CELL_WIDTH
                    ball.moves += 1
        # Check if the ball has reached the goal
        if (ball.x // CELL_WIDTH == goal_cell.col) and (ball.y // CELL_HEIGHT == goal_cell.row):
            print("You have reached the goal!")
            running = False

        draw_maze(grid)
        ball.draw()

        # Move the AI ball along the path
        if mode == "2" and len(ai_path) > 0:
            next_cell = ai_path.pop(0)
            ai_ball.x = next_cell.col * CELL_WIDTH + CELL_WIDTH // 2
            ai_ball.y = next_cell.row * CELL_HEIGHT + CELL_HEIGHT // 2
            ai_ball.draw()

        pygame.display.update()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
