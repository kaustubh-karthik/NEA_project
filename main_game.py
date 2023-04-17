import pygame
from enum import IntEnum
from random import randint
import numpy as np


# Setup
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 1024
screen_height = 1024
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

class Note(pygame.sprite.Sprite):

    note_group = pygame.sprite.Group()
    spawn_positions = [SpawnPos.ln0, SpawnPos.ln1, SpawnPos.ln2, SpawnPos.ln3, SpawnPos.ln4]
    note_width = lane_size
    note_height = screen_height//10
    note_times = np.genfromtxt("turning_points.txt", delimiter = ", ")
    bg_image = pygame.image.load("notes_falling.jpg")
    print(note_times)
    

    def __init__(self) -> None:
        super().__init__()
        random_spawn = Note.get_random_spawn()
        self.rect = pygame.Rect(random_spawn, 0, Note.note_width, Note.note_height)
        self.image = pygame.Surface((Note.note_width, Note.note_height))
        self.image.fill((255, 255, 255))
        Note.add_to_group(self)
    
    def get_random_spawn() -> SpawnPos:
        return Note.spawn_positions[randint(0, 4)]
    
    def add_to_group(note_rect):
        Note.note_group.add(note_rect)
    
    def draw_notes():
        Note.note_group.draw(screen)
        
    def generate_notes(num_notes):
        for _ in range(num_notes):
            Note()
        print(Note.note_group.sprites())
        
    def generate_timed_notes(clock_time):
        if clock_time in Note.note_times*1000:
            Note.generate_notes(1)
            print(clock_time)
    
    def note_movement():
        for sprite in Note.note_group.sprites():
            sprite.rect.y += 1
        Note.note_group.update()
    
    def render_background():
        screen.blit(Note.bg_image, (0, 0))
        
while True:
    Note.render_background()
    Note.generate_timed_notes(pygame.time.get_ticks())
    Note.note_movement()
    Note.draw_notes()
    pygame.display.update()

    