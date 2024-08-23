import sys

import numpy as np
import pygame

import _config_SIMULATOR


def handle_key_input(pressed_keys:dict) -> None:
    for event in pygame.event.get():
        #QUIT THE GAME
        if event.type == pygame.QUIT:
            _config_SIMULATOR.QUIT_GAME = True

        #PAUSE THE GAME
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                _config_SIMULATOR.GAME_IN_PAUSE = not _config_SIMULATOR.GAME_IN_PAUSE


        #MOVE THE TETROMINO
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                _config_SIMULATOR.QUIT_GAME = True
            if event.key == pygame.K_UP:
                pressed_keys['up'] = True
            elif event.key == pygame.K_DOWN:
                pressed_keys['down'] = True
            elif event.key == pygame.K_RIGHT:
                pressed_keys['right'] = True
            elif event.key == pygame.K_LEFT:
                pressed_keys['left'] = True
            elif event.key == pygame.K_d:
                pressed_keys['rot_right'] = True
            elif event.key == pygame.K_a:
                pressed_keys['rot_left'] = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                pressed_keys['up'] = False
            elif event.key == pygame.K_DOWN:
                pressed_keys['down'] = False
            elif event.key == pygame.K_RIGHT:
                pressed_keys['right'] = False
            elif event.key == pygame.K_LEFT:
                pressed_keys['left'] = False
            elif event.key == pygame.K_d:
                pressed_keys['rot_right'] = False
            elif event.key == pygame.K_a:
                pressed_keys['rot_left'] = False
    
    return pressed_keys


def get_net_vector_angle(pressed_keys:dict):
    translation_vector = np.array([0, 0])
    rotation_angle = 0

    if pressed_keys['rot_left']:    rotation_angle += _config_SIMULATOR.INPUT_ROTATION_SCALER
    elif pressed_keys['rot_right']: rotation_angle -= _config_SIMULATOR.INPUT_ROTATION_SCALER
    if pressed_keys['up']:          translation_vector[1] -= _config_SIMULATOR.INPUT_TRANSLATION_SCALER
    elif pressed_keys['down']:      translation_vector[1] += _config_SIMULATOR.INPUT_TRANSLATION_SCALER
    if pressed_keys['right']:       translation_vector[0] += _config_SIMULATOR.INPUT_TRANSLATION_SCALER
    elif pressed_keys['left']:      translation_vector[0] -= _config_SIMULATOR.INPUT_TRANSLATION_SCALER
    
    return translation_vector, rotation_angle

if __name__ == "__main__":
    pass