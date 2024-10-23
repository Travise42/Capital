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
        # Create window
        
        pygame.init()
        
        self.win = pygame.display.set_mode((Capital.WIDTH, Capital.HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Create buttons
        
        self.easy_button = Button("Easy", 300, 350, 100, 100)
        self.medium_button = Button("Medium", 450, 350, 100, 100)
        self.hard_button = Button("Hard", 600, 350, 100, 100)
        
        # Initialize variables
        
        self.board_surf = pygame.Surface((Capital.BOARD_SIZE, Capital.BOARD_SIZE))
        self.board = None
        self.marked_board = None
        self.initial_type = None
        self.valid = False
        self.found_capitals = 0
        self.success = False
        self.restart_delay = 0
        
        self.screen = constants.HOME
        
    def loop(self) -> None:
        """ Main loop for Capital.
        """
        
        self.running = True
        while self.running:
            
            self.handle_events()
                
            # Handle updates
            
            if self.screen == constants.HOME:
                self.update_buttons()
                
            elif self.screen == constants.GAME:
                self.update_game()

            # Handle drawing
            
            if self.screen == constants.HOME:
                self.draw_home_screen()
                
            elif self.screen == constants.GAME:
                self.draw_game_screen()
                
                self.handle_success()
            
            # Refresh the screen
            
            pygame.display.update()
            self.clock.tick(Capital.FPS)
        
    def handle_events(self) -> None:
        """ Handle mouse interactions.
        """
        
        self.mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            
            # Exit the application
            if event.type == pygame.QUIT:
                self.running = False
                
            # Hover over spaces
            elif event.type == pygame.MOUSEMOTION:
                if self.screen == constants.GAME:
                    self.drag_crosses()
            
            # Click spaces
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.screen == constants.GAME:
                    self.interact_with_the_board()
            
            # Click buttons
            elif event.type == pygame.MOUSEBUTTONUP:
                self.initial_type = None
                
                # Starting a new game
                if self.screen == constants.HOME:
                    if self.easy_button.pressed:
                        self.start_game(random.randint(4, 6))
                    elif self.medium_button.pressed:
                        self.start_game(random.randint(7, 9))
                    elif self.hard_button.pressed:
                        self.start_game(random.randint(10, 12))
                
                # Returning to the menu
                elif self.screen == constants.END:
                    self.restart()


    def update_buttons(self) -> None:
        """ Update the state of all the buttons.
        """
        
        self.easy_button.update(*self.mouse_pos)
        self.medium_button.update(*self.mouse_pos)
        self.hard_button.update(*self.mouse_pos)


    def start_game(self, board_size: int) -> None:
        """ Create a new board and change the screen to constants.GAME.
        """
        
        self.board = Board.create_single_solution_board(board_size)
        self.screen = constants.GAME
        self.marked_board = [[0 for i in range(len(self.board))] for j in range(len(self.board))]
        
        self.square_size = Capital.BOARD_SIZE / len(self.board)
        self.highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        self.highlight.fill((255, 255, 255, 100))


    def drag_crosses(self) -> None:
        """ Change the state of all spaces dragged over to the opposite of the inital space's state.
        """
        
        # Must have started right clicking over the board
        if self.initial_type == None or not pygame.mouse.get_pressed()[2]:
            return
        
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                
                # Only alter spaces with the same state as the one initially clicked
                if self.marked_board[row][column] != self.initial_type:
                    continue
                
                x = self.square_size*column + self.get_board_x()
                y = self.square_size*row + self.get_board_y()
                
                OVER_SPACE = (0 < self.mouse_pos[0] - x < self.square_size and
                              0 < self.mouse_pos[1] - y < self.square_size)
                
                if OVER_SPACE:
                    self.marked_board[row][column] = 1 - self.initial_type


    def interact_with_the_board(self) -> None:
        """ Handle placing capitals and crosses over spaces.
        """
        
        self.initial_type = None
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                
                x = self.square_size*column + self.get_board_x()
                y = self.square_size*row + self.get_board_y()
                
                OVER_SPACE = (0 < self.mouse_pos[0] - x < self.square_size and
                              0 < self.mouse_pos[1] - y < self.square_size)
                
                if not OVER_SPACE:
                    continue
                
                # Left click: Add / remove capital
                if pygame.mouse.get_pressed()[0]:
                    self.marked_board[row][column] = 2 - self.marked_board[row][column]
                    continue
                
                # Right click: Add / remove X
                if pygame.mouse.get_pressed()[2]:
                    if self.marked_board[row][column] == 2:
                        return
                    self.initial_type = self.marked_board[row][column]
                    self.marked_board[row][column] = 1 - self.initial_type
                
                return
            
                    
    def get_board_x(self) -> int:
        """ Return the distance the board is from the left of the screen.
        """
        
        return (Capital.WIDTH - Capital.BOARD_SIZE) / 2
                    
                    
    def get_board_y(self) -> int:
        """ Return the distance the board is from the top of the screen.
        """
        
        return (Capital.HEIGHT - Capital.BOARD_SIZE) / 2
                    
                    
    def update_game(self) -> None:
        """ Draw all game elements on 'board_surf'.
        """
        
        self.valid = False
        self.found_capitals = 0
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                
                x = self.square_size*column
                y = self.square_size*row
                
                # Draw space
                pygame.draw.rect(self.board_surf, palette.board_colors[self.board[row][column] - 1],
                                (x, y, self.square_size, self.square_size))
                
                OVER_SPACE = (0 < self.mouse_pos[0] - self.get_board_x() - x < self.square_size and
                              0 < self.mouse_pos[1] - self.get_board_y() - y < self.square_size)
                
                # Highlight if hovered
                if OVER_SPACE or self.success:
                    self.board_surf.blit(self.highlight, (x, y))
                
                # Draw border
                pygame.draw.rect(self.board_surf, palette.board_border,
                                (x, y, self.square_size + 1, self.square_size + 1), 2)
                
                self.draw_space_elements(column, row, x, y)


    def draw_space_elements(self, column: int, row: int, x: int, y: int) -> None:
        if self.marked_board[row][column] == 1:
            pygame.draw.line(self.board_surf, palette.board_border,
                            (x + self.square_size/6, y + self.square_size/6),
                            (x + self.square_size*5/6, y + self.square_size*5/6), 10)
            pygame.draw.line(self.board_surf, palette.board_border,
                            (x + self.square_size*5/6, y + self.square_size/6),
                            (x + self.square_size/6, y + self.square_size*5/6), 10)
            return
            
        if self.marked_board[row][column] != 2:
            return
        
        if self.validate_space(column, row):
            self.valid = True
            color = palette.success if self.success else palette.board_border
            self.found_capitals += 1
        else:
            color = palette.invalid
        
        pygame.draw.rect(self.board_surf, color,
                         (x + self.square_size/6, y + self.square_size/6,
                          self.square_size*2/3, self.square_size*2/3), 10)


    def validate_space(self, column: int, row: int) -> bool:
        """ Return True if no other capitals interfere with the
        capital on column and row: 'column' and 'row'.
        """
        
        # Vertical
        for i in range(len(self.board)):
            if i == row:
                continue
            if self.marked_board[i][column] == 2:
                return False
            
        # Horizontal
        for i in range(len(self.board)):
            if i == column:
                continue
            if self.marked_board[row][i] == 2:
                return False
            
        # Surrounding
        for r in [-1, 1]:
            if not (0 <= row + r < len(self.board)):
                continue
            for c in [-1, 1]:
                if not (0 <= column + c < len(self.board)):
                    continue
                if self.marked_board[row + r][column + c] == 2:
                    return False
            
        # City
        for r in range(len(self.board)):
            if r == row:
                continue
            for c in range(len(self.board)):
                if c == column:
                    continue
                if (self.marked_board[r][c] == 2 and
                    self.board[r][c] == self.board[row][column]):
                    return False
                
        return True


    def restart(self) -> None:
        """ Reset variables to initial values is delay is over.
        """
        
        if self.restart_delay > 0:
            self.restart_delay -= 1
            return
        
        self.screen = constants.HOME
        self.board = None
        self.marked_board = None
        self.initial_type = None
        self.valid = False
        self.found_capitals = 0
        self.success = False
        self.restart_delay = 0
        
        
    def draw_home_screen(self) -> None:
        """ Draw background and buttons.
        """
        
        self.win.fill(palette.background)
        pygame.draw.rect(self.win, palette.contrast, (250, 300, 500, 200), 0, 25)
        
        self.easy_button.draw(self.win)
        self.medium_button.draw(self.win)
        self.hard_button.draw(self.win)
        
    
    def draw_game_screen(self) -> None:
        """ Draw background and board.
        """
        
        self.win.fill(palette.background)
        self.win.blit(self.board_surf, ((Capital.WIDTH - Capital.BOARD_SIZE) / 2, (Capital.HEIGHT - Capital.BOARD_SIZE) / 2))
        
        
    def handle_success(self) -> None:
        """ Go to end screen if game is over.
        """
        
        if self.success:
            self.screen = constants.END
            self.restart_delay = 1
        if self.valid and self.found_capitals == len(self.board):
            self.success = True
                

if __name__ == "__main__":
    Capital().loop()