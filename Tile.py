import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np
from shapely.geometry import Point, Polygon
import shapely.affinity
import pickle
import torch
import torch.nn as nn
from StateStructure import StateStructure
import sys
import _config_SIMULATOR


class Sensor:
    def __init__(self, center:np.array) -> None:
        self.point = Point(center)
    
    @property
    def center(self) -> tuple:
        return np.array([self.point.x, self.point.y])

    @center.setter
    def center(self, new_center: tuple) -> None:
        self.point = shapely.affinity.translate(self.point, xoff=new_center[0], yoff=new_center[1], zoff=0.0)

class Tile:
    def __init__(self, id:int, matrix_position:np.array) -> None:
        self.id = id
        self.matrix_position = matrix_position
        self.polygon = Polygon(np.array([(0, 0), (1, 0), (1, 1), (0, 1)])*_config_SIMULATOR.TILE_SIZE)
        
        self.sensors: list[Sensor] = []
        self.is_contact = False
        self.is_target = False

        self.neighbors:list[Tile] = []
        

        #AI 
        self.ss = StateStructure(
                        estimation_dim  = 2,    
                        constant_dim    = 2,   
                        sensor_dim      = 1,   
                        hidden_dim      = 10)
        
        self._ESTIMATION = self.matrix_position # Default estimation is their own position
        self._HIDDEN = [0]*self.ss.hidden_dim
        self.model = self._load_model('Chebyshev_HS_10.pkl')
        

    def _load_model(self, model_path:str) -> nn.Module:
        with open(model_path, 'rb') as handle:
            model = pickle.load(handle)
        return model
    
    @property
    def vector_movement(self) -> tuple:
        return self._vector_movement
    
    @vector_movement.setter
    def vector_movement(self, new_vector: tuple) -> None:
        new_vector = np.array(new_vector)
        if np.linalg.norm(new_vector) != 0:
            new_vector = new_vector / np.linalg.norm(new_vector)
        self._vector_movement = np.array(new_vector)*1/2

    @property
    def center(self) -> tuple:
        center = self.polygon.centroid.coords.xy
        return np.array([center[0][0], center[1][0]])

    @center.setter
    def center(self, new_center: tuple) -> None:
        self.polygon = shapely.affinity.translate(self.polygon, xoff=new_center[0], yoff=new_center[1], zoff=0.0)
        #self.OBJECT_CENTER = self.center
        self._ESTIMATION = self.matrix_position

    @property
    def target_neighbors(self) -> list['Tile']:
        return [neighbor for neighbor in self.neighbors if neighbor.is_target]

    @property
    def contact_neighbors(self) -> list['Tile']:
        return [neighbor for neighbor in self.neighbors if neighbor.is_contact]
    
    @property
    def non_contact_neighbors(self) -> list['Tile']:
        return [neighbor for neighbor in self.neighbors if not neighbor.is_contact]
    
    @property
    #TODO this shouldnot be hardcoded
    def state(self) -> None:
        state = [
            self._ESTIMATION[0],
            self._ESTIMATION[1],
            self.matrix_position[0],
            self.matrix_position[1],
            int(self.is_contact),
            *self._HIDDEN
        ]
        return torch.Tensor(state)

    @state.setter
    #TODO this shouldnot be hardcoded
    def state(self, new_state: torch.Tensor) -> None:
        self._ESTIMATION = new_state[0:2].detach().numpy()
        self.matrix_position = new_state[2:4].detach().numpy()
        self.is_contact = bool(new_state[4].detach().numpy())
        self._HIDDEN = new_state[5:].detach().numpy()
        
    @property
    def perception_state(self) -> torch.Tensor:
        perception_state = torch.zeros(1, self.ss.state_dim, 3, 3)
        perception_state[0, ... , 1, 1] = self.state
        
        for neighbor in self.neighbors:
            relative_position = neighbor.matrix_position - self.matrix_position
            x, y = relative_position + 1
            perception_state[0, ... , int(x), int(y)] = neighbor.state
        return perception_state

    # BEHAVIOR
    def behave(self) -> None:
        output = self.model(input_state=self.perception_state, num_steps=1) # This is the forward pass of the NCA
        center_tile = output[0, ... , 1, 1]
        self.state = center_tile


    # VISUALIZATION
    def draw(self, screen: pygame.Surface) -> None:
        from Visualization import draw_tile
        draw_tile(self, screen)

    def draw_object_center(self, screen: pygame.Surface) -> None:
        from Visualization import draw_object_center
        draw_object_center(self, screen)
            
    def is_membrane(self) -> bool:
        return len(self.contact_neighbors) != len(self.neighbors)
    
    def __repr__(self) -> str:
        #return f'T{self.id}'
        #return f'{self.matrix_position}'
        return f'{int(self.is_contact)}'
    
    def print(self) -> None:
        print(f'Tile {self.id} at {self.matrix_position} with center {self.center}, is_contact: {self.is_contact}, is_target: {self.is_target}')

if __name__ == '__main__':
    pass
