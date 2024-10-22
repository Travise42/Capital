import pygame

import random

import src.Board as Board

import src.Palette as palette
import src.Constants as constants
from src.Button import Button

WIDTH, HEIGHT = 1000, 800
BOARD_SIZE = 600
FPS = 30

def init():
    
    pygame.init()
    
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    easy_button = Button("Easy", 300, 350, 100, 100)
    medium_button = Button("Medium", 450, 350, 100, 100)
    hard_button = Button("Hard", 600, 350, 100, 100)
    
    board_surf = pygame.Surface((BOARD_SIZE,)*2)
    board = None
    marked_board = None
    initial_type = None
    invalid = False
    found_capitals = 0
    success = False
    restart_delay = 0
    
    running = True
    screen = constants.HOME
    while running:
        
        # Handle events
        
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            
            # Exit the application
            if event.type == pygame.QUIT:
                running = False
                
            # Hover over buttons
            elif event.type == pygame.MOUSEMOTION:
                if screen == constants.GAME:
                    if initial_type == None or not pygame.mouse.get_pressed()[2]:
                        continue
                    for row in range(len(board)):
                        for column in range(len(board)):
                            if marked_board[row][column] != initial_type:
                                continue
                            
                            if (0 < mouse_pos[0] - square_size*column - (WIDTH - BOARD_SIZE) / 2 < square_size and
                                0 < mouse_pos[1] - square_size*row - (HEIGHT - BOARD_SIZE) / 2 < square_size):
                                marked_board[row][column] = 1 - initial_type
            
            # Click spaces
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if screen == constants.GAME:
                    initial_type = None
                    for row in range(len(board)):
                        for column in range(len(board)):
                            x = square_size*column
                            y = square_size*row
                            if 0 < mouse_pos[0] - x - (WIDTH - BOARD_SIZE) / 2 < square_size and 0 < mouse_pos[1] - y - (HEIGHT - BOARD_SIZE) / 2 < square_size:
                                # Add / remove X
                                if pygame.mouse.get_pressed()[2]:
                                    initial_type = marked_board[row][column]
                                    marked_board[row][column] = 1 - initial_type
                                # Add / remove capital
                                elif pygame.mouse.get_pressed()[0]:
                                    marked_board[row][column] = 2 - marked_board[row][column]
            
            # Click buttons
            elif event.type == pygame.MOUSEBUTTONUP:
                initial_type = None
                if screen == constants.HOME:
                    if easy_button.pressed:
                        board = Board.create_single_solution_board(random.randint(4, 6))
                        screen = constants.GAME
                        marked_board = [[0 for i in range(len(board))] for j in range(len(board))]
                    elif medium_button.pressed:
                        board = Board.create_single_solution_board(random.randint(7, 9))
                        screen = constants.GAME
                        marked_board = [[0 for i in range(len(board))] for j in range(len(board))]
                    elif hard_button.pressed:
                        board = Board.create_single_solution_board(random.randint(10, 12))
                        screen = constants.GAME
                        marked_board = [[0 for i in range(len(board))] for j in range(len(board))]
                elif screen == constants.END:
                    if restart_delay <= 0:
                        # Restart
                        screen = constants.HOME
                        board = None
                        marked_board = None
                        initial_type = None
                        invalid = False
                        found_capitals = 0
                        success = False
                        restart_delay = 0
                    else:
                        restart_delay -= 1
            
        # Handle updates
        
        if screen == constants.HOME:
            easy_button.update(*mouse_pos)
            medium_button.update(*mouse_pos)
            hard_button.update(*mouse_pos)
            
        elif screen == constants.GAME:
            square_size = BOARD_SIZE / len(board)
            highlight = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 100))
            invalid = False
            found_capitals = 0
            for row in range(len(board)):
                for column in range(len(board)):
                    x = square_size*column
                    y = square_size*row
                    pygame.draw.rect(board_surf, palette.board_colors[board[row][column] - 1],
                                     (x, y, square_size, square_size))
                    if success or (0 < mouse_pos[0] - x - (WIDTH - BOARD_SIZE) / 2 < square_size and
                                   0 < mouse_pos[1] - y - (HEIGHT - BOARD_SIZE) / 2 < square_size):
                        board_surf.blit(highlight, (x, y))
                    pygame.draw.rect(board_surf, palette.board_border,
                                     (x, y, square_size, square_size), 2)
                    
                    if marked_board[row][column] == 1:
                        pygame.draw.line(board_surf, palette.board_border,
                                         (x + square_size/6, y + square_size/6),
                                         (x + square_size*5/6, y + square_size*5/6), 10)
                        pygame.draw.line(board_surf, palette.board_border,
                                         (x + square_size*5/6, y + square_size/6),
                                         (x + square_size/6, y + square_size*5/6), 10)
                        
                    elif marked_board[row][column] == 2:
                        
                        color = palette.success if success else palette.board_border
                        found_capitals += 1
                        
                        # Vertical
                        for i in range(len(board)):
                            if i == row:
                                continue
                            if marked_board[i][column] == 2:
                                invalid = True
                                color = palette.invalid
                                found_capitals -= 1
                                break
                            
                        # Horizontal
                        for i in range(len(board)):
                            if i == column:
                                continue
                            if marked_board[row][i] == 2:
                                invalid = True
                                color = palette.invalid
                                found_capitals -= 1
                                break
                            
                        # Surrounding
                        for r in [-1, 1]:
                            if row + r not in range(len(board)):
                                continue
                            for c in [-1, 1]:
                                if column + c not in range(len(board)):
                                    continue
                                if marked_board[row + r][column + c] == 2:
                                    invalid = True
                                    color = palette.invalid
                                    found_capitals -= 1
                                    break
                            else:
                                continue
                            break
                            
                        # City
                        for r in range(len(board)):
                            if r == row:
                                continue
                            for c in range(len(board)):
                                if c == column:
                                    continue
                                if marked_board[r][c] == 2 and board[r][c] == board[row][column]:
                                    invalid = True
                                    color = palette.invalid
                                    found_capitals -= 1
                                    break
                            else:
                                continue
                            break
                        
                        pygame.draw.rect(board_surf, color,
                                         (x + square_size/6, y + square_size/6, square_size*2/3, square_size*2/3), 10)

            
        
        # Handle drawing
        
        if screen == constants.HOME:
            win.fill(palette.background)
            pygame.draw.rect(win, palette.contrast, (250, 300, 500, 200), 0, 25)
            
            easy_button.draw(win)
            medium_button.draw(win)
            hard_button.draw(win)
            
        elif screen == constants.GAME:
            win.fill(palette.background)
            win.blit(board_surf, ((WIDTH - BOARD_SIZE) / 2, (HEIGHT - BOARD_SIZE) / 2))
            
            if success:
                screen = constants.END
                restart_delay = 2
            if not invalid and found_capitals == len(board):
                success = True
        
        # Refresh the screen
        
        pygame.display.update()
        clock.tick(FPS)
                

if __name__ == "__main__":
    init()