import pygame
from bird import Bird
from pipe import Pipe
from base import Base

class Game:
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.bird = Bird(230, 350)
        self.base = Base(730)
        self.pipes = [Pipe(600)]
        self.run_game = True

    def run(self):
        while self.run_game:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.flap()

            self.bird.move()
            self.base.move()
            self._handle_pipes()
            self._draw()

    def _handle_pipes(self):
        for pipe in self.pipes:
            pipe.move()
            if pipe.collide(self.bird):
                self.run_game = False

            if pipe.off_screen():
                self.pipes.remove(pipe)
                self.pipes.append(Pipe(self.screen_width))

    def _draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.base.draw(self.screen)
        pygame.display.update()