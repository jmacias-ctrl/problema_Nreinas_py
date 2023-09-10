import random
from datetime import datetime   
import numpy as np

#Entrada:
#-size: En este contexto, es el tamaño de la poblacion
#-items: En este contexto, es el array de los fitness de la poblacion
#-sum_items: En este contexto, es el fitness total, que es la suam de todos los fitness de la poblacion
#Salida:
#El fitness es un array de tamaño poblation_size, por lo tanto cada indice representa una fila del array 2d poblation
#que es el conjunto de cromosomas que son las posibles posiciones de table_size reinas
#Lo que hace esta ruleta es dividir todos los valores del array fitness por el total de fitness, dando una proporcion
#Luego recorremos el array y sumamos el valor de la proporcion n con el valor de la proporcion anterior n-1
#Esto nos da una probabilidad de 0 a 1
#Luego sacamos un numero aleatorio entre 0 y 1 y buscamos dentro del array el valor mas cercano al obtenido y obtenemos su indice
#lo hacemos por segunda vez y estos seran los dos indices padres de la poblacion y se retornan estos
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