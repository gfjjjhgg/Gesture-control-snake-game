import pygame
from pygame.locals import *

class Sq(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 0, 0))

pygame.init()  # Init Pygame
win = pygame.display.set_mode((800, 600)) # Game window 800x600

# Create 4 squares
s1, s2, s3, s4 = Sq(), Sq(), Sq(), Sq()

# Game loop
run = True
while run:
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_BACKSPACE):
            run = False

    # Draw squares in corners
    win.blit(s1.surf, (40, 40))
    win.blit(s2.surf, (40, 530))
    win.blit(s3.surf, (730, 40))
    win.blit(s4.surf, (730, 530))

    pygame.display.flip()