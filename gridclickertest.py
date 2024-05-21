import pygame
import random

# Initialise Pygame
pygame.init()
pygame.display.set_caption('Grid Clicker')
a = pygame.image.load('assets/sweepericon.ico')
pygame.display.set_icon(a)

# Constants
windHeight = 400
windWidth = 400
blockSize = 20
blue = (0, 0, 255)

grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 128, 0)
pink = (255, 192, 203)
darkGrey = (169, 169, 169)
kindaDarkGrey = (180, 180, 180)
darkBlue = (0, 0, 128)
darkRed = (128, 0, 0)
teal = (0, 128, 128)

LEFT = 1
RIGHT = 3
score = 0
numTargets = 80


# Setup the display
screen = pygame.display.set_mode((windHeight, windWidth))
clock = pygame.time.Clock()
pygame.font.init()

# Default game font
gameFont = pygame.font.Font("assets/cmb10.ttf", 24)
score_font = pygame.font.Font("assets/cmb10.ttf", 16)

flagImage = pygame.image.load("assets/flag.png")
flagImage = pygame.transform.scale(flagImage, (blockSize, blockSize))

blockImage = pygame.image.load("assets/block.png")
blockImage = pygame.transform.scale(blockImage, (blockSize, blockSize))

running = True
startMenuRunning = True
firstClick = True

def startMenu():
    global startMenuRunning
    while startMenuRunning:
        screen.fill(grey)
        textSurface = gameFont.render("Minesweeper", True, black)
        textRect = textSurface.get_rect(center=(windWidth // 2, windHeight // 2))
        screen.blit(textSurface, textRect)
        button = pygame.draw.rect(screen,pink,[windWidth/3,windHeight/1.5,160,60])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == LEFT:
                    if button.collidepoint(event.pos):
                        print("Button clicked!")
                        startMenuRunning = False

grid = [[grey for _ in range(windWidth // blockSize)] for _ in range(windHeight // blockSize)]
adjacentCounts = [[0 for _ in range(windWidth // blockSize)] for _ in range(windHeight // blockSize)]
leftClicked = [[False for _ in range(windWidth // blockSize)] for _ in range(windHeight // blockSize)]

def drawGrid():
    for x in range(0, windHeight, blockSize):
        for y in range(0, windWidth, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            colour = grid[y // blockSize][x // blockSize]
            pygame.draw.rect(screen, colour, rect)
            pygame.draw.rect(screen, kindaDarkGrey, rect, 1)
            if grid[y // blockSize][x // blockSize] == darkGrey:
                count = adjacentCounts[y // blockSize][x // blockSize]
                if count > 0:
                    textColour = getCountColour(count)
                    font = pygame.font.Font(None, 24)
                    text = font.render(str(count), True, textColour)
                    screen.blit(text, (x + blockSize // 3, y + blockSize // 6))
            elif grid[y // blockSize][x // blockSize] == pink:
                screen.blit(flagImage, (x, y))
            elif grid[y // blockSize][x // blockSize] == grey:
                screen.blit(blockImage, (x, y))

def getCountColour(count):
    if count == 1:
        return blue
    elif count == 2:
        return green
    if count == 3:
        return red
    elif count == 4:
        return darkBlue
    if count == 5:
        return darkRed
    elif count == 6:
        return teal
    if count == 7:
        return black
    elif count == 8:
        return grey
    else:
        return black
    
def countAdjacentTargets(x, y):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < windWidth // blockSize and 0 <= ny < windHeight // blockSize:
                if (nx, ny) in targets:
                    count += 1
    return count

def revealSquare(x, y):
    if not (0 <= x < windWidth // blockSize and 0 <= y < windHeight // blockSize):
        return
    if leftClicked[y][x]:
        return
    
    leftClicked[y][x] = True
    adjacentCount = countAdjacentTargets(x, y)
    adjacentCounts[y][x] = adjacentCount
    grid[y][x] = darkGrey
    
    if adjacentCount == 0:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:
                    revealSquare(x + dx, y + dy)

def placeTargets(excludeX, excludeY):
    global targets
    targets = []
    while len(targets) < numTargets:
        targetX = random.randint(0, windWidth // blockSize - 1)
        targetY = random.randint(0, windHeight // blockSize - 1)
        target = (targetX, targetY)

        if target not in targets and target != (excludeX, excludeY):
            targets.append(target)
            
def gamefailed():
    global running
    screen.fill(grey)
    textSurface = gameFont.render("Game Over", True, black)
    textRect = textSurface.get_rect(center=(windWidth // 2, windHeight // 2))
    screen.blit(textSurface, textRect)
    pygame.display.flip()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Optionally, add a restart feature
                running = False

def gameWon():
    global running, score
    scoreText = str(score)
    screen.fill(grey)
    textSurface = gameFont.render("You Win!", True, black)
    textRect = textSurface.get_rect(center=(windWidth // 2, windHeight // 2))
    score_image = score_font.render(f"Score : {scoreText}", True, black)
    score_rect = score_image.get_rect(center=(windWidth / 1.5, windHeight / 1.5))
    screen.blit(score_image, score_rect)
    screen.blit(textSurface, textRect)
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
            gridX = mouseX // blockSize
            gridY = mouseY // blockSize
            
            if event.button == LEFT:
                if firstClick:
                    placeTargets(gridX, gridY)
                    firstClick = False
                if not leftClicked[gridY][gridX]:
                    if (gridX, gridY) in targets:
                        grid[gridY][gridX] = red
                        gamefailed()
                        break
                    else:
                        revealSquare(gridX, gridY)
            elif event.button == RIGHT:
                if firstClick:
                    placeTargets(gridX, gridY)
                    firstClick = False
                if grid[gridY][gridX] == darkGrey:
                    print("Not possible to mark clicked square.")   
                elif grid[gridY][gridX] != pink:
                    grid[gridY][gridX] = pink
                    print("Square marked!")
                    if ((gridX, gridY)) in targets:
                        score += 1
                        print(score)
                else:
                    grid[gridY][gridX] = grey
                    print("Target square unmarked!")
                    if ((gridX, gridY)) in targets:
                        score -= 1
                        print(score)
        elif score == numTargets:
            gameWon()

    # Render game
    startMenu()
    # screen.fill(grey)
    drawGrid()
    pygame.display.flip()

pygame.quit()

