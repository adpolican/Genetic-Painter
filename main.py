import random
import configparser
import time
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
#DISPLAY_ON = CONFIG[SECTION]['DISPLAY_ON']

# if DISPLAY_ON:
#    import matplotlib.pyplot as plt
#    import matplotlib.image as mpimg


def new_population(fittest, info):
    # Make new chromosomes by crossing over the fittest
    children = fittest[:ELITE_COUNT]
    for ii in range(POPULATION_SIZE-ELITE_COUNT):
        parent_a = random.choice(fittest)
        parent_b = random.choice(fittest)
        child = parent_a.crossover(parent_b, info)
        children.append(child)
    return children


def main():
    # Info is bound to a namespace so we can pass it to chromosomes
    info = SimpleNamespace(
        population=[],
        gens_done=0,
        gens_left=GENERATIONS,
        mutator=mutators.get_mutator(MUTATOR_NAME),
        target_image=cv.imread(FILE_NAME, 1),
        config_info=CONFIG,
    )
    if info.target_image is None:
        raise Exception('Image not found')

    for ii in range(POPULATION_SIZE):
        chrom = info.mutator.Chromosome(info)
        info.population.append(chrom)

    info.population.sort(key=lambda chrom: chrom.evaluate())
    fittest = info.population[:PARENT_COUNT]

    while info.gens_done < GENERATIONS:
        info.gens_left -= 1
        info.gens_done += 1

        # Find most fit
        info.population.sort(key=lambda chrom: chrom.evaluate())
        fittest = info.population[:PARENT_COUNT]

        # Crossover fittest to produce new population
        info.population = new_population(fittest, info)

        for chrom in info.population[ELITE_COUNT:]:
            chrom.mutate()

        msg = 'Generation: {} \tFittest: {}'
        print(msg.format(info.gens_done, repr(fittest[0].evaluate())))

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
