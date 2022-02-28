import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Window:

    screen : pygame.Surface
    
    @staticmethod
    def Init():
        pygame.init()
        pygame.display.set_caption('Gomoku')
        Window.screen = pygame.display.set_mode((750, 750))

    @staticmethod
    def BeginRender():
        Window.screen.fill((0,0,0))

    @staticmethod
    def EndRender():
        pygame.display.update()