import pygame

class Base:
    def __init__(self, y):
        self.y = y
        self.width = 500
        self.height = 100
        self.velocity = 5
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), (self.x1, self.y, self.width, self.height))
        pygame.draw.rect(screen, (139, 69, 19), (self.x2, self.y, self.width, self.height))