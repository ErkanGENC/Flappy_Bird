# File: /flappy-bird-game/flappy-bird-game/src/main.py

import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()