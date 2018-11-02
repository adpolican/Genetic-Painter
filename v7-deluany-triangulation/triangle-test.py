import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import to_hex
from scipy.spatial import Delaunay

POINTS = 100
HEIGHT = 2000
WIDTH = 1500

points = np.random.rand(POINTS,2)
points = np.multiply(points, np.array([WIDTH, HEIGHT]))
dela_tris = Delaunay(points, furthest_site=False, incremental=True)
colors = np.random.randint(0, 255, size=(len(dela_tris.simplices),3))
triangles = []
im = Image.new('RGB', (WIDTH, HEIGHT), 'black')
draw = ImageDraw.Draw(im)
for triangle, color in zip(dela_tris.simplices.copy(), colors):
    verts = [tuple(points[i]) for i in triangle]
    draw.polygon(verts, tuple(color))
im.format = 'PNG'
im.show()
im.save('test.png')

