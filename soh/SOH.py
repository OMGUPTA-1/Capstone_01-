import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import pandas as pd

data = pd.read_csv('data_csv.csv')
delta_v = data['Delta V']
cycle = data['Cycle Count']
delta_t = data['Delta T']

A = 0.5192
B = 0.0405
soh = [(A * (delta_t[i]/delta_v[i]) + B)for i in range(len(cycle))] 
plt.plot(cycle+1, soh)
plt.show()
