import os
import pygame

# Initialize pygame's mixer for sound
pygame.mixer.init()

# Define the path to the assets directory
ASSETS_DIR = os.path.dirname(__file__)

# Load images
BIRD_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'images', 'bird.png'))
PIPE_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'pipe.png'))
BASE_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'base.png'))
BACKGROUND_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'background.png'))

# Load sounds
FLAP_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'flap.wav'))
HIT_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'hit.wav'))
POINT_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'point.wav'))