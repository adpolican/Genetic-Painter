import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageChops, ImageStat, ImageFont, ImageDraw, ImageOps
#from copy import deepcopy
from random import randint, choice
from scipy.spatial import Delaunay
from copy import deepcopy
import pickle

POPULATION_SIZE = 20
COLOR_COUNT = 100
POINT_COUNT = 1000
FILE_NAME = '../sources/biggie.jpg'
DISPLAY_ON = False
PROMPT = False
NO_PROMPT_GENS = 10 # Default gen count if no prompt
NO_PROMPT_NAME = 'biggie_' + str(NO_PROMPT_GENS)
original_image = Image.open(FILE_NAME)
target_image = original_image.convert(mode='RGB')
img_colors = ImageOps.posterize(target_image,4).getcolors(100000000)
img_colors.sort()
img_colors.reverse()
COLORS = [i[1] for i in img_colors][:COLOR_COUNT]
FINAL_SIZE = target_image.size
SAMPLE_SIZE = (target_image.size[0]//3, target_image.size[1]//3)

if DISPLAY_ON:
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

'''
Individuals are represented as a 3 tuple 
a list of points, and a list of colors
The list of points is shaped (POINT_COUNT, 2)
The list of colors is shaped (POINT_COUNT*2, 3)
Colors are also tuples

Optimizations:
    1: Downsizing the samples during the mutation/evaluation phase
    2: Using pickle to copy instead of deepcopy
    3: Instead of creating a new ImageDraw.Draw instance every time
       we call render, just reuse and old one
'''
pklcopy = lambda x: pickle.loads(pickle.dumps(x,-1))

def generate_individual(size):
    #points = np.random.normal(loc=0.5, scale=0.2, size=(POINT_COUNT,2))
    points = np.random.rand(POINT_COUNT, 2)
    points = np.multiply(points, np.array(size))
    colors = [choice(COLORS) for i in range(len(points)*2)]
    new_indv = (points, colors)
    return new_indv

def mutate_parent(indiv, rate):
    '''
    rate is a float from 0 to 1
    '''
    indiv = pklcopy(indiv)
    mutate_color = random.random() < 0.5
    points, colors = indiv
    if mutate_color:
        #for i in range(int(rate*POINT_COUNT*2)):
        idx = randint(0, len(points)*2 - 1)
        colors[idx] = choice(COLORS)
    else: 
        #for i in range(int(rate*POINT_COUNT)):
        point_shift = np.random.randint(-rate*min(SAMPLE_SIZE)/5, 
                                        rate*min(SAMPLE_SIZE)/5, 
                                        size=(2,)) 
        idx = randint(0, len(points)-1)
        points[idx] += point_shift
        points[idx] = np.clip(points[idx], 
                              (-100,-100), 
                              (SAMPLE_SIZE[0]+100, SAMPLE_SIZE[1]+100))
    child = (points, colors)
    return child

def find_fitness(subject, target):
    '''
    subject is an individual
    target is the target_image
    '''
    im = render(subject) 
    diff_img = ImageChops.difference(im, target)
    score = sum(ImageStat.Stat(diff_img).sum)
    return score

def _getink(self, ink, fill=None):
    # A crazy hack to speed up rendering
    '''
    if isStringType(ink):
        ink = ImageColor.getcolor(ink, self.mode)
    '''
    if self.palette and not isinstance(ink, numbers.Number):
        ink = self.palette.getcolor(ink)
    ink = self.draw.draw_ink(ink, self.mode)
    if fill is not None:
        '''
        if isStringType(fill):
            fill = ImageColor.getcolor(fill, self.mode)
        '''
        if self.palette and not isinstance(fill, numbers.Number):
            fill = self.palette.getcolor(fill)
        fill = self.draw.draw_ink(fill, self.mode)
    return ink, fill

ImageDraw.Draw._getink = _getink

def render(indiv, size=SAMPLE_SIZE):
    points, colors = indiv
    simplices = Delaunay(points, incremental=True).simplices
    if size == SAMPLE_SIZE:
        im = global_im
        im.paste((0,0,0), [0,0,size[0],size[1]])
        draw = blank_draw
    else:
        im = Image.new('RGB', size)
        draw = ImageDraw.Draw(im)
    #draw = ImageDraw.Draw(im)
    for triangle, color in zip(simplices, colors):
        x_scale = size[0]/SAMPLE_SIZE[0]
        y_scale = size[1]/SAMPLE_SIZE[1]
        verts = []
        for i in triangle:
            x = points[i][0]*x_scale
            y = points[i][1]*y_scale
            verts.append((x, y)) 
        draw.polygon(verts, fill=color)
    return im

if __name__ == '__main__':
    population = []
    new_population = []

    generations = 0
    gens_left = 0
    started = False
    global_im = Image.new('RGB', SAMPLE_SIZE)
    blank_draw = ImageDraw.Draw(global_im)

    for i in range(POPULATION_SIZE):
        population.append(generate_individual(SAMPLE_SIZE))

    population.sort(key=lambda x: find_fitness(x, target_image))
    fittest = population[0]
    try:
        while True:
            if gens_left == 0:
                if PROMPT:
                    try:
                        gens_left = int(input('How many generations? (0 to exit) '))
                        if gens_left == 0:
                            break
                    except Exception as e:
                        print('INVLID INPUT')
                        print('EXITING')
                        break
                else:
                    gens_left = NO_PROMPT_GENS
                    NO_PROMPT_GENS = 0
                    if gens_left == 0:
                        break
            if not started and DISPLAY_ON:
                plt.ion()
                plt.axis('off')
            gens_left -= 1
            generations += 1
            #rate = gens_left/(gens_left + generations)
            rate = 0.3
            
            # Find most fit
            fittest = min(population, 
                          key=lambda x: find_fitness(x, target_image))
            new_population = [fittest]
            
            # Show fittest
            if DISPLAY_ON:
                plt.clf()
                im = render(fittest)
                im.save('tmp.png')
                plt.imshow(im)
                plt.axis('off')
                plt.pause(0.05)
            
            # Mutate fittest to produce new population
            while len(new_population) < POPULATION_SIZE:
                child = mutate_parent(fittest, rate)
                new_population.append(child)
            population = new_population

            print('Generation: ' 
                  + str(generations) 
                  + '\tFittest: ' 
                  + str(find_fitness(fittest, target_image))
                  + '\tMutation rate:'
                  + str(rate))
    except KeyboardInterrupt as e:
        pass
    if PROMPT:
        save_name = input('File name? ')
    else:
        save_name = NO_PROMPT_NAME
    print('Final score: ' + str(find_fitness(fittest, target_image)))
    result = render(fittest, size=FINAL_SIZE)
    result.save('../results/' + save_name + '.png')
    print('Result saved as ' + save_name + '.png')

