import random
from datetime import datetime   
import numpy as np
def roulette(size, items, sum_items):
    proportion = np.zeros(size, dtype=float)
    for i in range(size):
        proportion[i] = items[i]/sum_items 
        if(i>0):
            proportion[i]+=proportion[i-1]
    rng = np.random.random()
    index_1 = 0
    index_2 = 0
    for i in range(size):
        if(rng<proportion[i]):
            index_1 = i
            break
    while True:
        rng2 = np.random.random()
        for i in range(size):
            if(rng2<proportion[i]):
                index_2 = i
                break
        if(index_1 != index_2):
            break
    
    return index_1, index_2