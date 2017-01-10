import random
from PIL import Image, ImageChops, ImageStat, ImageDraw, ImageOps
from copy import copy
from random import randint
import time

POPULATION_SIZE = 40
SKIP_COUNT = 3
MAX_LETTER_SIZE = 200
MIN_LETTER_SIZE = 1
COLOR_COUNT = 100
FILE_NAME = '../sources/dan.png'
TRIANGLE_RANGE = range(-100,100)

def generate_individual(size):
    new_indv = mutate_parent(Image.new('RGBA', size, '#e0e0e0'))
    return new_indv

def mutate_parent(image_data):
    child = image_data.copy()
    xy1 = random.choice(range(0,child.size[0])), random.choice(range(0,child.size[1]))
    x_d, y_d = random.choice(TRIANGLE_RANGE), random.choice(TRIANGLE_RANGE)
    xy2 = xy1[0]+x_d, xy1[1]+y_d
    x_d, y_d = random.choice(range(-50,50)), random.choice(TRIANGLE_RANGE)
    xy3 = xy1[0]+x_d, xy1[1]+y_d
    xys = xy1+xy2+xy3
    color = random.choice(colors) + (100,)
    draw = ImageDraw.Draw(child)
    draw.polygon(xys, fill=color)
    return (child, xys, color)

def find_fitness(subject, target):
    diff_img = ImageChops.difference(subject, target)
    score = sum(ImageStat.Stat(diff_img).sum)
    return score

if __name__ == '__main__':
    start_time = time.time()
    population = []
    new_population = []
    shape_info = []

    generations = 0
    gens_left = 0
    started = False

    original_image = Image.open(FILE_NAME)
    target_image = original_image.convert(mode='RGBA')
    #img_colors = ImageOps.posterize(target_image,4).getcolors(100000000)
    img_colors = target_image.getcolors(100000000)
    img_colors.sort()
    img_colors.reverse()
    colors = [i[1] for i in img_colors][:COLOR_COUNT]
    image_size = target_image.size
    for i in range(POPULATION_SIZE):
        population.append(generate_individual(image_size))
    population.sort(key=lambda x: find_fitness(x[0],target_image))
    fittest = population[0]
    shape_info.append(fittest[1:])
    try:
        while True:
            if gens_left == 0:
                try:
                    gens_left = int(raw_input('How many generations? (0 to exit) '))
                    if gens_left == 0:
                        break
                except Exception as e:
                    print('INVLID INPUT')
                    print('EXITING')
                    break
            gens_left -= 1
            generations += 1
            
            # Find most fit
            fittest = min(population, key=lambda x: find_fitness(x[0],target_image))
            new_population = [fittest]
            shape_info.append(fittest[1:])
             
            # Mutate fittest to produce new population
            while len(new_population) < POPULATION_SIZE:
                new_population.append(mutate_parent(fittest[0]))
            population = new_population

            print('Generation: ' + str(generations) + '\t Fittest: ' + str(find_fitness(fittest[0], target_image)))
    except KeyboardInterrupt as e:
        pass
    save_name = raw_input('File name? ')
    print('Final score: ' + str(find_fitness(fittest[0], target_image)))
    scale = 3000.0/fittest[0].size[0]
    size_x = int(scale*fittest[0].size[0])
    size_y = int(scale*fittest[0].size[1])
    result = Image.new('RGBA', (size_x,size_y),'#e0e0e0')
    draw = ImageDraw.Draw(result)
    for i in shape_info:
        xys = [j*scale for j in i[0]]
        draw.polygon(xys, fill=i[1])
    result.save('../results/' + save_name + '.png')
    print('Result saved as ' + save_name+ '.png')
    print('Ended in ' + str(time.time() - start_time))

