from enum import Enum
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class PieceState(float, Enum):
    NONE = 0
    BLACK = 1
    WHITE = 2

class GomokuGame:

    boardImg = None
    
    def __init__(self):
        self.board = [[PieceState.NONE for i in range(19)] for j in range(19)]
        self.moves = 0
        self.winner = PieceState.NONE

    def Reset(self):
        self.board = [[PieceState.NONE for i in range(19)] for j in range(19)]
        self.moves = 0
        self.winner = PieceState.NONE

    @staticmethod
    def Draw(game, screen : pygame.Surface, pos : tuple):
        if GomokuGame.boardImg == None: 
            GomokuGame.boardImg = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Image\\board.png'))
            #pygame.transform.scale(GomokuGame.boardImg, (300, 300))

        screen.blit(game.boardImg, dest = pos)
        centerPos = (pos[0] + GomokuGame.boardImg.get_width() * 0.5, pos[1] + GomokuGame.boardImg.get_height() * 0.5)
        gridSize = 32.8

        for i, row in enumerate(game.board):
            for j, piece in enumerate(row):
                if piece == PieceState.WHITE:
                    pygame.draw.circle(screen, color=(255,255,255), radius=15,
                                       center=(centerPos[0] + (i - 9) * gridSize, centerPos[1] + (j - 9) * gridSize))
                elif piece == PieceState.BLACK:
                    pygame.draw.circle(screen, color=(0,0,0), radius=15,
                                       center=(centerPos[0] + (i - 9) * gridSize, centerPos[1] + (j - 9) * gridSize))

    def SetPosition(self, pos : tuple):
        self.centerPos = pos

    def PlacePiece(self, state : PieceState, pos : tuple):
        self.board[pos[0]][pos[1]] = state;
        self.moves += 1
        
        # Check for wins
        up = down = left = right = upLeft = upRight = downLeft = downRight = 0
        while up < 5 and pos[1] + up < 18 and self.board[pos[0]][pos[1] + up + 1] == state:
            up += 1
        while down < 5 and pos[1] - down > 0 and self.board[pos[0]][pos[1] - down - 1] == state:
            down += 1
        while left < 5 and pos[0] - left > 0 and self.board[pos[0] - left - 1][pos[1]] == state:
            left += 1
        while right < 5 and pos[0] + right < 18 and self.board[pos[0] + right + 1][pos[1]] == state:
            right += 1
        while upLeft < 5 and pos[0] - upLeft > 0 and pos[1] - upLeft > 0 and self.board[pos[0] - upLeft - 1][pos[1] - upLeft - 1] == state:
            upLeft += 1
        while upRight < 5 and pos[0] + upRight < 18 and pos[1] - upRight > 0 and self.board[pos[0] + upRight + 1][pos[1] - upRight - 1] == state:
            upRight += 1
        while downLeft < 5 and pos[0] - downLeft > 0 and pos[1] + downLeft < 18 and self.board[pos[0] - downLeft - 1][pos[1] + downLeft + 1] == state:
            downLeft += 1
        while downRight < 5 and pos[0] + downRight < 18 and pos[1] + downRight < 18 and self.board[pos[0] + downRight + 1][pos[1] + downRight + 1] == state:
            downRight += 1

        if up + down >= 4 or left + right >= 4 or upLeft + upRight >= 4 or downLeft + downRight >= 4:
            self.winner = state
            return True
        return False