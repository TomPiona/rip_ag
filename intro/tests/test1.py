__out_of__ = 3

try:
	if x == 10.5:
		__score__ += 1
except: 
  pass
try:
	if y == 7.2:
		__score__ += 1
except: 
  pass
try:
	import numpy as np
	if np.isclose(combo, 75.6):
		__score__ += 1
except: 
  pass