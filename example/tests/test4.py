__out_of__ = 1

try:
    import numpy as np
    if np.isclose(SoLtypical1400to1600, 916, atol=10) and np.isclose(SoLtypical1900to1950, 1405, atol=10):
        __score__ += 1
except: 
  pass