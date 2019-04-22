import pygame
from lordlarkamarasi.textures import relative_load

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = relative_load('textures/entities/player.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = 800 / 2
        self.rect.bottom = 800 - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -1
        if keystate[pygame.K_RIGHT]:
            self.speedx = 1
            
        self.rect.x += self.speedx
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0
