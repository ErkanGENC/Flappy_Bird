import pygame

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 1
        self.lift = -15
        self.velocity = 0

    def move(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 20)

    def flap(self):
        self.velocity = self.lift