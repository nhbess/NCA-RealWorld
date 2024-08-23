import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import numpy as np
import pygame
from InputKeysHandler import handle_key_input, get_net_vector_angle
import _config_SIMULATOR
from Board import Board
import sys
import time
import math
import RealWorldContactMask

class Simulator():
    def __init__(self, board:Board) -> None:
        self.board = board
        self.tetrominos = []

        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Simulator')
        self.screen = pygame.display.set_mode([self.board.X*_config_SIMULATOR.TILE_SIZE, self.board.Y*_config_SIMULATOR.TILE_SIZE])
        
        #User input
        self.pressed_keys = {'down':False, 'up':False, 'left':False, 'right':False, 'rot_left':False, 'rot_right':False}
                
        #Other stuff
        self.frames = []
        self._iteration = 0

    @property
    def iteration(self):
        self._iteration += 1
        return self._iteration
    
    def add_tetromino(self, tetromino) -> None:
        self.tetrominos.append(tetromino)
    
    def set_contact_tiles(self) -> None:
        if len(self.tetrominos) == 0:
            contact_mask = RealWorldContactMask.dummy_contact_mask() # This is the real world mask
            self.board.update_contact_tiles_from_real_world(contact_mask)

        else:
            target_polygons = [t.polygon for t in self.tetrominos]
            self.board.update_contact_tiles_from_tetromino(target_polygons) # If there is a virtual tetromino, it will be used to update the contact tiles
    
    def move_tetromino_user(self) -> None:
        if len(self.tetrominos) == 0: return
        translation_vector, rotation_angle = get_net_vector_angle(self.pressed_keys)
        self.tetrominos[0].rotate(rotation_angle)
        self.tetrominos[0].translate(translation_vector)
    
    def quit_game(self) -> None:
        pygame.quit()
        sys.exit()

    def make_gif(self) -> None:
        if _config_SIMULATOR.SAVE_ANIMATION:
            self.frames.append(pygame.surfarray.array3d(self.screen))
            if _config_SIMULATOR.QUIT_GAME:
                import imageio
                import datetime
                now = datetime.datetime.now()
                formatted_now = now.strftime("%Y-%m-%d_%H-%M-%S")
                filename = f'{formatted_now}.gif'
                imageio.mimsave(filename, self.frames, duration=20)
            
    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.board.draw(self.screen)
        for tetromino in self.tetrominos:
            tetromino.draw(self.screen)
        pygame.display.flip()
     
    def print_angle(self) -> None:
        period = math.pi*2/math.radians(90)
        error = math.sin(math.radians(self.tetrominos[0].angle)*period - math.pi/2)+1
        print(f'True Angle: {self.tetrominos[0].angle} Target Angle: {error}')

    def run(self) -> None:        
        while True:
            self.pressed_keys = handle_key_input(self.pressed_keys)
            if _config_SIMULATOR.GAME_IN_PAUSE: continue
            self.clock.tick(_config_SIMULATOR.FPS)
            
            self.set_contact_tiles()
            self.board.behave()
            self.move_tetromino_user()
            self.draw()
            pygame.display.flip()

            self.make_gif()
            if _config_SIMULATOR.QUIT_GAME: self.quit_game()
            
if __name__ == '__main__':
    pass