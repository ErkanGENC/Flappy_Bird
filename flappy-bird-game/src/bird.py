import pygame
import math

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 1
        self.lift = -10
        self.velocity = 0
        self.angle = 0
        self.max_angle = 30

        # Load and process the bird image
        original_image = pygame.image.load("flappy-bird-game/src/assets/images/erkan.jpg").convert()
        
        # Make the green background transparent
        original_image.set_colorkey((0, 255, 0))
        
        # Create a circular surface with transparency
        self.original_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        
        # Scale the original image
        scaled_image = pygame.transform.scale(original_image, (40, 40))
        
        # Create a circular mask
        mask_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(mask_surface, (255, 255, 255), (20, 20), 20)
        
        # Apply the scaled image and mask
        self.original_image.blit(scaled_image, (0, 0))
        self.original_image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        self.image = self.original_image

    def move(self):
        self.velocity += self.gravity
        self.y += self.velocity
        
        # Açıyı hesapla
        if self.velocity < 0:  # Yukarı çıkarken
            self.angle = self.max_angle
        else:  # Aşağı inerken
            # Hıza bağlı olarak -90 dereceye kadar dön
            self.angle = max(-90, self.max_angle - self.velocity * 4)
        
        # Resmi döndür
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def draw(self, screen):
        # Döndürülmüş resmin merkezini ayarla
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)

    def flap(self):
        self.velocity = self.lift
        self.angle = self.max_angle