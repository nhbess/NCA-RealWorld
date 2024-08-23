import numpy as np
import time


# --------------------------------------------------------------------------------------------
# Yo Bailey, this is the function that you should implement getting the contact mask from the real world
# --------------------------------------------------------------------------------------------


time_now = time.time()
mask = np.random.randint(low=0,high=2,size=(4, 4)) 
def dummy_contact_mask(): # This is a dummy mask that changes every second
    global mask
    global time_now
    if time.time() - time_now > 1:
        time_now = time.time()
        mask = np.random.randint(low=0,high=2,size=(4, 4))
    return mask