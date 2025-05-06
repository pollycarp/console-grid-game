import os
import random

# Constants
GRID_SIZE = 20  # Size of the grid (20x20)
INITIAL_HEALTH = 100  # Player starting health
ENEMY_COUNT = 5  # Number of enemies to be placed

# Symbols used in the grid
EMPTY_CELL = "#"
PLAYER = "P"
GOAL = "G"
ENEMY = "E"


# Class representing the game logic and state
class Game:
    def __init__(self):
        # Initialize the 20x20 grid with EMPTY_CELL
        self.grid = [[EMPTY_CELL for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Randomly place the player and goal on the grid
        self.player_pos = self.random_empty_cell()
        self.goal_pos = self.random_empty_cell(exclude=[self.player_pos])
        self.enemies = self.generate_enemies()

        # Set initial player health
        self.health = INITIAL_HEALTH
        self.debug_mode = False  # Controls whether enemies/goal are visible

        # Place entities on the grid
        self.place_entity(self.player_pos, PLAYER)
        self.place_entity(self.goal_pos, GOAL)
        for enemy in self.enemies:
            self.place_entity(enemy, ENEMY)

    def random_empty_cell(self, exclude=[]):
        # Generate a random position not in the exclude list
        while True:
            pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if pos not in exclude:
                return pos

    def generate_enemies(self):
        # Create a list of unique enemy positions
        enemies = []
        while len(enemies) < ENEMY_COUNT:
            pos = self.random_empty_cell(exclude=[self.player_pos, self.goal_pos] + enemies)
            enemies.append(pos)
        return enemies

    def place_entity(self, position, symbol):
        # Place a symbol (P, G, or E) at the given position
        x, y = position
        self.grid[x][y] = symbol

    def clear_entity(self, position):
        # Clear the given position (set to EMPTY_CELL)
        x, y = position
        self.grid[x][y] = EMPTY_CELL

    def move_player(self, direction):
        # Move the player in the given direction (if within bounds)
        x, y = self.player_pos
        self.clear_entity(self.player_pos)  # Clear current position

        # Handle movement direction with bounds check
        if direction == "W" and x > 0:
            x -= 1
        elif direction == "S" and x < GRID_SIZE - 1:
            x += 1
        elif direction == "A" and y > 0:
            y -= 1
        elif direction == "D" and y < GRID_SIZE - 1:
            y += 1

        new_pos = (x, y)

        # Decrease health by 1 for moving
        self.health -= 1

        # Additional penalty if moving onto an enemy
        if new_pos in self.enemies:
            self.health -= 5

        # Update player's position and place on grid
        self.player_pos = new_pos
        self.place_entity(self.player_pos, PLAYER)

    def print_grid(self):
        # Clear the console and display the grid and health
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Health: {self.health}")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                # Determine what to show based on debug mode
                if (i, j) == self.player_pos:
                    print(PLAYER, end=" ")
                elif self.debug_mode:
                    print(self.grid[i][j], end=" ")
                else:
                    # Hide enemies and goal unless in debug mode
                    if (i, j) == self.goal_pos or (i, j) in self.enemies:
                        print(EMPTY_CELL, end=" ")
                    else:
                        print(self.grid[i][j], end=" ")
            print()  # New line after each row

    def is_game_over(self):
        # End game if health is 0 or goal reached
        return self.player_pos == self.goal_pos or self.health <= 0

    def toggle_debug(self):
        # Toggle debug mode (reveals goal/enemies)
        self.debug_mode = not self.debug_mode


# Main game loop
def main():
    game = Game()
    while not game.is_game_over():
        game.print_grid()
        # Prompt user for movement or debug toggle
        move = input("Move (W/A/S/D), or type 'debug' to toggle debug mode: ").upper()
        if move in ["W", "A", "S", "D"]:
            game.move_player(move)
        elif move == "DEBUG":
            game.toggle_debug()
        else:
            print("Invalid input. Use W/A/S/D to move.")
    game.print_grid()
    # Display game result
    if game.player_pos == game.goal_pos:
        print("🎉 Congratulations! You reached the goal!")
    else:
        print("💀 Game over! You ran out of health.")


# Entry point of the program
if __name__ == "__main__":
    main()
