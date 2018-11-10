import configparser
import random

import numpy as np
import cv2 as cv

from mutators.abschromosome import AbsChromosome

NAME = 'solidTriangles'
CONFIG = configparser.ConfigParser()
CONFIG.read('./config/solidtriangles.ini')


class Chromosome(AbsChromosome):
    def __init__(self, img):
        '''
        Keyword arguments:
        img -- a numpy array representing the target image 
        with shape (height, width, 3)
        '''
        self.height, self.width, _ = img.shape
        self.colors = img.reshape(self.height*self.width, 3)
        bg_color = random.choice(self.colors)

        self.genes = np.zeros(img.shape, np.uint8)
        self.genes[:, :] = bg_color
        self.target = img

    def crossover(self, mate):
        # No real crossover, we're just randomly choosing one
        parent = random.choice((self, mate))
        child = Chromosome(self.target)
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
        offsets = np.random.randint(
            low=CONFIG['SETTINGS']['TRIANGLE_RANGE_MIN'],
            high=CONFIG['SETTINGS']['TRIANGLE_RANGE_MAX'],
            size=(3, 2))
        #offsets = np.zeros((3,3))
        vertices += offsets
        vertices = np.int32(vertices)
        #vertices.reshape((-1, 1, 2))
        color = random.choice(self.colors)
        color = [int(x) for x in color]
        #cv.polylines(self.genes, [vertices], True, color)
        cv.fillPoly(self.genes, pts=[vertices], color=color)

    def evaluate(self):
        # Pixel by pixel comparison
        diff = np.abs(self.target - self.genes)
        return np.sum(diff)

    def get_name(self):
        return NAME

    def render(self):
        return self.genes
