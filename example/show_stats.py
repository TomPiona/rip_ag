import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

last = 7
t = pd.read_csv('hw1.csv', header=None)
plt.barh(np.arange(1,last), [np.mean(t[i]) for i in np.arange(1,last)], align='center', alpha=0.5)
plt.title('E[question]')
plt.show()
plt.hist(t[last], bins=np.arange(-.5, max(t[last])+1.5, 1))
plt.title('Total Score Histogram')
plt.show()
print([t[i].value_counts()[:5] for i in np.arange(1, last)])