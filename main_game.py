import pygame
from enum import IntEnum
from random import randint


# Setup
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('NEA Rhythm Game')

lanes = 5
lane_size = screen_width//lanes

class SpawnPos(IntEnum):
    ln0 = 0
    ln1 = lane_size
    ln2 = lane_size*2
    ln3 = lane_size*3
    ln4 = lane_size*4

class Note():
    
    spawn_positions = [SpawnPos.ln0, SpawnPos.ln1, SpawnPos.ln2, SpawnPos.ln3, SpawnPos.ln4]
    note_width = lane_size
    note_height = screen_height//10

    def __init__(self, x_pos: SpawnPos) -> None:
        random_spawn = Note.get_random_spawn()
        note_rect = pygame.Rect(random_spawn, 0, Note.note_width, Note.note_height)
    
    def get_random_spawn() -> SpawnPos:
        return Note.spawn_positions[randint(0, 4)]
    