import os
import pygame

# Initialize pygame's mixer for sound
pygame.mixer.init()

# Define the path to the assets directory
ASSETS_DIR = os.path.dirname(__file__)

# Load images
BIRD_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'bird.png'))  # Update this line with the new bird image path
PIPE_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'pipe.png'))
BASE_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'base.png'))
BACKGROUND_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'background.png'))
BACK_IMG= pygame.image.load(os.path.join(ASSETS_DIR,'back.jpeg'))

# Load sounds
FLAP_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'flap.wav'))
HIT_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'hit.wav'))
POINT_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'point.wav'))