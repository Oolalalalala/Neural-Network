from gomoku import PieceState, GomokuGame
from window import Window
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import neat
import random
import concurrent.futures
import time
import pickle
    

def ApplyFitness(game, whiteGenome, blackGenome):
    if game.winner == PieceState.WHITE:
        whiteGenome.fitness += 1 + 8 / game.moves
    elif game.winner == PieceState.BLACK:
        blackGenome.fitness += 1 + 8 / game.moves
    else:
        whiteGenome.fitness += 0.5
        blackGenome.fitness += 0.5
        

def AIPlayGomoku(nnA, nnB, idxA, idxB):

    game = GomokuGame()
    turn = random.choice([PieceState.WHITE, PieceState.BLACK])
    occupied = set()
    input = [0 for _ in range(361)]

    while 1:
        for i, row in enumerate(game.board):
            for j, piece in enumerate(row):
                if piece == turn:
                    input[i * 19 + j] = 1
                elif piece == PieceState.NONE:
                    input[i * 19 + j] = 0.5
                else:
                    input[i * 19 + j] = 0

        maxValue, maxIdx = float('-inf'), -1


        if turn == PieceState.WHITE:
            output = nnA.activate(input)
            for i, value in enumerate(output):
                if i not in occupied:
                    if value > maxValue:
                        maxValue = value
                        maxIdx = i
            if maxIdx != -1:
                if game.PlacePiece(PieceState.WHITE, (maxIdx // 19, maxIdx % 19)):
                    return (game, idxA, idxB)

                occupied.add(maxIdx)

            turn = PieceState.BLACK
        else:
            output = nnB.activate(input)
            for i, value in enumerate(output):
                if i not in occupied:
                    if value > maxValue:
                        maxValue = value
                        maxIdx = i
            if maxIdx != -1:
                if game.PlacePiece(PieceState.BLACK, (maxIdx // 19, maxIdx % 19)):
                    return (game, idxA, idxB)

                occupied.add(maxIdx)

            turn = PieceState.WHITE
        
        if len(occupied) == 361:
            game.winner = PieceState.NONE
            return (game, idxA, idxB)


def EvaluateFitness(genomes, config):

    # Save the best for every 20 generation
    if pop.generation % 20 == 1:
        with open(f'best#{pop.generation - 1}.pickle', "wb") as f:
            pickle.dump(stats.best_genome(), f)


    for (id, genome) in genomes:
        genome.fitness = 0

    NNs = [neat.nn.FeedForwardNetwork.create(genome, config) for (id, genome) in genomes]

    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executer:
        for i, nnA in enumerate(NNs[:-1]):
            for j, nnB in enumerate(NNs[i + 1:]):
                results.append(executer.submit(AIPlayGomoku, nnA, nnB, i, j))
        for f in concurrent.futures.as_completed(results):
            (game, idxA, idxB) = f.result()
            ApplyFitness(game, genomes[idxA][1], genomes[idxB][1])
    
        


def TrainAI(config):
    global pop, stats
    # Initailze neat
    pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-15')
    #pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(5, 10000))
    
    
    bestAI = pop.run(EvaluateFitness, 32)
    


def AIPlayAgainstAI(genomeA, genomeB, config):

    Window.Init()

    nnA = neat.nn.FeedForwardNetwork.create(genomeA, config)
    nnB = neat.nn.FeedForwardNetwork.create(genomeB, config)

    game = GomokuGame()
    turn = PieceState.WHITE
    accumulatedTime, timePerMove, prevTime = 0, 0.7, time.time()
    occupied = set()
    input = [0 for _ in range(361)]

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        Window.BeginRender()
        GomokuGame.Draw(game, Window.screen, (0,0))
        Window.EndRender()
        
        accumulatedTime += time.time() - prevTime
        prevTime = time.time()
        if accumulatedTime < timePerMove:
            continue

        accumulatedTime -= timePerMove

        for i, row in enumerate(game.board):
            for j, piece in enumerate(row):
                if piece == turn:
                    input[i * 19 + j] = 1
                elif piece == PieceState.NONE:
                    input[i * 19 + j] = 0.5
                else:
                    input[i * 19 + j] = 0

        maxValue, maxIdx = float('-inf'), -1

        if turn == PieceState.WHITE:
            output = nnA.activate(input)
            for i, value in enumerate(output):
                if i not in occupied:
                    if value > maxValue:
                        maxValue = value
                        maxIdx = i
            if maxIdx != -1:
                if game.PlacePiece(PieceState.WHITE, (maxIdx // 19, maxIdx % 19)):
                    return PieceState.WHITE

                occupied.add(maxIdx)

            turn = PieceState.BLACK
        else:
            output = nnB.activate(input)
            for i, value in enumerate(output):
                if i not in occupied:
                    if value > maxValue:
                        maxValue = value
                        maxIdx = i
            if maxIdx != -1:
                if game.PlacePiece(PieceState.BLACK, (maxIdx // 19, maxIdx % 19)):
                    return PieceState.BLACK

                occupied.add(maxIdx)

            turn = PieceState.WHITE


        if len(occupied) == 361:
            return PieceState.NONE
        


def PlayerPlayAgainstAI(genome, config):
    Window.Init()

    nn = neat.nn.FeedForwardNetwork.create(genome, config)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    
if __name__ == '__main__':

    currrentDirectory = os.path.dirname(__file__)
    configPath = os.path.join(currrentDirectory, 'neatConfig.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)
    
    TrainAI(config)

    #with open("best.pickle", "rb") as f:
    #    genome = pickle.load(f)
    #    AIPlayAgainstAI(genome, genome, config)

    