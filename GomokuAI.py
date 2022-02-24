from enum import IntEnum
import os
import pygame
import neat
    
class SlotType(IntEnum):
    NONE = 0
    BLACK = 1
    WhITE = 2

class GomokuGame:
    
    def __init__(self, size = 19):
        self.board = [[SlotType.NONE for i in range(size)] for j in range(size)]

    def Draw(self):
        pass

    def TrainAI(self, a, b):
        # Main loop
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()


def EvaluateFitness(NNs, config):
    # Initialize pygame
    pygame.init()
    pygame.display.set_mode((700, 500))
    pygame.display.set_caption('Gomoku')

    game = GomokuGame()

    for i, (idA, nnA) in enumerate(NNs[:-1]):
        for (idB, nnB) in NNs[i + 1:]:
            game.TrainAI(nnA, nnB)
            


def TrainAI(config):
    # Initailze neat
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    bestAI = p.run(EvaluateFitness, 16)



def PlayAgainstAI(config):
    pass

    
if __name__ == '__main__':

    currrentDirectory = os.path.dirname(__file__)
    configPath = os.path.join(currrentDirectory, 'NeatConfig.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

    TrainAI(config)
    PlayAgainstAI(config)