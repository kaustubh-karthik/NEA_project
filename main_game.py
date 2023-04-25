import pygame
from enum import Enum, auto
import random
import numpy as np
import simpleaudio as sa
import queue
from dataclasses import dataclass


wav_file_name = "immortals"

def run():
    # Setup
    pygame.init()
    clock = pygame.time.Clock()

    # Main Window setup
    screen_width = 1024
    screen_height = 1024
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption('NEA Rhythm Game')

    # Initialising lanes
    lanes = 6
    lane_size = screen_width//lanes
    
    @dataclass
    class Lane:
        x: int
        queue: queue.Queue
        key: int

    # Main class
    class Note(pygame.sprite.Sprite):

        # Initialising class variables
        note_group = pygame.sprite.Group() # Contains all the note objects

        note_keys = [pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k, pygame.K_l]
        lane_tracker = [Lane(lane_size*num_lanes, queue.Queue(), key) for num_lanes, key in zip(range(lanes), note_keys)]
        
        
        # Note calculations
        note_width = lane_size
        note_height = screen_height//10
        
        # Generating list of times for notes to spawn from a txt file
        note_times = np.genfromtxt("turning_points.txt", delimiter = ", ")
        bg_image = pygame.image.load("bg_images/notes_falling.jpg") # Loading bg image

        def __init__(self) -> None:
            # Call to super class to initialise this Note instance as a pygame sprite instance
            super().__init__()
            
            # Initialising lane
            self.lane = Note.get_random_lane()
            
            # Overriding super() class variables
            # Base rect
            self.rect = pygame.Rect(self.lane.x, 0, Note.note_width, Note.note_height)
            
            # Surface to draw rect on
            self.image = pygame.Surface((Note.note_width, Note.note_height))
            self.image.fill((255, 255, 255)) # Adding color to image(white)
            
            self.add_to_group() # Adding to sprite group
            self.add_to_queue() # Adding to queue
        
        # Randomly selects an array value
        def get_random_lane() -> Lane:
            return random.choice(Note.lane_tracker)
        
        # Adds to group
        def add_to_group(self):
            Note.note_group.add(self)
        
        # Adds to queue
        def add_to_queue(self):
            self.lane.queue.put(self)
        
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
            if clock_time in (Note.note_times*1000).astype(int):
                Note.generate_notes(1)
                print(clock_time)
                
        def kill_note_pressed():
            for lane in Note.lane_tracker:
                    if event.key == lane.key:
                        if not lane.queue.empty():
                            lane.queue.get().kill()
                            


        # Makes every note in the sprite group move down at a consistant speed    
        def note_movement():
            speed = 1        

            # Iterates through the sprite group and adds a fixed speed to their y value
            for sprite in Note.note_group.sprites():
                sprite.rect.y += speed
                
                if sprite.rect.y > screen_height:
                    sprite.kill()
                    sprite.lane.queue.get()
            
            Note.note_group.update() # Updates all sprites in group
        
        # Blits the background image onto the screen at coords (0,0) - top left
        def render_background():
            screen.blit(Note.bg_image, (0, 0))


    # Starting playback of song
    wave_obj = sa.WaveObject.from_wave_file(f"wav_files/{wav_file_name}.wav")
    wave_obj.play()


    '''---------------Main game loop------------------'''
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                Note.kill_note_pressed()

        clock.tick(1000) # Starting game timer
        Note.render_background()
        Note.generate_timed_notes(pygame.time.get_ticks())
        Note.note_movement()
        Note.draw_notes()
        pygame.display.update()

if __name__ == "__main__":
  run()

    