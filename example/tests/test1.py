__out_of__ = 1

try:
    import numpy as np
    if np.isclose(Capital_output_ratio2050, 4.46, atol=0.1) and np.isclose(Capital_output_ratio2100, 4.75, atol=0.1) and np.isclose(Capital_output_ratio2150, 4.84, atol=0.1):
        __score__ += 1
except: 
    pass