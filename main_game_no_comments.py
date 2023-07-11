import pygame
import sys
import random
import numpy as np
import simpleaudio as sa
import queue
from dataclasses import dataclass

wav_file_name = "message_bottle"

def run():

    pygame.init()
    clock = pygame.time.Clock()

    screen_width = 1024
    screen_height = 1024
    screen = pygame.display.set_mode((screen_width,screen_height), vsync=1)
    pygame.display.set_caption('NEA Rhythm Game')

    lanes = 6
    lane_size = screen_width//lanes

    @dataclass
    class Lane:
        x: int
        queue: queue.Queue
        key: int

    class Note(pygame.sprite.Sprite):

        note_group = pygame.sprite.Group() 
        note_keys = [pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k, pygame.K_l]
        lane_tracker = [Lane(lane_size*num_lanes, queue.Queue(), key) for num_lanes, key in zip(range(lanes), note_keys)]
        note_width = lane_size
        note_height = screen_height//10
        note_times = (np.genfromtxt("turning_points.txt", delimiter = ", ")*1000).astype(int)
        bg_image = pygame.image.load("bg_images/notes_falling.jpg") 

        def __init__(self) -> None:
            super().__init__()
            self.lane = Note.get_random_lane()
            self.rect = pygame.Rect(self.lane.x, 0, Note.note_width, Note.note_height)
            self.image = pygame.Surface((Note.note_width, Note.note_height))
            self.image.fill((255, 255, 255)) 
            self.add_to_group() 
            self.add_to_queue() 

        def get_random_lane() -> Lane:
            return random.choice(Note.lane_tracker)

        def add_to_group(self):
            Note.note_group.add(self)

        def add_to_queue(self):
            self.lane.queue.put(self)

        def draw_notes():
            Note.note_group.draw(screen)

        def generate_notes(num_notes):
            for _ in range(num_notes):
                Note()

        def generate_timed_notes(clock):
            current_time = pygame.time.get_ticks()
            accepted_times = np.asarray(list(range(current_time - clock.get_time(), current_time)))
            matched_elements = np.isin(Note.note_times, accepted_times)
            Note.generate_notes(np.count_nonzero(matched_elements))

        def kill_note_pressed():
            for lane in Note.lane_tracker:
                if event.key == lane.key:
                    if not lane.queue.empty():
                        lane.queue.get().kill()

        def note_movement():
            speed = 5

            for sprite in Note.note_group.sprites():
                sprite.rect.y += speed

                if sprite.rect.y > screen_height:
                    sprite.kill()
                    sprite.lane.queue.get() 

            Note.note_group.update() 

        def render_background():
            screen.blit(Note.bg_image, (0, 0))

    wave_obj = sa.WaveObject.from_wave_file(f"wav_files/{wav_file_name}.wav")
    wave_obj.play()

    '''---------------Main game loop------------------'''
    while True:

        clock.tick(75) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                Note.kill_note_pressed()

        Note.render_background()
        Note.generate_timed_notes(clock)
        Note.note_movement()
        Note.draw_notes()
        pygame.display.update()

if __name__ == "__main__":
  run()