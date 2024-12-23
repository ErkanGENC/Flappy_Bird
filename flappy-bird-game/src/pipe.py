import pygame

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 80
        self.height = 500
        self.gap = 200
        self.velocity = 5

    def move(self):
        self.x -= self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.height + self.gap, self.width, self.height))

    def collide(self, bird):
        if bird.y < self.height or bird.y > self.height + self.gap:
            if bird.x > self.x and bird.x < self.x + self.width:
                return True
        return False

    def off_screen(self):
        return self.x < -self.width