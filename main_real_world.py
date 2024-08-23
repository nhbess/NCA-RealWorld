import numpy as np

import _config_SIMULATOR
import Shapes
from Board import Board, Neigbor_type
from Simulator import Simulator
from Tetromino import Tetromino

_config_SIMULATOR.TILE_SIZE = 100           # Pixels size of the tiles, only affects visualization
_config_SIMULATOR.SAVE_ANIMATION = False    # Save animation as gif

board = Board(N=4, M=4, neighberhood_type=Neigbor_type.Chebyshev)
simulator = Simulator(board)
simulator.run()