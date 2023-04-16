import pygame
from enum import IntEnum
from random import randint


# Setup
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
lanes = 5
lane_size = screen_width//lanes
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('NEA Rhythm Game')

class SpawnPos(IntEnum):
    ln0 = 0
    ln1 = lane_size
    ln2 = lane_size*2
    ln3 = lane_size*3
    ln4 = lane_size*4

spawn_positions = [SpawnPos.ln0, SpawnPos.ln1, SpawnPos.ln2, SpawnPos.ln3, SpawnPos.ln4]

class Note():
    def __init__(self, x_pos: SpawnPos) -> None:
        pygame.Rect()
    
    def get_random_spawn() -> SpawnPos:
        return spawn_positions[randint(0, 4)]
    