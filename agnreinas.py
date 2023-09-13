import numpy as np
import sys
from time import process_time
from geneticprocess import *

#Se requiere tener el paquete Numpy instalado para ejecutar este codigo
#Para ejecutar necesita pasar los siguientes argumentos:
#python agnreinas semilla.py [semilla] [tamaño_tablero] [tamaño_población] [probabilidad_cruza] [probabilidad_mutación] [número_iteraciones]

#Solucion de 15 reinas: python agnreinas.py 4 15 50 0.9 0.08 100
#Solucion de 20 reinas: python agnreinas.py 4 20 60 0.9 0.05 250
#Solucion de 30 reinas: python agnreinas.py 54 30 80 0.9 0.05 300
#Solucion de 50 reinas: python agnreinas.py 42413 50 120 0.95 0.08 600

if((len(sys.argv)-1)<6):
    sys.exit("Faltan argumentos \nEjecute: python agnreinas semilla.py [semilla] [tamaño_tablero] [tamaño_población] [probabilidad_cruza] [probabilidad_mutación] [número_iteraciones]")

#Imprime la solucion encontrada
def printSolution(population, index, table_size, generation):
    print('Solución factible encontrada en la generación '+str(generation)+':')
    for position in population[index]:
        for i in range(1,position+1):
            if(i==position):
                print(' X ', end='')
            else:
                print(' □ ', end='')
        for i in range(position+1, table_size+1):
            print(' □ ', end='')
        print()

#Se almacena los parametros dados por el usuario
seed = int(sys.argv[1])
table_size = int(sys.argv[2])
population_size = int(sys.argv[3])
cross_prob = float(sys.argv[4])
mutation_prob = float(sys.argv[5])
num_iterations = int(sys.argv[6])

#Fitness objetivo que se deberia obtener para que sea una solucion
fitness_obj = 0

#Almacena el tiempo cuando empieza a correr el algoritmo 
t1_start = process_time()

setSeed(seed)

population = initiate_population(population_size, table_size)
fitness,total_fitness = calculate_fitness(population, population_size, table_size)

#Buscamos el cromosoma que tiene el mejor fitness, si este tiene un fitness igual al fitness objetivo
#entonces se encontro una solucion en la poblacion inicial y termina el algoritmo
index = fitness.argmin()
if(fitness[index]==fitness_obj):
    printSolution(population, index, table_size, 0)
    exit
found = False
#Iteramos num_iterations en hacer cruzas con padres de manera aleatoria y obtener hijos y hacer mutaciones, almacenando los padres y hijos que tienen
#el mejor fitness, hasta encontrar el cromosoma que tenga el fitness igual al fitness objetivo, eso significa que encontramos una solucion
for i in range(num_iterations):
    population = set_new_population(population, population_size, fitness, table_size, cross_prob, total_fitness, mutation_prob)
    fitness, total_fitness = calculate_fitness(population, population_size, table_size)
    index = fitness.argmin()
    

    if(fitness[index]==fitness_obj):
        printSolution(population, index, table_size, i)
        found = True
        break
    print('Generation '+str(i+1)+":")
    print('Fitness: '+str(fitness[index])+' Queens Positions:',population[index])
    
    
#Se obtiene el tiempo en que termino el algoritmo, ya sea encontrando una solucion o llego al limite de iteraciones y se calcula cuanto tiempo
#restando el tiempo final con el tiempo inicial
t1_stop = process_time()
if(found==False):
    print('No se ha logrado encontrar una solución factible')
print('Proceso terminado en '+str(t1_stop - t1_start)+' segundos')