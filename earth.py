import pygame as pg
import numpy as np

clock = pg.time.Clock()

FPS = 30

WIDTH = HEIGHT = 800

pg.init()

running = True

class Projection:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        self.background = (10, 10, 60) # black
        pg.display.set_caption("ASCII 3D Earth")
        self.surfaces = {}
        
    def addSuface(self, name, surface):
        self.surfaces[name] = surface
        
    def display(self):
        self.screen.fill(self.background)
        
        for surface in self.surfaces.values():
            for node in surface.nodes:
                pg.draw.circle(self.screen, (255, 255, 255), (int(node[0]), int(node[1])), 4, 0)
                
    def rotateAll(self, theta):
        for surface in self.surfaces.values():
            centre = surface.findCentre()
            matrix = np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                              [np.sin(theta), np.cos(theta), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
            
            surface = surface.rotate(centre, matrix)
                
class Object:
    def __init__(self) -> None:
        self.nodes = np.zeros((0,4))
    
    def addNodes(self, node_array):
        ones_col = np.ones((len(node_array),1))
        ones_added = np.hstack((node_array, ones_col))
        self.nodes = np.vstack((self.nodes, ones_added))
        
    def findCentre(self):
        return self.nodes.mean(axis=0)
    
    def rotate(self, centre, matrix):
        for i, node in enumerate(self.nodes):
            self.nodes[i] = centre + np.matmul(matrix, node - centre)
            
angle = 0
    
while(running):
    clock.tick(FPS)
    
    pv = Projection(WIDTH, HEIGHT)
    cube = Object()
    cube.addNodes(np.array([(x,y,z) for x in (200, 600) for y in (200, 600) for z in (200, 600)]))
    pv.addSuface("cube", cube)
    pv.rotateAll(angle)
    pv.display()
    for event in pg.event.get():
        if event.type == pg.QUIT:
             running = False
    angle == 0.05
    pg.display.update()