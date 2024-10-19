import pygame
import numpy as np
import random
import os
import copy

class Tile:
    def __init__(self, image, edges):
        self.image = image
        self.edges = edges

class Cell:
    def __init__(self, options):
        self.collapsed = False
        self.options = options

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 4,4
CELL_SIZE = WIDTH // COLS
GRID = np.empty((ROWS, COLS),object)

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wave Function Collapse")

image_folder = os.path.join(os.path.dirname(__file__),"Tiles")
image_files = ["Tile1.png","Tile5.png","Tile8.png","Tile6.png","Tile7.png"]#,"Tile5.png","Tile6.png","Tile7.png","Tile8.png"
images = []

for img_file in image_files:
    img_path = os.path.join(image_folder,img_file)
    img = pygame.image.load(img_path)
    img = pygame.transform.scale(img, (CELL_SIZE,CELL_SIZE))
    images.append(img)

Tiles = [
    Tile(images[0],[0,0,0,0]), #blank
    Tile(images[1],[1,1,0,1]), #up
    Tile(images[2],[1,1,1,0]), #right
    Tile(images[3],[0,1,1,1]), #down
    Tile(images[4],[1,0,1,1])  #left
]

GRID = []
for i in range(ROWS):
    row = []
    for j in range(COLS):
        cell = Cell(list(range(len(Tiles))))
        row.append(cell)
    GRID.append(row)
        
def draw():
    for row in range(ROWS):
        for col in range(COLS):
            cell = GRID[row][col]
            if cell.collapsed:
                index = cell.options[0]
                x, y = col * CELL_SIZE, row * CELL_SIZE
                window.blit(images[index], (x, y))
                    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    window.fill((0,0,0))

    draw()

    pygame.display.flip()

pygame.quit