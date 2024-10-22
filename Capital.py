import pygame

import random

import src.Board as Board

import src.Palette as palette
import src.Constants as constants
from src.Button import Button


class Capital:
    WIDTH, HEIGHT = 1000, 800
    BOARD_SIZE = 600
    FPS = 30

    def __init__(self):
        
        pygame.init()
        
        self.win = pygame.display.set_mode((Capital.WIDTH, Capital.HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.easy_button = Button("Easy", 300, 350, 100, 100)
        self.medium_button = Button("Medium", 450, 350, 100, 100)
        self.hard_button = Button("Hard", 600, 350, 100, 100)
        
        self.board_surf = pygame.Surface((Capital.BOARD_SIZE, Capital.BOARD_SIZE))
        self.board = None
        self.marked_board = None
        self.initial_type = None
        self.invalid = False
        self.found_capitals = 0
        self.success = False
        self.restart_delay = 0
        
        self.screen = constants.HOME
        
    def loop(self) -> None:
        running = True
        while running:
            
            # Handle events
            
            self.mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                
                # Exit the application
                if event.type == pygame.QUIT:
                    running = False
                    
                # Hover over buttons
                elif event.type == pygame.MOUSEMOTION:
                    if self.screen == constants.GAME:
                        if self.initial_type == None or not pygame.mouse.get_pressed()[2]:
                            continue
                        for row in range(len(self.board)):
                            for column in range(len(self.board)):
                                if self.marked_board[row][column] != self.initial_type:
                                    continue
                                
                                if (0 < self.mouse_pos[0] - self.square_size*column - (Capital.WIDTH - Capital.BOARD_SIZE) / 2 < self.square_size and
                                    0 < self.mouse_pos[1] - self.square_size*row - (Capital.HEIGHT - Capital.BOARD_SIZE) / 2 < self.square_size):
                                    self.marked_board[row][column] = 1 - self.initial_type
                
                # Click spaces
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.screen == constants.GAME:
                        self.initial_type = None
                        for row in range(len(self.board)):
                            for column in range(len(self.board)):
                                x = self.square_size*column
                                y = self.square_size*row
                                if (0 < self.mouse_pos[0] - x - (Capital.WIDTH - Capital.BOARD_SIZE) / 2 < self.square_size and
                                    0 < self.mouse_pos[1] - y - (Capital.HEIGHT - Capital.BOARD_SIZE) / 2 < self.square_size):
                                    # Add / remove X
                                    if pygame.mouse.get_pressed()[2]:
                                        self.initial_type = self.marked_board[row][column]
                                        self.marked_board[row][column] = 1 - self.initial_type
                                    # Add / remove capital
                                    elif pygame.mouse.get_pressed()[0]:
                                        self.marked_board[row][column] = 2 - self.marked_board[row][column]
                
                # Click buttons
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.initial_type = None
                    if self.screen == constants.HOME:
                        if self.easy_button.pressed:
                            self.board = Board.create_single_solution_board(random.randint(4, 6))
                            self.screen = constants.GAME
                            self.marked_board = [[0 for i in range(len(self.board))] for j in range(len(self.board))]
                        elif self.medium_button.pressed:
                            self.board = Board.create_single_solution_board(random.randint(7, 9))
                            self.screen = constants.GAME
                            self.marked_board = [[0 for i in range(len(self.board))] for j in range(len(self.board))]
                        elif self.hard_button.pressed:
                            self.board = Board.create_single_solution_board(random.randint(10, 12))
                            self.screen = constants.GAME
                            self.marked_board = [[0 for i in range(len(self.board))] for j in range(len(self.board))]
                    elif self.screen == constants.END:
                        if self.restart_delay <= 0:
                            # Restart
                            self.screen = constants.HOME
                            self.board = None
                            self.marked_board = None
                            self.initial_type = None
                            self.invalid = False
                            self.found_capitals = 0
                            self.success = False
                            self.restart_delay = 0
                        else:
                            self.restart_delay -= 1
                
            # Handle updates
            
            if self.screen == constants.HOME:
                self.easy_button.update(*self.mouse_pos)
                self.medium_button.update(*self.mouse_pos)
                self.hard_button.update(*self.mouse_pos)
                
            elif self.screen == constants.GAME:
                #TODO
                self.square_size = Capital.BOARD_SIZE / len(self.board)
                self.highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                self.highlight.fill((255, 255, 255, 100))
                self.invalid = False
                self.found_capitals = 0
                for row in range(len(self.board)):
                    for column in range(len(self.board)):
                        x = self.square_size*column
                        y = self.square_size*row
                        pygame.draw.rect(self.board_surf, palette.board_colors[self.board[row][column] - 1],
                                        (x, y, self.square_size, self.square_size))
                        if self.success or (0 < self.mouse_pos[0] - x - (Capital.WIDTH - Capital.BOARD_SIZE) / 2 < self.square_size and
                                    0 < self.mouse_pos[1] - y - (Capital.HEIGHT - Capital.BOARD_SIZE) / 2 < self.square_size):
                            self.board_surf.blit(self.highlight, (x, y))
                        pygame.draw.rect(self.board_surf, palette.board_border,
                                        (x, y, self.square_size, self.square_size), 2)
                        
                        if self.marked_board[row][column] == 1:
                            pygame.draw.line(self.board_surf, palette.board_border,
                                            (x + self.square_size/6, y + self.square_size/6),
                                            (x + self.square_size*5/6, y + self.square_size*5/6), 10)
                            pygame.draw.line(self.board_surf, palette.board_border,
                                            (x + self.square_size*5/6, y + self.square_size/6),
                                            (x + self.square_size/6, y + self.square_size*5/6), 10)
                            
                        elif self.marked_board[row][column] == 2:
                            
                            color = palette.success if self.success else palette.board_border
                            self.found_capitals += 1
                            
                            # Vertical
                            for i in range(len(self.board)):
                                if i == row:
                                    continue
                                if self.marked_board[i][column] == 2:
                                    self.invalid = True
                                    color = palette.invalid
                                    self.found_capitals -= 1
                                    break
                                
                            # Horizontal
                            for i in range(len(self.board)):
                                if i == column:
                                    continue
                                if self.marked_board[row][i] == 2:
                                    self.invalid = True
                                    color = palette.invalid
                                    self.found_capitals -= 1
                                    break
                                
                            # Surrounding
                            for r in [-1, 1]:
                                if row + r not in range(len(self.board)):
                                    continue
                                for c in [-1, 1]:
                                    if column + c not in range(len(self.board)):
                                        continue
                                    if self.marked_board[row + r][column + c] == 2:
                                        self.invalid = True
                                        color = palette.invalid
                                        self.found_capitals -= 1
                                        break
                                else:
                                    continue
                                break
                                
                            # City
                            for r in range(len(self.board)):
                                if r == row:
                                    continue
                                for c in range(len(self.board)):
                                    if c == column:
                                        continue
                                    if self.marked_board[r][c] == 2 and self.board[r][c] == self.board[row][column]:
                                        self.invalid = True
                                        color = palette.invalid
                                        self.found_capitals -= 1
                                        break
                                else:
                                    continue
                                break
                            
                            pygame.draw.rect(self.board_surf, color,
                                            (x + self.square_size/6, y + self.square_size/6, self.square_size*2/3, self.square_size*2/3), 10)

            # Handle drawing
            
            if self.screen == constants.HOME:
                self.win.fill(palette.background)
                pygame.draw.rect(self.win, palette.contrast, (250, 300, 500, 200), 0, 25)
                
                self.easy_button.draw(self.win)
                self.medium_button.draw(self.win)
                self.hard_button.draw(self.win)
                
            elif self.screen == constants.GAME:
                self.win.fill(palette.background)
                self.win.blit(self.board_surf, ((Capital.WIDTH - Capital.BOARD_SIZE) / 2, (Capital.HEIGHT - Capital.BOARD_SIZE) / 2))
                
                if self.success:
                    self.screen = constants.END
                    self.restart_delay = 1
                if not self.invalid and self.found_capitals == len(self.board):
                    self.success = True
            
            # Refresh the screen
            
            pygame.display.update()
            self.clock.tick(Capital.FPS)
                

if __name__ == "__main__":
    Capital().loop()