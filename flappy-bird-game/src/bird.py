import pygame
import math

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 1
        self.lift = -10
        self.velocity = 0

        # Load and process the bird image
        original_image = pygame.image.load("flappy-bird-game/src/assets/images/erkan.jpg").convert()
        
        # Make the green background transparent
        original_image.set_colorkey((0, 255, 0))  # Green color key
        
        # Create a circular surface with transparency
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        
        # Scale the original image
        scaled_image = pygame.transform.scale(original_image, (40, 40))
        
        # Create a circular mask
        mask_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(mask_surface, (255, 255, 255), (20, 20), 20)
        
        # Apply the scaled image and mask
        self.image.blit(scaled_image, (0, 0))
        self.image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def move(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self, screen):
        screen.blit(self.image, (self.x - 20, self.y - 20))  # Merkezi doğru konumlandırmak için -20

    def flap(self):
        self.velocity = self.lift