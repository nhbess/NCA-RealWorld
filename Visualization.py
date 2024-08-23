import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import numpy as np
import pygame

import _config_SIMULATOR
from Tile import Tile


def draw_object_center(tile:Tile, screen: pygame.Surface) -> None:
    center = tuple(map(int, np.array(tile._ESTIMATION) * _config_SIMULATOR.TILE_SIZE + _config_SIMULATOR.TILE_SIZE/2))
    pygame.draw.circle(screen, _config_SIMULATOR.COLOR_ESTIMATION, center, 5)

def draw_tile(tile:Tile, screen: pygame.Surface) -> None:
    if tile.is_contact:     color = _config_SIMULATOR.COLOR_CONTACT_TILE
    else:                     color = _config_SIMULATOR.COLOR_TILE
    
    
    border = np.array(tile.polygon.exterior.coords[:-1])
    pygame.draw.polygon(screen, color, border, 0)
    pygame.draw.polygon(screen, _config_SIMULATOR.COLOR_TILE_CONTOUR, border, 1)
        
    #for sensor in tile.sensors:
    #    pygame.draw.circle(screen, config.COLOR_SENSOR, sensor.center, 2)
    
    