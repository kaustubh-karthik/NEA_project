import pygame
from enum import IntEnum
from random import randint
import numpy as np
import simpleaudio as sa


# Setup
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 1024
screen_height = 1024
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('NEA Rhythm Game')

# Initialising lanes
lanes = 5
lane_size = screen_width//lanes

# Enum to store the x positions of lanes
class SpawnPos(IntEnum):
    ln0 = 0
    ln1 = lane_size
    ln2 = lane_size*2
    ln3 = lane_size*3
    ln4 = lane_size*4

# Main class
class Note(pygame.sprite.Sprite):

    # Initialising class variables
    note_group = pygame.sprite.Group() # Contains all the note objects
    # Array of spawn positions allows me to randomly select a spawn position
    spawn_positions = [SpawnPos.ln0, SpawnPos.ln1, SpawnPos.ln2, SpawnPos.ln3, SpawnPos.ln4]
    
    # Note calculations
    note_width = lane_size
    note_height = screen_height//10
    
    # Generating list of times for notes to spawn from a txt file
    note_times = np.genfromtxt("turning_points.txt", delimiter = ", ")
    bg_image = pygame.image.load("notes_falling.jpg") # Loading bg image

    def __init__(self) -> None:
        # Call to super class to initialise this Note instance as a pygame sprite instance
        super().__init__()
        
        # Overriding super() class variables
        random_spawn = Note.get_random_spawn()
        # Base rect
        self.rect = pygame.Rect(random_spawn, 0, Note.note_width, Note.note_height)
        
        # Surface to draw rect on
        self.image = pygame.Surface((Note.note_width, Note.note_height))
        self.image.fill((255, 255, 255)) # Adding color to image(white)
        Note.add_to_group(self) # Adding to sprite group
    
    # Randomly selects an array value
    def get_random_spawn() -> SpawnPos:
        return Note.spawn_positions[randint(0, 4)]
    
    # Adds to group
    def add_to_group(note_rect):
        Note.note_group.add(note_rect)
    
    # Draws notes to the screen
    def draw_notes():
        Note.note_group.draw(screen)
    
    # Generates any number of notes at random positions
    def generate_notes(num_notes):
        for _ in range(num_notes):
            Note()

    # Generates a note at the correct point(needs to be called in main game loop)        
    def generate_timed_notes(clock_time):
        # Checks if the game time(ms) is equal to any time in the note_times array
        if clock_time in Note.note_times*1000:
            Note.generate_notes(1)

    # Makes every note in the sprite group move down at a consistant speed    
    def note_movement():
        speed = 1        

        # Iterates through the sprite group and adds a fixed speed to their y value
        for sprite in Note.note_group.sprites():
            sprite.rect.y += speed
        Note.note_group.update() # Updates all sprites in group
    
    # Blits the background image onto the screen at coords (0,0) - top left
    def render_background():
        screen.blit(Note.bg_image, (0, 0))
        
# Starting playback of song
wave_obj = sa.WaveObject.from_wave_file("pasoori.wav")
wave_obj.play()


'''---------------Main game loop------------------'''
while True:
    clock.tick() # Starting game timer
    Note.render_background()
    Note.generate_timed_notes(pygame.time.get_ticks())
    Note.note_movement()
    Note.draw_notes()
    pygame.display.update()

    