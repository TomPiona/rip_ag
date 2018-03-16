__out_of__ = 1

try:
    import numpy as np
    if np.isclose(Output_per_worker2050, 468103, atol=1000)\
        and np.isclose(Output_per_worker2100, 1055954, atol=1000)\
        and np.isclose(Output_per_worker2150, 2280114, atol=1000):
        __score__ += 1
except: 
  pass