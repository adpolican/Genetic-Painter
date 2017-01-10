from main import generate_individual, find_fitness
from PIL import Image
from copy import copy
from multiprocessing import Pool
import time
from PIL import ImageChops, ImageStat

FILE_NAME = 'Tina.jpg'
original_image = Image.open(FILE_NAME)
target_image = original_image.convert(mode='RGB')
pop1 = []
pop2 = []
coor = []

for x in range(target_image.size[0]):
    for y in range(target_image.size[1]):
        coor.append((x,y))

def f0(subject):
    diff_img = ImageChops.difference(subject, target_image)
    score = sum(ImageStat.Stat(diff_img).sum)
    return score

def f1(subject):
    diff_img = ImageChops.difference(subject, target_image)
    score = sum([sum(i) for i in diff_img.getdata()])
    return score

for i in range(500):
    pop1.append(generate_individual(target_image.size))
    pop2.append(generate_individual(target_image.size))
'''
start_time = time.time()
print('staring sort')
pop1.sort(key=lambda x: find_fitness(x,target_image))
print('finished sort in ' + str(time.time()-start_time))

p = Pool(5)
start_time = time.time()
print('starting parallel sort')
scored_pop2 = p.map(f, pop2)
scored_pop2.sort(key=lambda x: x[1])
print('finished parallel sort in ' + str(time.time()-start_time))
'''
start_time = time.time()
print('starting f0')
m = min(pop2, key=f0)
print('finished in ' + str(time.time() - start_time))
start_time = time.time()

print('starting f1')
m = min(pop2, key=f1)
print('finished in ' + str(time.time() - start_time))




