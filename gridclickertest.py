import pygame
import random

# Initialise Pygame
pygame.init()
pygame.display.set_caption('Grid Clicker')
a = pygame.image.load('sweepericon.ico')
pygame.display.set_icon(a)

# Constants
windGridheight = 400
wingGridwidth = 400
windowlength = 650
windowheight = 400
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
screen = pygame.display.set_mode((windowlength, windowheight))
clock = pygame.time.Clock()

running = True

grid = [[grey for _ in range(wingGridwidth // blocksize)] for _ in range(windGridheight // blocksize)]
adjacent_counts = [[0 for _ in range(wingGridwidth // blocksize)] for _ in range(windGridheight // blocksize)]
left_clicked = [[False for _ in range(wingGridwidth // blocksize)] for _ in range(windGridheight // blocksize)]

def drawGrid(): # Creates a grid
    for x in range(0, windGridheight, blocksize):
        for y in range(0, wingGridwidth, blocksize):
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
            if 0 <= nx < wingGridwidth // blocksize and 0 <= ny < windGridheight // blocksize:
                if (nx, ny) in targets:
                    count += 1
    return count

def reveal_square(x, y):
    if not (0 <= x < wingGridwidth // blocksize and 0 <= y < windGridheight // blocksize):
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

targets = []
while len(targets) < num_targets:
    targetX = random.randint(0, wingGridwidth // blocksize - 1)
    targetY = random.randint(0, windGridheight // blocksize - 1)
    target = (targetX, targetY)
    # Makes all mines display as red for testing
    grid[targetY][targetX] = red
    if target not in targets:
        targets.append(target)
print(f"target squares are {targets}")

while running:
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close the window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # Check if the mouse click is within a grid square
            mouseX, mouseY = pygame.mouse.get_pos()
            gridX = mouseX // blocksize
            gridY = mouseY // blocksize
            if 0 <= gridX < wingGridwidth // blocksize and 0 <= gridY < windGridheight // blocksize:  # Boundary check
                if event.button == LEFT:
                    if not left_clicked[gridY][gridX]:
                        if (gridX, gridY) in targets:
                            grid[gridY][gridX] = red
                            print(f"Clicked on grid square ({gridX}, {gridY})")
                            print("Target square clicked! Closing game")
                            running = False
                        else:
                            reveal_square(gridX, gridY)
                            print(f"Revealed square ({gridX}, {gridY}) with {adjacent_counts[gridY][gridX]} adjacent target(s)")
                elif event.button == RIGHT:
                    if grid[gridY][gridX] == green:
                        print("Not possible")   
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

    # flip() the display to put the work on the screen
    pygame.display.flip()

    clock.tick(30) # Limit fps to 30

pygame.quit()
