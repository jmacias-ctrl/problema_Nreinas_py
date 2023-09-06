import random
from datetime import datetime   
import numpy as np
def roulette(size, items, sum_items):
    proportion = np.zeros(size, dtype=float)
    for i in range(size):
        proportion[i] = items[i]/sum_items 
        if(i>0):
            proportion[i]+=proportion[i-1]
    random.seed(datetime.now().timestamp())
    rng = random.uniform(0,1)
    index_1 = 0
    index_2 = 0
    for i in range(size):
        if(proportion[i]==1):
            break
        elif(proportion[i]<=rng and proportion[i+1]>=rng):
            index_1 = i

    while True:
        random.seed(datetime.now().timestamp())
        rng2 = random.uniform(0,1)
        for i in range(size):
            if(proportion[i]==1):
                break
            elif(proportion[i]<=rng2 and proportion[i+1]>=rng2):
                index_2 = i
        if(index_1 != index_2):
            break
    return index_1, index_2