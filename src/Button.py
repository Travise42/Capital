
import pygame

import src.Palette as palette

class Button:
    
    text: str
    x_pos: int
    y_pos: int
    
    surf: pygame.Surface
    
    font: pygame.font.Font
    hovered: bool
    
    def __init__(self, text: str, x_pos: int, y_pos: int, width: int, height: int) -> None:
        """ Create a new button that draws on its own surface. Draw it on another surface using 'draw'.
        Drawing will blit this button's surface at ('x_pos', 'y_pos') with width and height: 'width' and 'height'.
        'text' will appear centered on the button with size 30 monospaced font.
        """
        
        self.text = text
        self.x_pos, self.y_pos = x_pos, y_pos
        
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        
        self.font = pygame.font.SysFont("monospaced", 30)
        self.hovered = False
        
    def update(self, mouse_x: int, mouse_y: int) -> None:
        """ Update this button's state to interact with the 
        mouse based on its x, 'mouse_x'; and y, 'mouse_y'.
        """
        
        # Update button states
        self.hovered = (0 < mouse_x - self.x_pos < self.get_width() and
                        0 < mouse_y - self.y_pos < self.get_height())
        self.pressed = self.hovered and pygame.mouse.get_pressed()[0]
        
        # Update background
        color = (palette.pressed_button if self.pressed else
                 palette.hovered_button if self.hovered else
                 palette.button)
        
        pygame.draw.rect(self.surf, color, (0, 0, self.get_width(), self.get_height()), 0, 25)
        
        # Update text
        text = self.font.render(self.text, True, palette.text)
        self.surf.blit(text, ((self.get_width() - text.get_width()) / 2,
                              (self.get_height() - text.get_height()) / 2))
    
    
    def draw(self, win: pygame.Surface) -> None:
        """ Draw this button's surface at its position on 'win'.
        """
        
        win.blit(self.surf, (self.x_pos, self.y_pos))
    
    
    def get_width(self) -> int:
        """ Returns the width of the surface button uses.
        """
        
        return self.surf.get_width()
    
    
    def get_height(self) -> int:
        """ Returns the height of the surface button uses.
        """
        
        return self.surf.get_height()
        