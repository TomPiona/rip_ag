__out_of__ = 1

try:
    import numpy as np
    if np.isclose(Growth_Rate_1000BC_to_1000AD, 0.0008, atol=0.001)\
        and np.isclose(Growth_Rate_1400_to_1600, 0.0022, atol=0.001)\
        and np.isclose(Growth_Rate_1900_to_1950, 0.0087, atol=0.001):
        __score__ += 1
except: 
  pass