import random
from PIL import Image, ImageChops, ImageStat, ImageFont, ImageDraw, ImageOps
from copy import copy
from random import randint

POPULATION_SIZE = 40
SKIP_COUNT = 3
MAX_LETTER_SIZE = 200
MIN_LETTER_SIZE = 1
COLOR_COUNT = 100
FILE_NAME = '../sources/carrie.jpg'
FONT_NAME = '../fonts/odin.otf'
DISPLAY_ON = False

if DISPLAY_ON:
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg


def generate_individual(size):
    new_indv = mutate_parent(Image.new('RGB', size, '#e0e0e0'))
    return new_indv

def mutate_parent(image_data):
    child = image_data.copy()
    x = random.choice(range(-50,child.size[0]))
    y = random.choice(range(-50,child.size[1]))
    font_size = random.choice(range(MIN_LETTER_SIZE, MAX_LETTER_SIZE))
    letter = random.choice(alphabet)
    font_color = random.choice(colors)
    #font_color = (100,100,0)
    draw = ImageDraw.Draw(child)
    draw_font = ImageFont.truetype(FONT_NAME, size=font_size) 
    draw.text((x,y), letter, font=draw_font, fill=font_color)
    return (child,(x,y),letter,font_size,font_color)

def find_fitness(subject, target):
    diff_img = ImageChops.difference(subject, target)
    score = sum(ImageStat.Stat(diff_img).sum)
    return score



if __name__ == '__main__':
    alphabet = []
    population = []
    new_population = []
    letter_info = []

    generations = 0
    gens_left = 0
    started = False

    alphabet = list(raw_input('alphabet: '))
    original_image = Image.open(FILE_NAME)
    target_image = original_image.convert(mode='RGB')
    img_colors = ImageOps.posterize(target_image,4).getcolors(100000000)
    img_colors.sort()
    img_colors.reverse()
    colors = [i[1] for i in img_colors][:COLOR_COUNT]
    image_size = target_image.size
    for i in range(POPULATION_SIZE):
        population.append(generate_individual(image_size))
    population.sort(key=lambda x: find_fitness(x[0],target_image))
    fittest = population[0]
    letter_info.append((fittest[1],fittest[2],fittest[3],fittest[4]))
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
            if not started and DISPLAY_ON:
                plt.ion()
                plt.axis('off')
                '''
                window = pyglet.window.Window()
                p.start() 
                started = True
                '''
            gens_left -= 1
            generations += 1
            
            # Find most fit
            fittest = min(population, key=lambda x: find_fitness(x[0],target_image))
            new_population = [fittest]
            letter_info.append((fittest[1],fittest[2],fittest[3],fittest[4]))
            
            # Show fittest
            if DISPLAY_ON:
                plt.clf()
                plt.imshow(fittest[0])
                plt.axis('off')
                plt.pause(0.05)
            
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
    result = Image.new('RGB', (size_x,size_y),'#e0e0e0')
    draw = ImageDraw.Draw(result)
    for i in letter_info:
        draw_font = ImageFont.truetype(FONT_NAME, size=i[2]*int(scale))
        x,y = i[0]
        x *= scale
        y *= scale
        draw.text((x,y), i[1], font=draw_font, fill=i[3])
    result.save('../results/' + save_name + '.png')
    print('Result saved as ' + save_name+ '.png')

