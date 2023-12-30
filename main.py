import matplotlib.pyplot as plt
import numpy as np

def draw_connect4_board(board):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(7, 6))

    # Define the colors: empty as white, R as red, and Y as yellow
    color_dict = {"": "white", "R": "red", "Y": "yellow"}

    # Convert the board to a numerical grid where 0: empty, 1: R, 2: Y for color mapping
    num_grid = np.zeros((len(board), len(board[0])), dtype=int)
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            num_grid[i, j] = 0 if cell == "" else (1 if cell == "R" else 2)

    # Create the Connect 4 grid structure
    ax.matshow(np.ones_like(num_grid), cmap='Blues', vmin=0, vmax=1)

    # Plot the pieces on the board
    for (i, j), val in np.ndenumerate(num_grid):
        if val:  # Only draw if the cell is not empty
            ax.add_patch(plt.Circle((j, i), 0.45, color=color_dict[board[i][j]]))

    # Set the ticks and labels
    ax.set_xticks(np.arange(len(board[0])))
    ax.set_yticks(np.arange(len(board)))
    ax.set_xticklabels(range(1, len(board[0]) + 1))
    ax.set_yticklabels(range(1, len(board) + 1))
    ax.set_xticks(np.arange(-.5, len(board[0]), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(board), 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

    # Hide the major tick labels
    ax.tick_params(which='major', size=0)

    # Set aspect ratio to be equal
    ax.set_aspect('equal')

    # Show the plot
    plt.show()

# Test the function with a sample board
sample_board = [
    ["R", "Y", "R", "R", "Y", "R", "Y"],
    ["R", "R", "Y", "Y", "R", "", ""],
    ["Y", "Y", "R", "R", "", "", ""],
    ["Y", "R", "Y", "", "", "", ""],
    ["R", "Y", "R", "", "", "", ""],
    ["Y", "R", "", "", "", "", ""]
]

draw_connect4_board(sample_board)
