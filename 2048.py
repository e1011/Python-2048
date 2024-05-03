import pygame
import copy
import random

# todo: 
# create pip installable package
# fix font
# victory and game over screen
# test for bugs
pygame.init()
screen = pygame.display.set_mode((500, 720))
running = True

score = 0
highscore = 0

grid = [
    [-1, -1, -1, -1], 
    [-1, -1, -1, -1], 
    [-1, -1, -1, -1], 
    [-1, -1, -1, -1]
]

newgrid = copy.deepcopy(grid)

slidefactor = 0
growpointer = 0
growthpattern = [0, 0.1, 0.4, 0.6, 0.8, 1, 1.12, 1.18, 1.17, 1.12, 1.05, 1]

# for animation of sliding tiles
offseti = [
    [0, 0, 0, 0], 
    [0, 0, 0, 0], 
    [0, 0, 0, 0], 
    [0, 0, 0, 0]
]
offsetj = copy.deepcopy(offseti)

# for animation of new tiles
newtiles = [
    [-1, -1, -1, -1], 
    [-1, -1, -1, -1], 
    [-1, -1, -1, -1], 
    [-1, -1, -1, -1]
]
empty = copy.deepcopy(newtiles)

values = [
        [2, (238, 227, 217), (118, 108, 104)],
        [4, (239, 225, 203), (118, 108, 104)],
        [8, (242, 177, 121), (246, 247, 242)],
        [16, (245, 149, 99), (246, 247, 242)],
        [32, (246, 124, 95), (246, 247, 242)],
        [64, (246, 94, 59), (246, 247, 242)],
        [128, (237, 207, 114), (246, 247, 242)],
        [256, (239, 204, 99), (246, 247, 242)],
        [512, (236, 200, 80), (246, 247, 242)],
        [1024, (239, 197, 66), (246, 247, 242)],
        [2048, (236, 194, 46), (246, 247, 242)],
        [4096, (61, 58, 50), (246, 247, 242)],
        [8192, (61, 58, 50), (246, 247, 242)],
        [16384, (61, 58, 50), (246, 247, 242)]]

# draw background and board
def drawbackground():
    screen.fill((251,249,241))

    # empty grid
    pygame.draw.rect(screen, (186,172,158), (0, 220, 500, 500), border_radius=7)
    for i in range(0, 4):
        for j in range(0, 4):
            pygame.draw.rect(screen, (204, 191, 180), (14.5+121.5*i, 235+121.5*j, 107, 107), border_radius=3)

    # logo
    font1 = pygame.font.SysFont('ClearSans.ttf', 100)
    img1 = font1.render("2048", True, (118, 108, 104))
    screen.blit(img1, (20, 75))

    # button
    pygame.draw.rect(screen, (145,122,103,255), (370, 140, 130, 40), border_radius = 2)
    font1 = pygame.font.SysFont('ClearSans.ttf', 30)
    img1 = font1.render("New Game", True, (255, 255, 255))
    screen.blit(img1, (380, 150))

    # scores
    pygame.draw.rect(screen, (186,172,158), (190, 0, 150, 55), border_radius = 2)
    pygame.draw.rect(screen, (186,172,158), (350, 0, 150, 55), border_radius = 2)
    font1 = pygame.font.SysFont('ClearSans.ttf', 25)
    img1 = font1.render("Best: ", True, (255, 255, 255))
    img2 = font1.render(str(highscore), True, (255, 255, 255))
    screen.blit(img1, (380, 10))
    screen.blit(img2, (380, 30))
    img1 = font1.render("Score: ", True, (255, 255, 255))
    img2 = font1.render(str(highscore), True, (255, 255, 255))
    screen.blit(img1, (220, 10))
    screen.blit(img2, (220, 30))

# rotate 90 degrees clockwise
def rotate(grid):
    grid2 = copy.deepcopy(grid)
    for i in range(0, 4):
        for j in range(0, 4):
            grid2[i][3-j] = grid[j][i]
    return grid2

# spawn one new tile randomly
def spawn(grid):
    grid = copy.deepcopy(grid)
    while True:
        i = random.randint(0, 3)
        j = random.randint(0, 3)
        if (grid[i][j] == -1):
            grid[i][j] = (random.randint(1, 10) == 1)
            newtiles[i][j] = grid[i][j]
            return grid

# direction 0 -> up, 1 -> left, 2 -> down, 3 -> right
def move(grid, direction):
    global score
    grid = copy.deepcopy(grid)
    for i in range(0, direction):
        grid = rotate(grid)
    
    # this moves tiles up
    for i in range(0, 4):
        for j in range(1, 4):
            k = copy.deepcopy(j)
            while (grid[k][i] != -1):
                if (k == 0):
                    break
                elif (grid[k-1][i] == -1):
                    grid[k-1][i] = grid[k][i]
                    grid[k][i] = -1
                    k -= 1
                elif (grid[k-1][i] == grid[k][i]):
                    score += values[grid[k][i]][0]
                    grid[k-1][i] += 1
                    grid[k][i] = -1
                    if (direction == 0):
                        newtiles[k-1][i] = grid[k-1][i]
                    elif (direction == 1):
                        newtiles[3-i][k-1] = grid[k-1][i]
                    elif (direction == 2):
                        newtiles[4-k][3-i] = grid[k-1][i]
                    else:
                        newtiles[i][4-k] = grid[k-1][i]
                    k -= 1
                    break
                else:
                    break
            if (direction == 0):
                offseti[j][i] = k-j
            elif (direction == 1):
                offsetj[3-i][j] = k-j
            elif (direction == 2):
                offseti[3-j][3-i] = j-k
            else:
                offsetj[i][3-j] = j-k

    for i in range(0, 4-direction):
        grid = rotate(grid)

    return grid

# checks if there are any possible moves
def checkdead(grid):
    dead = True
    for i in range(0, 4):
        for j in range(0, 4):
            if (grid[i][j] == -1):
                dead = False
            if (i < 3 and grid[i][j] == grid[i+1][j]):
                dead = False
            if (j < 3 and grid[i][j] == grid[i][j+1]):
                dead = False
    return dead

# adds new tiles to grid, after animation complete
def resetanimation():
    global growpointer, slidefactor, grid, newtiles, offseti, offsetj
    growpointer = 0
    slidefactor = 0
    grid = copy.deepcopy(newgrid)
    newtiles = copy.deepcopy(empty)

    offseti = [
        [0, 0, 0, 0], 
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    offsetj = copy.deepcopy(offseti)

def maketile(details):
    tile = pygame.Surface((107, 107), pygame.SRCALPHA)
    pygame.draw.rect(tile, details[1], (0, 0, 107, 107), border_radius=3)
    font1 = pygame.font.SysFont('ClearSans.ttf', 70)
    img1 = font1.render(str(details[0]), True, details[2])
    tile.blit(img1, (35, 35))
    return tile

while running:
    drawbackground()

    # draw all tiles
    tiles = []
    for i in range(0, 4): 
        for j in range(0, 4):
            if (grid[i][j] != -1):
                tile = maketile(values[grid[i][j]])
                tiles.append([abs(offseti[i][j])+abs(offsetj[i][j]), i, j, tile])
    tiles.sort()
    tiles.reverse()
    for i in range(0, len(tiles)):
        screen.blit(tiles[i][3], 
                    (14.5+121.5*tiles[i][2]+(121.5*slidefactor*offsetj[tiles[i][1]][tiles[i][2]]), 
                     235+121.5*tiles[i][1]+(121.5*slidefactor*offseti[tiles[i][1]][tiles[i][2]])))
    
    # growing animation
    for i in range(0, 4):
        for j in range(0, 4):
            if (newtiles[i][j] != -1):
                tile = maketile(values[newtiles[i][j]])
                tile = pygame.transform.scale(tile, (107*growthpattern[growpointer], 
                                                     107*growthpattern[growpointer]))
                screen.blit(tile, (14.5+121.5*j+(53.5*(1-growthpattern[growpointer])), 
                                   235+121.5*i+(53.5*(1-growthpattern[growpointer]))))

    # empty grid edge case
    if (newgrid == empty):
        newgrid = spawn(grid)

    # animation logic
    if (grid != newgrid and slidefactor < 1):
        slidefactor += 0.15
        slidefactor = min(slidefactor, 1)

    if (slidefactor == 1 and newtiles != empty):
        growpointer += 1
    
    if (growpointer >= len(growthpattern)):
        resetanimation()

    # game over
    if (checkdead(grid)):
        running = False

    # handle user input
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        elif (event.type == pygame.KEYDOWN):
            resetanimation()

            if (event.key == pygame.K_UP):
                newgrid = move(grid, 0)
            elif (event.key == pygame.K_LEFT):
                newgrid = move(grid, 1)
            elif (event.key == pygame.K_DOWN):
                newgrid = move(grid, 2)
            else:
                newgrid = move(grid, 3)
            
            highscore = max(score, highscore)

            # spawn new if moved
            if (grid != newgrid):
                newgrid = spawn(newgrid)
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mouse = pygame.mouse.get_pos()
            # restart button pressed
            if (mouse[0] > 370 and mouse[0] < 500 and mouse[1] < 180 and mouse[1] > 140):
                newgrid = copy.deepcopy(empty)
                grid = copy.deepcopy(newgrid)
                resetanimation()
                score = 0

    pygame.display.flip()


pygame.quit()