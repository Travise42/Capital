
import pygame

import src.Palette as palette

class Button:
    
    text: str
    x_pos: int
    y_pos: int
    
    surf: pygame.Surface
    
    font: pygame.font.Font
    hovered: bool
    
    def __init__(self, text: str, x_pos: int, y_pos: int, width: int, height: int):
        self.text = text
        self.x_pos, self.y_pos = x_pos, y_pos
        
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        
        self.font = pygame.font.SysFont("monospaced", 30)
        self.hovered = False
        
    def update(self, mouse_x, mouse_y):
        self.hovered = 0 < mouse_x - self.x_pos < self.get_width() and 0 < mouse_y - self.y_pos < self.get_height()
        self.pressed = self.hovered and pygame.mouse.get_pressed()[0]
        
        color = palette.pressed_button if self.pressed else palette.hovered_button if self.hovered else palette.button
        
        pygame.draw.rect(self.surf, color, (0, 0, self.get_width(), self.get_height()), 0, 25)
        
        text = self.font.render(self.text, True, palette.pressed_text if self.pressed else palette.text)
        self.surf.blit(text, ((self.get_width() - text.get_width()) / 2, (self.get_height() - text.get_height()) / 2))
    
    def draw(self, win):
        win.blit(self.surf, (self.x_pos, self.y_pos))
    
    def get_width(self):
        return self.surf.get_width()
    
    def get_height(self):
        return self.surf.get_height()
        