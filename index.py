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
ROWS, COLS = 50,50
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

def IsValidNeighbor(tile, neighborTile, direction):
    neighborDirection = 0

    if direction >= 2:
        neighborDirection = direction - 2
    else:
        neighborDirection = direction + 2
    
    return tile.edges[direction] == neighborTile.edges[neighborDirection]

def CollapseCell(GRID):
    minEntropy = float("inf")
    targetCell = None

    for row in range(ROWS):
        for col in range(COLS):
            cell = GRID[row][col]
            if not cell.collapsed and len(cell.options) < minEntropy:
                minEntropy = len(cell.options)
                targetCell = cell, row, col
    
    if targetCell:
        cell, row, col = targetCell
        chosenTile = random.choice(cell.options)
        cell.options = [chosenTile]
        cell.collapsed = True
        return row, col
    
    return None

def propagate(GRID,row,col):
    directions = [(-1,0),(0,1),(1,0),(0,-1)]
    tileIndex = GRID[row][col].options[0]
    tile = Tiles[tileIndex]

    for d,(dy,dx) in enumerate(directions):
        neighborRow, neighborCol = row + dy, col + dx
        if 0 <= neighborRow < ROWS and 0 <= neighborCol < COLS:
            neighbor = GRID[neighborRow][neighborCol]
            if not neighbor.collapsed :
                neighbor.options = [
                    i for i in neighbor.options if IsValidNeighbor(tile,Tiles[i],d)
                ]

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
    
    result = CollapseCell(GRID)
    if result:
        row, col = result
        propagate(GRID,row,col)

    window.fill((0,0,0))

    draw()

    pygame.display.flip()

pygame.quit