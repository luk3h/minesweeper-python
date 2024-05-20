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
grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
pink = (255, 192, 203)
LEFT = 1
RIGHT = 3
score = 0
num_targets = 80

# Setup the display
screen = pygame.display.set_mode((windheight, windwidth))
clock = pygame.time.Clock()
pygame.font.init()

# Default game font
game_font = pygame.font.Font("assets\cmb10.ttf", 24)

running = True
first_click = True

grid = [[grey for _ in range(windwidth // blocksize)] for _ in range(windheight // blocksize)]
adjacent_counts = [[0 for _ in range(windwidth // blocksize)] for _ in range(windheight // blocksize)]
left_clicked = [[False for _ in range(windwidth // blocksize)] for _ in range(windheight // blocksize)]

def drawGrid(): # Creates a grid
    for x in range(0, windheight, blocksize):
        for y in range(0, windwidth, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            colour = grid[y // blocksize][x // blocksize]
            pygame.draw.rect(screen, colour, rect)
            pygame.draw.rect(screen, black, rect, 1)
            if grid[y // blocksize][x // blocksize] == green:
                count = adjacent_counts[y // blocksize][x // blocksize]
                if count > 0:
                    font = pygame.font.Font(None, 24)
                    text = font.render(str(count), True, black)
                    screen.blit(text, (x + blocksize // 3, y + blocksize // 6))

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
    grid[y][x] = green
    
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

def gamefailed():
    global running

    screen.fill(grey)

    text_surface = game_font.render("Game Over", True, black)
    text_rect = text_surface.get_rect(center=(windwidth // 2, windheight // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            gridX = mouseX // blocksize
            gridY = mouseY // blocksize
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    if first_click:
                        place_targets(gridX, gridY)
                        first_click = False
                    if not left_clicked[gridY][gridX]:
                        if (gridX, gridY) in targets:
                            grid[gridY][gridX] = red
                            print(f"Clicked on grid square ({gridX}, {gridY})")
                            print("Target square clicked! Closing game")
                            gamefailed()
                            break
                        else:
                            reveal_square(gridX, gridY)
                            print(f"Revealed square ({gridX}, {gridY}) with {adjacent_counts[gridY][gridX]} adjacent target(s)")

                elif event.button == RIGHT:
                    if grid[gridY][gridX] == green:
                        print("Not possible to mark green square.")   
                    elif grid[gridY][gridX] != pink:
                        grid[gridY][gridX] = pink
                        print("Target square marked!")
                        score += 1
                    else:
                        grid[gridY][gridX] = grey
                        print("Target square unmarked!")

    # Render game
    screen.fill(grey)
    drawGrid()

    pygame.display.flip()

pygame.quit()
