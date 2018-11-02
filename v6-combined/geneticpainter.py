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
FILE_NAME = '../sources/Afgan_girl.jpg'
BRUSH_RANGE = range(2,150)
brushes = [Image.open('../brushes/1.png')]

def pix_compare(subject, target):
    diff_img = ImageChops.difference(subject, target)
    score = sum(ImageStat.Stat(diff_img).sum)
    return score

class painter(object):
    def __init__(self, image, mutator, errorFunction=pix_compare,
                 finalWidth=3000):
        self.image = image
        self.mutator = mutator
        # self.mutator must take an image of arbitrary size
        # and return an image of the same size
        self.fitnessFunction = fitnessFunction
        self.finalWidth = finalWidth
        self.generation_info = []
        original_image = Image.open(FILE_NAME)
        self.target_image = original_image.convert(mode='RGB')
        self.findError = errorFunction(self.image)

    def generate_individual(size):
        new_indv = Image.new('RGB', size, '#e0e0e0')
        return new_indv
 
    def render_final(self):
        continue

    def step(self):
        # performs 1 step, doesn't guarantee progress
        new_image = self.mutator(self.image)
        new_image_fitness = self.fitness
        if new_image_fitness < 



if __name__ == '__main__':
    start_time = time.time()
    population = []
    new_population = []
    brush_info = []

    generations = 0
    gens_left = 0
    started = False

    img_colors = ImageOps.posterize(target_image,4).getcolors(100000000)
    img_colors.sort()
    img_colors.reverse()
    colors = [i[1] for i in img_colors][:COLOR_COUNT]
    image_size = target_image.size
    for i in range(POPULATION_SIZE):
        population.append(generate_individual(image_size))
    population.sort(key=lambda x: find_fitness(x[0],target_image))
    fittest = population[0]
    brush_info.append(fittest[1:])
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
            brush_info.append(fittest[1:])
             
            # Mutate fittest to produce new population
            while len(new_population) < POPULATION_SIZE:
                new_population.append(mutate_parent(fittest[0]))
            population = new_population

            print('Generation: ' + str(generations) + '\t Fittest: ' + str(find_fitness(fittest[0], target_image)))
    except KeyboardInterrupt as e:
        pass
    save_name = raw_input('File name? ')
    print('Final score: ' + str(find_fitness(fittest[0], target_image)))
    scale = 2000.0/fittest[0].size[0]
    size_x = int(scale*fittest[0].size[0])
    size_y = int(scale*fittest[0].size[1])
    result = Image.new('RGB', (size_x,size_y),'#e0e0e0')
    draw = ImageDraw.Draw(result)
    for idx, i in enumerate(brush_info):
        xys = [j*scale for j in i[0]]
        brush = brushes[0].copy()
        brush = brush.resize((int(scale*i[2]*brush.size[0]), int(scale*i[2]*brush.size[1])))
        brush = brush.rotate(i[4], expand=True)
        draw.bitmap(xys, brush, fill=i[1])
        print('rendering stroke :' + str(idx))
    result.save('../results/' + save_name + '.png')
    print('Result saved as ' + save_name+ '.png')
    print('Ended in ' + str(time.time() - start_time))

