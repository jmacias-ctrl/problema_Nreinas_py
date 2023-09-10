import numpy as np
from numpy import random
import math
import sys
import random as rng
from roulette import *

#Entrada: getSeed->Numero Seed para establecer el generador de numeros aleatorios
#Salida: True
def setSeed(getSeed):
    np.random.seed(getSeed)
    return True

#Entradas: 
#- population_size->Tamaño de la poblacion
#- table_size->tamaño del tablero de ajedrez (tambien indica cuantas reinas deben haber por filas)
#Salida:
#Retorna un array 2d de tamaño population_size x table_size de genes generado de manera aleatoria
#mediante creaciones de arrays de tamaño de table_size con la funcion shuffle para desordernar el array.
def initiate_population(population_size, table_size):
    population = np.zeros(shape=(population_size, table_size), dtype=int)
    for i in range(population_size):
        x = np.arange(1, table_size+1)
        np.random.shuffle(x)
        population[i] = x
    return population

#Entradas:
#- population->Array 2d de tamaño poblacion_size x table_size, donde las filas son los cromosomas y cada gen de un cromosoma es un posicion de una reina en una fila
#- population_size->Tamaño de la poblacion
#- table_size->tamaño del tablero de ajedrez (tambien indica cuantas reinas deben haber por filas)
#Salida:
#Retorna el valor fitness de cada gen dentro de la poblacion, siendo un arary 1d de tamaño poblacion_size, siendo este el calculo de la cantidad
#de choques que se tienen cada reinas con otras reinas, siendo 0 cuando no hay reinas que se chocan entre si, tambien retorna el valor total de fitness
#que es la suma de todos los fitness del array
def calculate_fitness(population, population_size, table_size):
    fitness = np.zeros(population_size, dtype=int)
    totalFitness = 0
    pos=0
    for gen in population:
        set_fitness = 0
        for i in range(table_size):
            queenPosX = gen[i]
            j = i+1
            iteration = 1
            colision = 0
            while j < table_size:
                queenPosY = gen[j]
                l_x = queenPosX - iteration
                r_x = queenPosX + iteration
                if((queenPosY == l_x) or (queenPosY == r_x)):
                    set_fitness+=1
                    colision+=1
                j+=1
                iteration+=1
                
            j = i-1
            iteration = 1
            while j>=0:
                queenPosY = gen[j]
                l_x = queenPosX - iteration
                r_x = queenPosX + iteration
                if((queenPosY == l_x) or (queenPosY == r_x)):
                    set_fitness+=1
                    colision+=1
                iteration+=1
                j-=1
        fitness[pos] = set_fitness
        totalFitness+=set_fitness
        pos+=1
    return fitness, totalFitness

#Entrada:
#- population->Array 2d de tamaño poblacion_size x table_size, donde las filas son los cromosomas y cada gen de un cromosoma es un posicion de una reina en una fila
#- population_size->Tamaño de la poblacion
#- table_size->tamaño del tablero de ajedrez (tambien indica cuantas reinas deben haber por filas)
#- fitness->El valor fitness de cada fila del array population
#- cross_prob->la probabilidad de cruza entre dos cromosomas (en este caso dos tableros de tamaño table_size con posiciones de table_size reinas)
#- mutation_prob->la probabilidad de mutacion en un hijo
#- total_fitness->la sumatoria de todos los fitness
#Salida:
#Un array 2d de tamaño population_size x table_size llamado new_population que contiene los hijos que son obtenidos cruzando de una seleccion aleatoria de padres del array 2d population
#y tambien padres que tengan el mejor fitness (esten mas cercano a una solucion)
def set_new_population(population, population_size, fitness, table_size, cross_prob, total_fitness, mutation_prob):
    new_population = np.zeros(shape=(population_size, table_size), dtype=int)
    i = 0
    while(i<population_size):
        cross_indv1, cross_indv2 = roulette(population_size,fitness,total_fitness)
        randomNumber = np.random.random()
        if(randomNumber<=cross_prob):
            newIndividual = chromosome_cross(population, mutation_prob, table_size,cross_indv1,cross_indv2)
            newIndividual2 = chromosome_cross(population, mutation_prob, table_size,cross_indv2,cross_indv1)
            new_population[i] = newIndividual
            new_population[i+1] = newIndividual2
            i+=2
    new_fitness, total_fitnes= calculate_fitness(new_population, population_size, table_size)
    atFitness = np.append(new_fitness,fitness)
    atPopulation = np.concatenate((new_population, population))
    best_fitness = np.argsort(atFitness)
    best_individuals = np.zeros(shape=(population_size, table_size), dtype=int)
    for i in range(population_size):
        best_individuals[i] = atPopulation[best_fitness[i]]
    return best_individuals


#Entrada:
#- population->Array 2d de tamaño poblacion_size x table_size, donde las filas son los cromosomas y cada gen de un cromosoma es un posicion de una reina en una fila
#- mutation_prob->la probabilidad de mutacion en un hijo
#- table_size->tamaño del tablero de ajedrez (tambien indica cuantas reinas deben haber por filas)
#- indexInd1->El primer cromosoma (o tambien fila del array de population) en que sera utilizado para la cruza
#- indexInd2->El segundo cromosoma (o tambien fila del array de population) en que sera utilizado para la cruza
#Salida:
#Retorna un hijo que fue obtenido siempre y cuando este dentro de la probabilidad, del padre de population[indexInd1] y population[indexInd2], indices que fueron
#obtenidos por ruleta, siendo la seleccion de una cantidad aleatoria de genes tanto para el primer padre como el segundo
#Tambien es posible que el hijo pueda mutar, siempre y cuando este dentro de la posiblidad.
def chromosome_cross(population, cross_mutation, table_size, indexInd1, indexInd2):
    indices = np.random.randint(2, table_size)
    rngSplit = np.random.random()
    if(rngSplit>=0.6):
        chromosomeF1, chromosomeF2 = population[indexInd1][:indices], population[indexInd2][indices:]
    else:
        chromosomeF1, chromosomeF2 = population[indexInd2][:indices], population[indexInd1][indices:]
    chromsomeFinal = chromosome_cross_correction(np.concatenate((chromosomeF2,chromosomeF1)), table_size)
    return mutation(chromsomeFinal, cross_mutation, table_size)


#Entrada:
#- chromosomeFinal->Es el hijo (array de tamaño table_size con los valores de las posiciones de table_size reinas) obtenido a partir de dos padres
#- table_size->tamaño del tablero de ajedrez (tambien indica cuantas reinas deben haber por filas)
#Salida:
#Durante la cruza, es posible que hayan numeros que se repitan en el array del hijo, esto significa que hay reinas que se estan chocando ded manera
#vertical, esto se soluciona mediante esta solucion, lo que se hace es buscar las posiciones de reinas que se van repitiendo en el array, reemplazandolas
#por posiciones que no estan dentro del array hijo
#Retorna el hijo con estas corecciones
def chromosome_cross_correction(chromsomeFinal, table_size):
    seenValues = np.zeros(table_size, dtype=int)
    indexDuplicate = []
    for i in range(len(chromsomeFinal)):
        if(seenValues[chromsomeFinal[i]-1]>0):
            indexDuplicate.append(i)
        else:
            seenValues[chromsomeFinal[i]-1]+=1
    for j in range(len(seenValues)):
        if(len(indexDuplicate)<=0):
            break
        if(seenValues[j]==0):
            chromsomeFinal[indexDuplicate.pop()] = j+1     
    return chromsomeFinal


#Entrada:
#- chromosomeFinal->Es el hijo (array de tamaño table_size con los valores de las posiciones de table_size reinas) obtenido a partir de dos padres
#- table_size->tamaño del tablero de ajedrez (tambien indica cuantas reinas deben haber por filas)
#- mutation_prob->la probabilidad de mutacion en un hijo
#Salida:
#Retorna el hijo obtenido de dos padres con una mutacion, siempre y cuando de la posibilidad de hacerlo, con una probablidad de cross_mutation
#Si no esta dentro de la probabilidad, entonces no muta y retorna el hijo tal cual como se recibio
def mutation(chromsomeFinal, cross_mutation, table_size):
    randomNumber = np.random.random()
    if(randomNumber <= cross_mutation):
        randomIndex2 = np.random.randint(1,table_size-1)
        randomIndex = np.random.randint(1, table_size-1)
        value = chromsomeFinal[randomIndex]
        chromsomeFinal[randomIndex] = chromsomeFinal[randomIndex2]
        chromsomeFinal[randomIndex2] = value
    return chromsomeFinal