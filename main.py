import copy
from deap import base, creator, tools
from scoop import futures
import numpy as np
from torch.nn import Module
from torch import from_numpy
from game import Game

from neural_net import YourNetwork

net_sample: Module = YourNetwork().float()


def genotype_to_phenotype(vector: list[float]) -> Module:
    # net_sample is needed to build the net from the vector
    # Individuals in the populations are represented as lists.
    # In order to evaluate their performance, they need to be converted to
    # neural network (phenotype)
    net_copy: Module = copy.deepcopy(net_sample)
    vector_copy: np.ndarray = copy.deepcopy(np.array(vector, dtype=np.float32))

    for p in net_copy.parameters():
        len_slice: int = p.numel()
        replace_with: np.ndarray = vector_copy[0:len_slice].reshape(p.data.size())
        p.data = from_numpy(replace_with)
        vector_copy = np.delete(vector_copy, np.arange(len_slice))

    return net_copy


from deap import base, creator, tools
import random
from game import MoveResult, Game


def play_game(individual1, individual2) -> tuple[MoveResult, int]:
    # Convert the individuals to neural networks
    net1 = genotype_to_phenotype(individual1)
    net2 = genotype_to_phenotype(individual2)

    # Play a game of Connect4 between the two individuals
    game = Game()
    last_move = None
    player1_move = True
    while last_move not in {
        MoveResult.PLAYER1_WON,
        MoveResult.PLAYER2_WON,
        MoveResult.DRAW,
        MoveResult.INVALID_MOVE,
    }:
        if player1_move:
            move = net1.forward(game.vectorize_board())
            last_move = game.player1_move(move)
        else:
            move = net2.forward(game.vectorize_board())
            last_move = game.player2_move(move)
        player1_move = not player1_move
    return last_move, game.player1_moves + game.player2_moves


# Define the fitness function
def evaluate(individual: list[float]):
    # Convert the individual to a neural network

    # Play a game of Connect4 against 20 other individuals and compute the fitness score
    score = 0
    for _ in range(50):
        opponent = random.choice(population)
        game_result, num_moves = play_game(individual, opponent)
        score += num_moves * 2
        if game_result == MoveResult.PLAYER1_WON:
            score += 100
        elif game_result == MoveResult.PLAYER2_WON:
            score -= 10
        elif game_result == MoveResult.INVALID_MOVE:
            score -= 70
    return (score,)


# Define the individual and population
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()


def float32_generator():
    return np.float32(random.uniform(-1, 1))


toolbox.register("attr_float", float32_generator)
toolbox.register(
    "individual",
    tools.initRepeat,
    creator.Individual,
    toolbox.attr_float,
    n=net_sample.num_params(),
)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Register the map function
toolbox.register("map", futures.map)

# Generate the initial population
population = toolbox.population(n=100)

# Register the evaluation function
toolbox.register("evaluate", evaluate)

# Register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# Register a mutation operator
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.1)

# Register the selection operator
toolbox.register("select", tools.selTournament, tournsize=3)

# Run the algorithm
NGEN = 1000
for gen in range(NGEN):
    print(f"Generation {gen}")
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.5:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < 0.2:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit,

    population[:] = offspring

# pickle the population
import pickle

with open("population.pkl", "wb") as f:
    pickle.dump(population, f)
