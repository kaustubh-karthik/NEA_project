import pygame, sys, random, queue
import numpy as np
import simpleaudio as sa
from dataclasses import dataclass
import cv2 as cv
import mediapipe as mp


wav_file_name = "message_bottle"

def run():
    # Setup
    pygame.init()
    clock = pygame.time.Clock()

    # Main Window setup
    screen_width = 1024
    screen_height = 1024
    screen = pygame.display.set_mode((screen_width,screen_height), vsync=1)
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
        # Initialising speed
        speed = 5

        # Initialising arrays to keep track of lanes and keys
        note_keys = [pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k, pygame.K_l]
        # Creates Lane instances for each lane
        lane_tracker = [Lane(lane_size*num_lanes, queue.Queue(), key) for num_lanes, key in zip(range(lanes), note_keys)]
        
        
        # Note calculations
        note_width = lane_size
        note_height = screen_height//10
        
        # Generating list of times for notes to spawn from a txt file
        note_times = (np.genfromtxt("turning_points.txt", delimiter = ", ")*1000).astype(int)
        
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
        def generate_timed_notes(clock):
            
            current_time = pygame.time.get_ticks() # Checks if any of the notes are inbetween this tick and the previous tick
            accepted_times = np.asarray(list(range(current_time - clock.get_time(), current_time))) # Creates an array of a range of times that the note can be in
            matched_elements = np.isin(Note.note_times, accepted_times) # Creates an array of booleans of whether an element matches another
            Note.generate_notes(np.count_nonzero(matched_elements)) # Generates the same number of notes as the matched elements
                 
                 
        def kill_note_pressed():
            # Iterates through each lane and checks if their key is being pressed
            # kills first note in corresponding queue if pressed
            for lane in Note.lane_tracker:
                if event.key == lane.key:
                    if not lane.queue.empty():
                        lane.queue.get().kill()
                        

        # Makes every note in the sprite group move down at a consistant speed    
        def note_movement():
            # Iterates through the sprite group and adds a fixed speed to their y value
            for sprite in Note.note_group.sprites():
                sprite.rect.y += Note.speed
                
                # Kills the note if it goes off screen
                if sprite.rect.y > screen_height:
                    sprite.kill()
                    sprite.lane.queue.get() # Removes killed reference from queue
            
            Note.note_group.update() # Updates all sprites in group

    class HandTracking:
        capture = cv.VideoCapture(0)

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        
        fixed_y = True
        fixed_y_coord = 800
        
        def get_hand_landmarks():
            success, img = HandTracking.capture.read()
            rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            rgb_img = cv.flip(rgb_img, 1)
            results = HandTracking.hands.process(rgb_img)

            return results.multi_hand_landmarks            
                        
    
        def landmark_iteration():
            hand_landmarks = HandTracking.get_hand_landmarks()

            if hand_landmarks:
                for hand in hand_landmarks:
                    index_finger = hand.landmark[8]
                    
                    for lm in hand.landmark:
                        centre_x = lm.x*screen_width
                        centre_y = lm.y*screen_height
                        
                        if HandTracking.fixed_y:
                            y_offset = index_finger.y*screen_height - HandTracking.fixed_y_coord
                            centre_y -= y_offset
                            
                        pygame.draw.circle(screen, (255, 0, 255), (centre_x, centre_y), 5)
                        
                    
                    HandTracking.hand_collision(index_finger)

            
            

        def hand_collision(index_finger):
            for note in Note.note_group.sprites():#
                index_x, index_y = index_finger.x*screen_width, index_finger.y*screen_height
                
                if HandTracking.fixed_y and note.rect.collidepoint((index_x, HandTracking.fixed_y_coord)):
                    note.kill()
                    note.lane.queue.get()
                elif note.rect.collidepoint((index_x, index_y)) and not HandTracking.fixed_y:
                    note.kill()
                    note.lane.queue.get()
        
        

    class GameManager:
        
        # Initialising fps
        fps = 75
        
        # Loading background image
        bg_image = pygame.image.load("bg_images/notes_falling.jpg") # Loading bg image

        # Blits the background image onto the screen at coords (0,0) - top left
        def render_background():
            screen.blit(GameManager.bg_image, (0, 0))
        
        def start_playback():
            # Starting playback of song
            wave_obj = sa.WaveObject.from_wave_file(f"wav_files/{wav_file_name}.wav")
            wave_obj.play()
        
        def read_vars():
            with open("settings_vars.txt", "r") as vars:
                GameManager.fps, Note.speed = [int(x) for x in vars.readline().split()]
        
    # Initialising variables
    GameManager.read_vars()
    
    '''---------------Main game loop------------------'''
    while True:
        
        clock.tick(GameManager.fps) # Starting game timer
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                Note.kill_note_pressed()

        GameManager.render_background()
        HandTracking.landmark_iteration()
        Note.generate_timed_notes(clock)
        Note.note_movement()
        Note.draw_notes()
        pygame.display.update()

if __name__ == "__main__":
  run()

    