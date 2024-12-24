import pygame
import sys
import time

pygame.init()

screenWidth = 800
screenHeight = 600
cellSize = 20
rows = screenHeight // cellSize
cols = screenWidth // cellSize

screen = pygame.display.set_mode((screenWidth, screenHeight + 50))
pygame.display.set_caption("Jeu de la Vie")

BLACK = (0, 0, 0)
WHITE = (100, 100, 100)
GREEN = (0, 100, 100)
BLUE = (0, 0, 100)
RED = (100, 0, 0)

grid = [[0 for _ in range(cols)] for _ in range(rows)]
running = True
runningSimulation = False

def drawGrid():
    for x in range(cols):
        for y in range(rows):
            rect = pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)

def toggleCell(pos):
    x, y = pos
    colN = x // cellSize
    rowN = y // cellSize
    if 0 <= colN < cols and 0 <= rowN < rows:  
        grid[rowN][colN] = 1 - grid[rowN][colN]

def draw_start_button():
    button_rect = pygame.Rect(200, screenHeight + 10, 150, 30)
    pygame.draw.rect(screen, BLUE, button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Start", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

def draw_restart_button():
    button_rect = pygame.Rect(400, screenHeight + 10, 150, 30)
    pygame.draw.rect(screen, RED, button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Restart", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

def reset_grid():
    global grid, runningSimulation
    grid = [[0 for _ in range(cols)] for _ in range(rows)] 
    runningSimulation = False 

def update_grid():
    global grid
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            neighbors = sum(
                grid[y + dy][x + dx]
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (dx != 0 or dy != 0) and 0 <= x + dx < cols and 0 <= y + dy < rows
            )
            if grid[y][x] == 1 and neighbors in [2, 3]:
                new_grid[y][x] = 1
            elif grid[y][x] == 0 and neighbors == 3:
                new_grid[y][x] = 1
    grid = new_grid

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type ==pygame.MOUSEWHEEL:
            if event.y > 0 :
                cellSize += 2 
            if event.y < 0 :
                cellSize -= 2
            cellSize = max(5, min(cellSize, 50))
            rows = screenHeight // cellSize
            cols = screenWidth // cellSize
            new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
            for y in range(min(len(grid), rows)):
                for x in range(min(len(grid[0]), cols)):
                    new_grid[y][x] = grid[y][x]
            grid = new_grid
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not runningSimulation:
                start_button_rect = draw_start_button()
                if start_button_rect.collidepoint(event.pos):
                    runningSimulation = True
            restart_button_rect = draw_restart_button()
            if restart_button_rect.collidepoint(event.pos):
                reset_grid() 
            if not runningSimulation:
                toggleCell(event.pos)

    screen.fill(BLACK)

    drawGrid()

    draw_start_button()
    draw_restart_button()
    
    button_rect = pygame.Rect(600, 10, 150, 30)
    if runningSimulation:
        color=  GREEN
        state = "Running"
    else : 
        color = RED
        state = "Stopped"
    pygame.draw.rect(screen, color, button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render(state, True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    if runningSimulation:
        update_grid()
        time.sleep(0.1)

    pygame.display.flip()

pygame.quit()
sys.exit()
