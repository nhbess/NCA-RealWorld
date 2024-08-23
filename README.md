# Hello!

So, I refactored a little bit.
File by file:

### _config...py 
_config.. files just handle some colors and key handlers and random stuff necesary for the NCA

### Board.py
Board is the cool one, it acts as a collection of tiles, set their neighberhoods and allow you to batch manage the tiles.
I divided the set up of the contact mask in two methods:
    - update_contact_tiles_from_real_world(self, contact_mask:np.array) -> None
    - update_contact_tiles_from_tetromino(self, target_polygons: list[Polygon]) -> None

Both of the will change the self.is_contact of each tile, the second method is used when you have a virtual tetromino and you move it around with the keyboar. The first one is the important and we will check it in a while. The important thing rigth now is that you give to the method the real world array and it maps it into the tiles. (Tiles in this context is each sensor).

### Chebyshev_HS_10.pkl
This is the NCA model, I pushed the training in the git of the previous paper. Nothing different, just trained in a 4x4 board.

### InputKeysHandler.py
Just handle the keys when there is a virtual tetromino in the simulator.

### main_tetromino_user.py, main_real_world.py and Simulator.py
Two examples, one with a virtual tetromino and one with real world data. They are extacly the same Simulator, if you dont add a tetromino it will take the data from the real world.

### NCA.py and StateStructure.py
You need the class to load the .pkl file and initialize the NCA

### Shapes.py and Tetromino.py
The first one contains the available shapes, and the second handle the virtual object (if there is one).

### Visualization.py
That just some pygame visuals, I moved some methods there to handle everything in the same file.

### RealWorldContactMask.py
This is the one that you need to implement !!!

# How does it works?
Open the main_real_world.py file.
First you create a Board object, this one will create all the tiles, set their neighborhoods, and initialize the NCA on each one.
Every time you need to interact with a tile you do it through the Board class.
The method that matters here is, as mention before, the update_contact_tiles_from_real_world(self, contact_mask:np.array) -> None:
this methods gets a contact mask (a 4x4 array full of True/False or 0/1s) and set the self.is_contact of each tile respectivelly.

Where the heck does that contact mask comes from?
Check the Simulator class, the method set_contact_tiles() in line 38. If there is no virtual tetromino it will call the method that you should implement. And basically that is all.

# Some further details
Class tile has (bellow the #AI title):
    - self._ESTIMATION = self.matrix_position # Default estimation is their own position.
    - self._HIDDEN = [0]*self.ss.hidden_dim   # Hidden channels for communication between tiles.

The _ESTIMATION is the [x,y] belief of where is the center of the object, you may need this to compare it with the real world value.