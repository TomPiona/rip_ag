import pandas as pd

t = pd.read_csv('hw1.csv')
print(t.isnull().mean())