import configparser
import random

import numpy as np
import cv2 as cv

from mutators.abschromosome import AbsChromosome

NAME = 'solidTriangles'
CONFIG = configparser.ConfigParser()
CONFIG.read('./config/solidtriangles.ini')


class Chromosome(AbsChromosome):
    def __init__(self, context):
        '''
        Keyword arguments:
        img -- a numpy array representing the target image 
        with shape (height, width, 3)
        '''
        img = context.target_image
        self.height, self.width, _ = img.shape
        self.colors = img.reshape(self.height*self.width, 3)
        bg_color = random.choice(self.colors)

        self.genes = np.zeros(img.shape, np.uint8)
        self.genes[:, :] = bg_color
        self.target = context.target_image
        self.context = context

    def crossover(self, mate, context):
        # No real crossover, we're just randomly choosing one to copy
        parent = random.choice((self, mate))
        child = Chromosome(context)
        child.genes[:] = self.genes # copy values
        return child

    def mutate(self):
        # Place a random triangle on the canvas
        vertices = np.zeros((3, 2))
        center = np.random.randint(
            low=1,
            high=max(self.height, self.width),
            size=(2,))
        vertices[:] = center
        
        '''
        gens_left = self.context.gens_left
        total_gens = int(self.context.config_info['SETTINGS']['GENERATIONS'])
        lowest_ratio = 0.5
        prog_ratio = gens_left/total_gens
        prog_ratio = max(prog_ratio, lowest_ratio)

        low = int(CONFIG['SETTINGS']['TRIANGLE_RANGE_MIN'])
        high = int(CONFIG['SETTINGS']['TRIANGLE_RANGE_MAX'])
        low *= prog_ratio
        high *= pro_ratio
        '''

        
        offsets = np.random.randint(
            low=int(CONFIG['SETTINGS']['TRIANGLE_RANGE_MIN']),
            high=int(CONFIG['SETTINGS']['TRIANGLE_RANGE_MAX']),
            size=(3, 2))
        scale = int(CONFIG['SETTINGS']['TRIANGLE_RANGE_MAX'])
        #offsets = np.random.standard_normal((3,2))*scale
        vertices += offsets
        vertices = np.int32(vertices)
        color = random.choice(self.colors)
        color = [int(x) for x in color]
        cv.fillPoly(self.genes, pts=[vertices], color=color)
        return self

    def evaluate(self):
        # Pixel by pixel comparison
        diff = np.abs(self.target - self.genes)
        return np.sum(diff)

    def get_name(self):
        return NAME

    def render(self):
        return self.genes
