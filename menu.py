import pygame

from constants import *

class Button:

    def __init__(self, x, y, text, callback):
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text = text.upper()
        self.callback = callback

    def draw(self, screen, font):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        text_surf = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surf, (self.rect.x + (BUTTON_WIDTH // 3), self.rect.y + (BUTTON_HEIGHT // 3.6)))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            print(self.text)
            self.callback()
