import pygame
import random

# Initialise Pygame
pygame.init()
pygame.display.set_caption('Grid Clicker')
a = pygame.image.load('assets/sweepericon.ico')
pygame.display.set_icon(a)

# Constants
windheight = 400
windwidth = 400
blocksize = 20

blue = (0, 0, 255)
grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 128, 0)
pink = (255, 192, 203)
darkgrey = (169, 169, 169)
kinddarkgrey = (180, 180, 180)
purple = (50, 6, 128)
darkred = (128, 0, 0)
teal = (0, 128, 128)

LEFT = 1
RIGHT = 3
score = 0
num_targets = 64


# Setup the display
screen = pygame.display.set_mode((windheight, windwidth))
clock = pygame.time.Clock()
pygame.font.init()

# Default game font
game_font = pygame.font.Font("assets/cmb10.ttf", 24)


flag_image = pygame.image.load("assets/flag.png")
flag_image = pygame.transform.scale(flag_image, (blocksize, blocksize))

block_image = pygame.image.load("assets/block.png")
block_image = pygame.transform.scale(block_image, (blocksize, blocksize))

running = True
first_click = True

grid = [[grey for _ in range(windwidth // blocksize)] for _ in range(windheight // blocksize)]
adjacent_counts = [[0 for _ in range(windwidth // blocksize)] for _ in range(windheight // blocksize)]
left_clicked = [[False for _ in range(windwidth // blocksize)] for _ in range(windheight // blocksize)]




def drawGrid():
    for x in range(0, windheight, blocksize):
        for y in range(0, windwidth, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            colour = grid[y // blocksize][x // blocksize]
            pygame.draw.rect(screen, colour, rect)
            pygame.draw.rect(screen, kinddarkgrey, rect, 1)
            if grid[y // blocksize][x // blocksize] == darkgrey:
                count = adjacent_counts[y // blocksize][x // blocksize]
                if count > 0:
                    text_colour = get_count_colour(count)
                    font = pygame.font.Font(None, 24)
                    text = font.render(str(count), True, text_colour)
                    screen.blit(text, (x + blocksize // 3, y + blocksize // 6))
            elif grid[y // blocksize][x // blocksize] == pink:
                screen.blit(flag_image, (x, y))
            elif grid[y // blocksize][x // blocksize] == grey:
                screen.blit(block_image, (x, y))

def get_count_colour(count):
    if count == 1:
        return blue
    elif count == 2:
        return green
    if count == 3:
        return red
    elif count == 4:
        return purple
    if count == 5:
        return darkred
    elif count == 6:
        return teal
    if count == 7:
        return black
    elif count == 8:
        return grey
    else:
        return black
    
def count_adjacent_targets(x, y):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < windwidth // blocksize and 0 <= ny < windheight // blocksize:
                if (nx, ny) in targets:
                    count += 1
    return count

def reveal_square(x, y):
    if not (0 <= x < windwidth // blocksize and 0 <= y < windheight // blocksize):
        return
    if left_clicked[y][x]:
        return
    
    left_clicked[y][x] = True
    adjacent_count = count_adjacent_targets(x, y)
    adjacent_counts[y][x] = adjacent_count
    grid[y][x] = darkgrey
    
    if adjacent_count == 0:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:
                    reveal_square(x + dx, y + dy)

def place_targets(exclude_x, exclude_y):
    global targets
    targets = []
    while len(targets) < num_targets:
        targetX = random.randint(0, windwidth // blocksize - 1)
        targetY = random.randint(0, windheight // blocksize - 1)
        target = (targetX, targetY)

        if target not in targets and target != (exclude_x, exclude_y):
            targets.append(target)
            
def write(text, x, y, color="Black",):
    text = game_font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(center=(windwidth // 2, y))
    return text, text_rect

def gamefailed():
    global running
    score_text = str(score)
    targets_text = str(num_targets)
    screen.fill(grey)
    text, text_rect = write("You lose!", 10, 15)
    score_image, score_rect = write(f"Mines marked : {score_text} / {targets_text}", 10, 45)
    screen.blit(score_image, score_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Optionally, add a restart feature
                running = False

def gamewon():
    global running
    targets_text = str(num_targets)
    score_text = str(score)
    screen.fill(grey)
    text, text_rect = write("You win!", 10, 15)
    score_image, score_rect = write(f"Mines marked : {score_text} / {targets_text}", 10, 45)
    screen.blit(score_image, score_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Optionally, add a restart feature
                running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            gridX = mouseX // blocksize
            gridY = mouseY // blocksize
            
            if event.button == LEFT:
                if first_click:
                    place_targets(gridX, gridY)
                    first_click = False
                if not left_clicked[gridY][gridX]:
                    if (gridX, gridY) in targets:
                        grid[gridY][gridX] = red
                        gamefailed()
                        break
                    else:
                        reveal_square(gridX, gridY)
            elif event.button == RIGHT:
                if first_click:
                    place_targets(gridX, gridY)
                    first_click = False
                if grid[gridY][gridX] == darkgrey:
                    print("Not possible to mark clicked square.")   
                elif grid[gridY][gridX] != pink:
                    grid[gridY][gridX] = pink
                    print("Square marked!")
                    if ((gridX, gridY)) in targets:
                        score += 1
                else:
                    grid[gridY][gridX] = grey
                    print("Target square unmarked!")
                    if ((gridX, gridY)) in targets:
                        score -= 1
        elif score == num_targets:
            gamewon()

    # Render game
    screen.fill(grey)
    drawGrid()
    pygame.display.flip()

pygame.quit()
