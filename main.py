import random
import configparser
import time
import multiprocessing as mltpc
from types import SimpleNamespace

import cv2 as cv

import mutators

CONFIG = configparser.ConfigParser()
CONFIG.read('./config/main.ini')

SECTION = 'SETTINGS'
MUTATOR_NAME = CONFIG[SECTION]['MUTATOR_NAME']
PARENT_COUNT = int(CONFIG[SECTION]['PARENT_COUNT'])
ELITE_COUNT = int(CONFIG[SECTION]['ELITE_COUNT'])
POPULATION_SIZE = int(CONFIG[SECTION]['POPULATION_SIZE'])
GENERATIONS = int(CONFIG[SECTION]['GENERATIONS'])
FILE_NAME = CONFIG[SECTION]['FILE_NAME']
PARALLEL = ('true' == CONFIG[SECTION]['PARALLEL'].lower())
#DISPLAY_ON = CONFIG[SECTION]['DISPLAY_ON']

# if DISPLAY_ON:
#    import matplotlib.pyplot as plt
#    import matplotlib.image as mpimg


def new_population(fittest, context):
    # Make new chromosomes by crossing over the fittest
    children = fittest[:ELITE_COUNT]
    for ii in range(POPULATION_SIZE-ELITE_COUNT):
        parent_a = random.choice(fittest)
        parent_b = random.choice(fittest)
        child = parent_a.crossover(parent_b, context)
        children.append(child)
    return children

def mutate(child): 
    return child.mutate()

class Context:
    def __init__(self, gens_left, target_image, config_info):
        self.population = []
        self.gens_done = 0
        self.gens_left = gens_left
        self.target_image = target_image
        self.config_info = config_info

def main():
    # Context info is bound to a namespace so we can pass it to chromosomes
    context = Context(
        gens_left=GENERATIONS,
        target_image=cv.imread(FILE_NAME, 1),
        config_info=CONFIG,
    )
    if context.target_image is None:
        raise Exception('Image not found')

    for ii in range(POPULATION_SIZE):
        chrom = mutators.get_mutator(MUTATOR_NAME).Chromosome
        context.population.append(chrom(context))
    context.population.sort(key=lambda chrom: chrom.evaluate())
    fittest = context.population[:PARENT_COUNT]
 
    while context.gens_done < GENERATIONS:
        context.gens_left -= 1
        context.gens_done += 1

        # Find most fit
        context.population.sort(key=lambda chrom: chrom.evaluate())
        fittest = context.population[:PARENT_COUNT]

        # Crossover fittest to produce new population
        context.population = new_population(fittest, context)

        # Mutate population
        cpu_count = mltpc.cpu_count()
        if PARALLEL: 
            # Parallel execution is still experimental
            # At the moment it is actually 
            # slower than serial execution
            with mltpc.Pool(cpu_count-2) as pool:
                context.population = pool.map(mutate, context.population)
        else:
            for chrom in context.population[ELITE_COUNT:]:
                chrom.mutate()

        msg = 'Generation: {} \tFittest: {}'
        print(msg.format(context.gens_done, repr(fittest[0].evaluate())))

    name_info = (MUTATOR_NAME, POPULATION_SIZE, GENERATIONS, time.time())
    save_name = '{}_{}POP_{}GENS_{}'.format(*name_info)
    print('Final score: ' + repr(fittest[0].evaluate()))

    best = fittest[0]
    save_path = './results/{}.png'.format(save_name)
    cv.imwrite(save_path, best.render())
    msg = 'Result saved as {}'
    print(msg.format(save_path))


if __name__ == '__main__':
    main()
