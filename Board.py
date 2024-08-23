import os
import _config_SIMULATOR
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import numpy as np
import pygame
from matplotlib import pyplot as plt
from shapely.geometry import Polygon
from Tile import Sensor, Tile
import sys
from StateStructure import StateStructure
from Tetromino import Tetromino

class Neigbor_type:
    Manhattan = 0
    Chebyshev = 1

class Board:
    def __init__(self, N:int, M:int = None, neighberhood_type=Neigbor_type.Manhattan):
        self.neighberhood_type = neighberhood_type
        self.X = N
        self.Y = N
        if M: self.Y = M
        self.tiles: np.array[[Tile]] = self.__create_tiles()

    #TILES and NEIGHBORS
    def __create_tiles(self):
        tiles:list[Tile] = []
        for x in range(self.X):
            for y in range(self.Y):
                pos = np.array([x, y])
                tile = Tile(id=len(tiles), matrix_position=np.array(pos))
                tile.center = np.array(pos*_config_SIMULATOR.TILE_SIZE)
                tile.sensors.append(Sensor(tile.center))
                tiles.append(tile)
        
        tiles_grid = np.array(tiles).reshape(self.X, self.Y)

        for tile in tiles:
            x, y = tile.matrix_position
            if self.neighberhood_type == Neigbor_type.Manhattan:
                neighbors_positions = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
            elif self.neighberhood_type == Neigbor_type.Chebyshev:
                neighbors_positions = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                                       (x - 1, y),                 (x + 1, y),
                                       (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]    
            else:
                raise Exception("Neighberhood type not defined")
            
            tile.neighbors = [tiles_grid[p[0]][p[1]] for p in neighbors_positions if 0 <= p[0] < self.X and 0 <= p[1] < self.Y]
        return tiles_grid
    

    #VISUALIZATION
    def draw(self, screen: pygame.Surface) -> None:
        tile: Tile
        for tile in self.tiles.flatten():
            tile.draw(screen)

        for tile in self.tiles.flatten():
            tile.draw_object_center(screen)

    #PRELIMINARY
    def set_target_tiles(self, target_polygon: Polygon) -> None:
        for tile in self.tiles.flatten():
            tile: Tile
            tile.is_target = any(target_polygon.contains(sensor.point) for sensor in tile.sensors)

    def set_target_tile_by_position(self, position: np.array) -> None:
        self.get_tile_by_position(position).is_target = True

    def get_tile_by_position(self, position: np.array) -> Tile:
        x, y = position
        return self.tiles[int(position[0])][int(position[1])]

    #MAIN LOOP
    def update_contact_tiles_from_real_world(self, contact_mask:np.array) -> None:
        contact_mask = contact_mask.flatten()        
        for cm, tile in zip(contact_mask, self.tiles.flatten()):
            tile: Tile
            tile.is_contact = cm
          
    def update_contact_tiles_from_tetromino(self, target_polygons: list[Polygon]) -> None:
        for tile in self.tiles.flatten():
            tile: Tile
            tile.is_contact = any(polygon.contains(sensor.point) for sensor in tile.sensors for polygon in target_polygons)

    def behave(self) -> None:
        random_order = np.random.choice(len(self.tiles.flatten()), len(self.tiles.flatten()), replace=False)
        for index in random_order:
            tile:Tile = self.tiles.flatten()[index]
            tile.behave()
    
    # Random stuff
    def print_state(self) -> None:
        board_state = np.zeros([5, self.X, self.Y]) 
        for tile in self.tiles.flatten():
            tile: Tile
            sensiblex, sensibley = tile._ESTIMATION
            x,y = tile.matrix_position
            sensor = int(tile.is_contact)
            tile_state = np.array([sensiblex, sensibley, x, y, sensor])
            board_state[..., int(x), int(y)] = tile_state
        #print(board_state)
        transpose = np.transpose(board_state, (0, 2, 1))
        print(transpose)
    
        print('-'*10)
         
    @property
    def contact_tiles(self) -> list[Tile]:
        return [tile for tile in self.tiles.flatten() if tile.is_contact]
    @property
    def target_tiles(self) -> list[Tile]:
        return [tile for tile in self.tiles.flatten() if tile.is_target]

if __name__ == "__main__":
    tetero = Tetromino(constructor_vertices=_config_SIMULATOR.VERTICES_T)
    board = Board(5)
    contact = board.get_contact_mask(tetero)
    print(contact)
    pass
