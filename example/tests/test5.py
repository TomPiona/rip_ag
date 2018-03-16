__out_of__ = 1

try:
    import numpy as np
    if np.isclose(YoverLstarinitial, 130000, atol=1000):
        __score__ += 1
except: 
  pass