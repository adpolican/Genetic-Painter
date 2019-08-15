import configparser
import random

import numpy as np
import cv2 as cv

from mutators.abschromosome import AbsChromosome

NAME = 'eqTriangles'
CONFIG = configparser.ConfigParser()
CONFIG.read('./config/eqtriangles.ini')


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
        # Place an equilateral triangle on the canvas
        vertices = np.array([[0, 1],
                             [-0.866, -0.5], 
                             [0.866, -0.5]])
        max_radius = int(CONFIG['SETTINGS']['MAX_RADIUS'])
        min_radius = int(CONFIG['SETTINGS']['MIN_RADIUS'])
        scale = random.randint(min_radius, max_radius)
        vertices *= scale
        center = np.random.randint(
            low=1,
            high=max(self.height, self.width),
            size=(2,))
        vertices += center
        
        vertices = np.int32(vertices)
        color = random.choice(self.colors)
        color = [int(x) for x in color]
        cv.fillPoly(self.genes, pts=[vertices], color=color)

        # Pixel by pixel comparison
        diff = np.abs(self.target - self.genes)
        self.fitness = np.sum(diff)

        return self


    def evaluate(self): 
        try:
            return self.fitness
        except:
            diff = np.abs(self.target - self.genes)
            self.fitness = np.sum(diff)
            return self.fitness

    def get_name(self):
        return NAME

    def render(self):
        return self.genes
