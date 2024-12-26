import pygame
import random

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 80
        
        # Rastgele yükseklik ve boşluk ayarları
        self.min_height = 100  # Minimum boru yüksekliği
        self.max_height = 400  # Maximum boru yüksekliği
        self.min_gap = 150     # Minimum boşluk
        self.max_gap = 250     # Maximum boşluk
        
        # Rastgele değerleri ayarla
        self.height = random.randint(self.min_height, self.max_height)
        self.gap = random.randint(self.min_gap, self.max_gap)
        self.velocity = 5

    def move(self):
        self.x -= self.velocity

    def draw(self, screen):
        # Üst boru
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.height))
        # Alt boru
        bottom_pipe_height = 800 - (self.height + self.gap)  # 800 ekran yüksekliği
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.height + self.gap, self.width, bottom_pipe_height))

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x - 20, bird.y - 20, 40, 40)
        top_pipe = pygame.Rect(self.x, 0, self.width, self.height)
        bottom_pipe = pygame.Rect(self.x, self.height + self.gap, self.width, 800 - (self.height + self.gap))
        
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)

    def off_screen(self):
        return self.x < -self.width