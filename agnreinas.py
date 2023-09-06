import numpy as np
import sys
from time import process_time
from geneticprocess import *
if((len(sys.argv)-1)<6):
    sys.exit("Faltan argumentos \nEjecute: python agnreinas semilla.py [semilla] [tamaño_tablero] [tamaño_población] [probabilidad_cruza] [probabilidad_mutación] [número_iteraciones]")
seed = int(sys.argv[1])
table_size = int(sys.argv[2])
population_size = int(sys.argv[3])
cross_prob = float(sys.argv[4])
mutation_prob = float(sys.argv[5])
num_iterations = int(sys.argv[6])

t1_start = process_time()
setSeed(seed)

population = initiate_population(seed, population_size, table_size)
fitness,total_fitness = calculate_fitness(population, population_size, table_size)

index = fitness.argmin()
if(fitness[index]==0):
    print('Solucion encontrada:',population[index])
    exit

for i in range(num_iterations):
    population = set_new_populatiopn(population, population_size, fitness, table_size, cross_prob, total_fitness, mutation_prob)
    fitness, total_fitness = calculate_fitness(population, population_size, table_size)
    index = fitness.argmin()
    print('Generation '+str(i)+":")
    print('Fitness: '+str(fitness[index])+' Queens Positions:',population[index])
    if(fitness[index]==0):
        print('Solución encontrada')
        break
t1_stop = process_time()
print('Proceso terminado en '+str(t1_stop - t1_start)+' segundos')