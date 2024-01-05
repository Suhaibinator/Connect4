import random
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np


from enum import Enum


class MoveResult(Enum):
    MOVE_MADE = 1
    PLAYER1_WON = 2
    PLAYER2_WON = 3
    INVALID_MOVE = 4
    DRAW = 5


class Game:
    board: list
    player1_moves = 0
    player2_moves = 0
    column_chips = []

    def __init__(self):
        self.board = [[""] * 7 for _ in range(6)]
        self.column_chips = [0] * 7

    def vectorize_board(self) -> np.ndarray:
        result = np.zeros((42,), dtype=np.float32)
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == "R":
                    result[i * 7 + j] = 1
                elif cell == "Y":
                    result[i * 7 + j] = 2
        return result

    def get_row(self, column: int) -> int:
        if self.column_chips[column] == 6:
            return -1
        return 5 - self.column_chips[column]

    def check_win(self, row: int, column: int) -> MoveResult:
        # Check horizontal
        count = 0
        for i in range(7):
            if self.board[row][i] == self.board[row][column]:
                count += 1
            else:
                count = 0
            if count == 4:
                return (
                    MoveResult.PLAYER1_WON
                    if self.board[row][column] == "R"
                    else MoveResult.PLAYER2_WON
                )

        # Check vertical
        count = 0
        for i in range(6):
            if self.board[i][column] == self.board[row][column]:
                count += 1
            else:
                count = 0
            if count == 4:
                return (
                    MoveResult.PLAYER1_WON
                    if self.board[row][column] == "R"
                    else MoveResult.PLAYER2_WON
                )

        # Check diagonals
        for direction in [-1, 1]:
            count = 0
            for dr in range(-3, 4):
                r, c = row + dr, column + dr * direction
                if (
                    0 <= r < 6
                    and 0 <= c < 7
                    and self.board[r][c] == self.board[row][column]
                ):
                    count += 1
                else:
                    count = 0
                if count == 4:
                    return (
                        MoveResult.PLAYER1_WON
                        if self.board[row][column] == "R"
                        else MoveResult.PLAYER2_WON
                    )

        return MoveResult.MOVE_MADE

    def player1_move(self, column: int) -> MoveResult:
        if self.player1_moves + self.player2_moves == 42:
            return MoveResult.DRAW
        if self.player1_moves == self.player2_moves:
            self.player1_moves += 1
            if column < 0 or column > 6:
                raise Exception("Invalid column!")
            row = self.get_row(column)
            if row == -1:
                return MoveResult.INVALID_MOVE
            self.board[row][column] = "Y"
            self.column_chips[column] += 1
            return self.check_win(row, column)
        else:
            raise Exception("Player 2's turn!")

    def player2_move(self, column: int) -> MoveResult:
        if self.player1_moves + self.player2_moves == 42:
            return MoveResult.DRAW
        if self.player1_moves > self.player2_moves:
            self.player2_moves += 1
            if column < 0 or column > 6:
                raise Exception("Invalid column!")
            row = self.get_row(column)
            if row == -1:
                return MoveResult.INVALID_MOVE
            self.board[row][column] = "R"
            self.column_chips[column] += 1
            return self.check_win(row, column)
        else:
            raise Exception("Player 1's turn!")

    def draw_board(self):
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(7, 6))

        # Define the colors: empty as white, R as red, and Y as yellow
        color_dict = {"": "white", "R": "red", "Y": "yellow"}

        # Convert the board to a numerical grid where 0: empty, 1: R, 2: Y for color mapping
        num_grid = np.zeros((len(self.board), len(self.board[0])), dtype=int)
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                num_grid[i, j] = 0 if cell == "" else (1 if cell == "R" else 2)

        # Create the Connect 4 grid structure
        ax.matshow(np.ones_like(num_grid), cmap="Blues", vmin=0, vmax=1)

        # Plot the pieces on the board
        for (i, j), val in np.ndenumerate(num_grid):
            if val:  # Only draw if the cell is not empty
                ax.add_patch(
                    plt.Circle((j, i), 0.45, color=color_dict[self.board[i][j]])
                )

        # Set the ticks and labels
        ax.set_xticks(np.arange(len(self.board[0])))
        ax.set_yticks(np.arange(len(self.board)))
        ax.set_xticklabels(range(1, len(self.board[0]) + 1))
        ax.set_yticklabels(range(1, len(self.board) + 1))
        ax.set_xticks(np.arange(-0.5, len(self.board[0]), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(self.board), 1), minor=True)
        ax.grid(which="minor", color="black", linestyle="-", linewidth=2)

        # Hide the major tick labels
        ax.tick_params(which="major", size=0)

        # Set aspect ratio to be equal
        ax.set_aspect("equal")

        # Show the plot
        plt.show()

