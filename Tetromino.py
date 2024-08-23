import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import matplotlib.pyplot as plt
import numpy as np
import pygame
import shapely.affinity
from shapely.geometry import Polygon
import _config_SIMULATOR

class Tetromino:
    def __init__(self, constructor_vertices:list[tuple], scaler = 1) -> None:
        self.id = id
        self.polygon = Polygon(constructor_vertices*scaler*_config_SIMULATOR.TILE_SIZE)
        self.__angle = 0.0
        self.color = _config_SIMULATOR.COLOR_OBJECT
    
    @property
    def center(self) -> tuple:
        center = self.polygon.centroid.coords.xy
        return np.array([center[0][0], center[1][0]])
    
    @property
    def vertices(self) -> np.array:
        vertices = self.polygon.exterior.coords.xy
        return np.array([vertices[0], vertices[1]]).T
    
    @center.setter
    def center(self, new_center: tuple) -> None:
        self.polygon = shapely.affinity.translate(self.polygon, xoff=new_center[0] - self.center[0], yoff=new_center[1] - self.center[1], zoff=0.0)

    def rotate(self, angle: float) -> None:
        self.polygon = shapely.affinity.rotate(self.polygon, angle, origin='centroid', use_radians=False)
        self.__angle = (self.__angle + angle)%360

    def translate(self, direction) -> None:
        self.polygon = shapely.affinity.translate(self.polygon, xoff=direction[0], yoff=direction[1], zoff=0.0)
        
    def plot(self) -> None:
        x_values, y_values = zip(*self.vertices)
        plt.plot(x_values, y_values)  # Plot the vertices
        plt.plot(self.center[0],self.center[1], 'ro')  # Mark the first vertex with a red dot
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Tetromino')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
  
    def set_angle(self, new_angle):
        angle = new_angle - self.__angle
        self.polygon = shapely.affinity.rotate(self.polygon, angle, origin='centroid', use_radians=False)
        self.__angle = new_angle
    
    @property
    def angle(self) -> float:
        return self.__angle
    
    def print_info(self) -> None:
        print('center: {}'.format(self.center))
        print('angle: {}'.format(self.__angle))
 
    def draw(self, screen: pygame.Surface) -> None:
        #pygame.draw.polygon(screen, self.color, self.vertices, 0)        # fill
        pygame.draw.polygon(screen, _config_SIMULATOR.COLOR_OBJECT, self.vertices, width=3)     # draw outline in black
        pygame.draw.circle(screen, _config_SIMULATOR.COLOR_OBJECT_CENTER, self.center, 5)       #draw center
        

if __name__ == '__main__':
    pass