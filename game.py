import random
import pygame
import numpy as np


from enum import Enum


PLAYER1_CHAR = "Y"
PLAYER2_CHAR = "R"

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
                if cell == PLAYER1_CHAR:
                    result[i * 7 + j] = 1
                elif cell == PLAYER2_CHAR:
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
                    if self.board[row][column] == PLAYER1_CHAR
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
                    if self.board[row][column] == PLAYER1_CHAR
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
                        if self.board[row][column] == PLAYER1_CHAR
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
            self.board[row][column] = PLAYER1_CHAR
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
            self.board[row][column] = PLAYER2_CHAR
            self.column_chips[column] += 1
            return self.check_win(row, column)
        else:
            raise Exception("Player 1's turn!")

    def draw_board(self, screen=None):
        if screen is None:
            screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))
        for i in range(6):
            for j in range(7):
                if self.board[i][j] == "R":
                    pygame.draw.circle(screen, (255, 0, 0), (j * 100 + 50, i * 100 + 50), 40)
                elif self.board[i][j] == "Y":
                    pygame.draw.circle(screen, (255, 255, 0), (j * 100 + 50, i * 100 + 50), 40)
                else:
                    pygame.draw.circle(screen, (255, 255, 255), (j * 100 + 50, i * 100 + 50), 40)
        pygame.display.flip()
        
if __name__ == "__main__":
    game = Game()
    pygame.init()
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption("Connect 4")
    game.draw_board(screen)
    player1_move = True
    move = None
    while move not in {MoveResult.PLAYER1_WON, MoveResult.PLAYER2_WON, MoveResult.DRAW}:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if player1_move:
                    move = game.player1_move(event.pos[0] // 100)
                else:
                    move = game.player2_move(event.pos[0] // 100)
                game.draw_board(screen)
                if move == MoveResult.PLAYER1_WON:
                    print("Player 1 won!")
                elif move == MoveResult.PLAYER2_WON:
                    print("Player 2 won!")
                elif move == MoveResult.INVALID_MOVE:
                    print("Invalid move!")
                elif move == MoveResult.DRAW:
                    print("Draw!")
                player1_move = not player1_move
