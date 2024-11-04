import json
import pygame

import random

import src.Board as Board

import src.Palette as palette
import src.Constants as constants
from src.Button import Button


class Capital:
    
    WIDTH, HEIGHT = 1000, 800
    BOARD_SIZE = 600
    FPS = 60

    def __init__(self):
        # Create window
        
        pygame.init()
        
        self.win = pygame.display.set_mode((Capital.WIDTH, Capital.HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Create buttons
        
        self.easy_button = Button("Easy", 300, 350, 100, 100)
        self.medium_button = Button("Medium", 450, 350, 100, 100)
        self.hard_button = Button("Hard", 600, 350, 100, 100)
        self.custom_button = Button("Custom", 400, 550, 200, 50)
        
        # Initialize variables
        
        self.board_surf = pygame.Surface((Capital.BOARD_SIZE, Capital.BOARD_SIZE))
        self.board = None
        self.marked_board = None
        self.initial_type = None
        self.valid = False
        self.found_capitals = 0
        self.success = False
        self.restart_delay = 0
        
        try:
            # Create custom-boards.json if it does not exist
            with open("data/custom-boards.json", "x") as file:
                json.dump([], file)
                self.custom_boards = []
        except FileExistsError:
            # If it does, import custom boards 
            try:
                with open("data/custom-boards.json", "r") as file:
                    self.custom_boards = json.load(file)
            except:
                self.custom_boards = []
            
        self.custom_buttons = []
        self.workshop_buttons = []
        self.workshop_save_button = Button("Save", Capital.WIDTH - 250, 350, 150, 50)
        
        self.workshop_city = 1
        self.workshop_solutions = 0
        
        self.screen = constants.HOME
        
        self.font = pygame.font.SysFont("monospaced", 80)
        
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
                
            elif self.screen == constants.CUSTOM:
                self.update_custom()
                
            elif self.screen == constants.WORKSHOP:
                self.update_workshop()

            # Handle drawing
            
            if self.screen == constants.HOME:
                self.draw_home_screen()
                
            elif self.screen == constants.GAME:
                self.draw_game_screen()
                
                self.handle_success()
                
            elif self.screen == constants.CUSTOM:
                self.draw_custom_screen()
                
            elif self.screen == constants.WORKSHOP:
                self.draw_workshop_screen()
            
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
                
            # Main menu
            
            elif event.type == pygame.KEYDOWN:
                self.screen = constants.HOME
                
            # Hover over spaces
            
            elif event.type == pygame.MOUSEMOTION:
                if self.screen == constants.GAME:
                    self.drag_crosses()
                    
                elif pygame.mouse.get_pressed()[0] and self.screen == constants.WORKSHOP:
                    self.interact_with_workshop()
                    self.workshop_solutions = Board.get_solutions(self.board)
            
            # Click spaces
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.screen == constants.GAME:
                    self.interact_with_the_board()
                    
                elif self.screen == constants.WORKSHOP:
                    self.interact_with_workshop()
                    self.workshop_solutions = Board.get_solutions(self.board)
            
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
                    elif self.custom_button.pressed:
                        self.create_custom_screen()
                        self.screen = constants.CUSTOM
                
                # Returning to the menu
                
                elif self.screen == constants.END:
                    self.restart()
                
                # Custom Screen
                
                elif self.screen == constants.CUSTOM:
                    if self.custom_buttons[0].pressed:
                        self.start_game(None, Board.create_board(5))
                        self.screen = constants.WORKSHOP
                        
                        self.create_workshop()
                        
                    for i in range(0, len(self.custom_boards)):
                        if self.custom_buttons[i + 1].pressed:
                            self.start_game(None, self.custom_boards[i])
                            
                elif self.screen == constants.WORKSHOP:
                    if self.workshop_save_button.pressed:
                        self.custom_boards += [self.board]
                        with open("data/custom-boards.json", 'w') as file:
                            json.dump(self.custom_boards, file)
                        self.screen = constants.CUSTOM
                        self.create_custom_screen()
                    
                    elif self.workshop_buttons[0].pressed and len(self.board) > 5:
                        self.board = [row[:-1] for row in self.board[:-1]]
                        self.create_workshop()
                        
                    elif self.workshop_buttons[-1].pressed and len(self.board) < 15:
                        self.board = [row + [0] for row in (self.board + [[0 for row in self.board]])]
                        self.create_workshop()
                        
                    else:
                        for i in range(1, len(self.board) + 1):
                            if self.workshop_buttons[i].pressed:
                                self.workshop_city = i
                                
                    self.workshop_solutions = Board.get_solutions(self.board)
                        

    def update_buttons(self) -> None:
        """ Update the state of all the buttons.
        """
        
        self.easy_button.update(*self.mouse_pos)
        self.medium_button.update(*self.mouse_pos)
        self.hard_button.update(*self.mouse_pos)
        self.custom_button.update(*self.mouse_pos)


    def start_game(self, board_size: int = None, board: list[list[int]] = None) -> None:
        """ Create a new board and change the screen to constants.GAME.
        """
        
        self.board_surf = pygame.Surface((Capital.BOARD_SIZE, Capital.BOARD_SIZE))
        
        if board_size != None:
            # Create new board
            self.board = Board.create_single_solution_board(board_size)
        else:
            self.board = board
            
        self.screen = constants.GAME
        self.marked_board = [[0 for i in range(len(self.board))] for j in range(len(self.board))]
        
        # Create variables and surfaces
        
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
                
                # Swap X's with Empty spaces and vise versa
                
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
                
                # Break loop since only one square can be hovered
                
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
                
                # Draw square
                
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
                
                self.draw_space_elements(column, row)


    def draw_space_elements(self, column: int, row: int) -> None:
        """ Draw X's and Capital Squares within the board 'column' and 'row'.
        """
                
        x = self.square_size*column
        y = self.square_size*row
        
        # Draw X
        
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
        
        # Draw Capital and validate capital
        
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
        
        # Vertical: No capitals can be in the same column.
        
        for i in range(len(self.board)):
            if i == row:
                continue
            if self.marked_board[i][column] == 2:
                return False
            
        # Horizontal: No capitals can be in the same row.
        
        for i in range(len(self.board)):
            if i == column:
                continue
            if self.marked_board[row][i] == 2:
                return False
            
        # Surrounding: No capitals can be touching.
        
        for r in [-1, 1]:
            if not (0 <= row + r < len(self.board)):
                continue
            for c in [-1, 1]:
                if not (0 <= column + c < len(self.board)):
                    continue
                if self.marked_board[row + r][column + c] == 2:
                    return False
            
        # City: No other capital can be in the same city (color)
        
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
        
        
    def handle_success(self) -> None:
        """ Go to end screen if game is over.
        """
        
        # Allow for a second frame to pass before changing screen
            
        if self.success:
            self.screen = constants.END
            self.restart_delay = 1
            
        # End game if the board is filled and the capitals are in the right place
            
        if self.valid and self.found_capitals == len(self.board):
            self.success = True
            
            
    def draw_workshop_board(self):
        
        square_size = Capital.BOARD_SIZE / 2 / len(self.board)
        
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                
                x = square_size*column
                y = square_size*row
                
                # Draw square
                
                pygame.draw.rect(self.board_surf, palette.board_colors[self.board[row][column] - 1],
                                (x, y, square_size + 1, square_size + 1))
                
                boardx = (Capital.WIDTH - Capital.BOARD_SIZE/2) / 2
                boardy = (Capital.HEIGHT - Capital.BOARD_SIZE/2) / 3
                
                OVER_SPACE = (0 < self.mouse_pos[0] - boardx - x < square_size and
                              0 < self.mouse_pos[1] - boardy - y < square_size)
                
                # Highlight if hovered
                
                if OVER_SPACE or self.success:
                    self.board_surf.blit(self.highlight, (x, y))
                
                # Draw border
                
                pygame.draw.rect(self.board_surf, palette.board_border,
                                (x, y, self.square_size + 1, self.square_size + 1), 2)
        
        
    def draw_home_screen(self) -> None:
        """ Draw background and buttons.
        """
        
        self.win.fill(palette.background)
        pygame.draw.rect(self.win, palette.contrast, (250, 300, 500, 200), 0, 25)
        
        self.easy_button.draw(self.win)
        self.medium_button.draw(self.win)
        self.hard_button.draw(self.win)
        self.custom_button.draw(self.win)
        
    
    def draw_game_screen(self) -> None:
        """ Draw background and board.
        """
        
        self.win.fill(palette.background)
        self.win.blit(self.board_surf, ((Capital.WIDTH - Capital.BOARD_SIZE) / 2,
                                        (Capital.HEIGHT - Capital.BOARD_SIZE) / 2))
        
        
    def create_custom_screen(self) -> None:
        marginx = self.WIDTH / 10
        marginy = self.HEIGHT / 10
        
        button_size = 100
        pad = button_size / 2
        
        self.custom_buttons.clear()
        
        self.custom_buttons.append(Button("+", marginx + pad, marginy + pad, button_size, button_size))
        
        column = 1
        row = 0
        for _ in self.custom_boards:
            self.custom_buttons.append(Button("", marginx + (button_size + pad)*column + pad,
                                              marginy + (button_size + pad)*row + pad, button_size, button_size))
            
            column += 1
            if column > 5 or (row == 0 and column > 4):
                column = 0
                row += 1
                
                
    def create_workshop(self) -> None:
        self.board_surf = pygame.Surface((Capital.BOARD_SIZE/2, Capital.BOARD_SIZE/2))
        
        marginx = self.WIDTH / 4
        marginy = self.HEIGHT * 3/4
        dist = self.WIDTH / 2 / len(self.board)
        button_size = dist * 7/8
        
        self.workshop_buttons.clear()
                        
        for i in range(len(self.board)):
            self.workshop_buttons.append(Button(str(i + 1), marginx + dist*i, marginy, button_size, 100))
            
        self.workshop_buttons.insert(0, Button("-", marginx + button_size - dist - 100, marginy, 100, 100))
        self.workshop_buttons.append(Button("+", marginx + dist*len(self.board), marginy, 100, 100))
    
    def interact_with_workshop(self) -> None:
        square_size = Capital.BOARD_SIZE / 2 / len(self.board)
        
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                
                x = square_size*column
                y = square_size*row
                
                boardx = (Capital.WIDTH - Capital.BOARD_SIZE/2) / 2
                boardy = (Capital.HEIGHT - Capital.BOARD_SIZE/2) / 3
                
                OVER_SPACE = (0 < self.mouse_pos[0] - boardx - x < square_size and
                              0 < self.mouse_pos[1] - boardy - y < square_size)
                
                if OVER_SPACE:
                    self.board[row][column] = self.workshop_city
                    return
                    
    
    
    def update_custom(self) -> None:
        for custom_button in self.custom_buttons:
            custom_button.update(*self.mouse_pos)
    

    def update_workshop(self) -> None:
        for workshop_button in self.workshop_buttons:
            workshop_button.update(*self.mouse_pos)
        
        self.workshop_save_button.update(*self.mouse_pos)
        
        self.draw_workshop_board()


    def draw_custom_screen(self) -> None:
        marginx = self.WIDTH / 10
        marginy = self.HEIGHT / 10
        
        self.win.fill(palette.background)
        pygame.draw.rect(self.win, palette.contrast, (marginx, marginy, self.WIDTH - 2*marginx, self.HEIGHT - 2*marginy), 0, 25)
        
        # Draw add new custom board button
        self.custom_buttons[0].draw(self.win)
        for i, custom_button in enumerate(self.custom_buttons[1:]):
            # Draw button
            custom_button.draw(self.win)
            # Draw preview
            board_size = len(self.custom_boards[i])
            for row in range(board_size):
                for column in range(board_size):
                    pygame.draw.rect(self.win, palette.board_colors[self.custom_boards[i][row][column] - 1], (
                        custom_button.x_pos + (column + 1) * custom_button.surf.get_width()/(board_size + 2),
                        custom_button.y_pos + (row + 1) * custom_button.surf.get_height()/(board_size + 2),
                        custom_button.surf.get_width()/(board_size + 2) + 1,
                        custom_button.surf.get_height()/(board_size + 2) + 1))
    

    def draw_workshop_screen(self) -> None:
        marginx = self.WIDTH / 4 - self.WIDTH / 2 / 10 * 7/8 - 100
        marginy = self.HEIGHT * 3/4 - 50
        
        self.win.fill(palette.background)
        pygame.draw.rect(self.win, palette.contrast, (marginx, marginy, self.WIDTH - 2*marginx, 200), 0, 25)
        for workshop_button in self.workshop_buttons:
            workshop_button.draw(self.win)
            
        self.workshop_save_button.draw(self.win)
        
        self.win.blit(self.board_surf, ((Capital.WIDTH - Capital.BOARD_SIZE/2) / 2,
                                        (Capital.HEIGHT - Capital.BOARD_SIZE/2) / 3))
        
        solutions = self.font.render(str(self.workshop_solutions), True, '#ffffff')
        self.win.blit(solutions, (Capital.WIDTH - 200, 250))
                

if __name__ == "__main__":
    Capital().loop()
