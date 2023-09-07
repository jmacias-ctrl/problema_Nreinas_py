import numpy as np
from numpy import random
import math
import sys
import random as rng
from roulette import *

def setSeed(getSeed):
    np.random.seed(getSeed)

def initiate_population(seed, population_size, table_size):
    population = np.zeros(shape=(population_size, table_size), dtype=int)
    for i in range(population_size):
        x = np.arange(1, table_size+1)
        np.random.shuffle(x)
        population[i] = x
    return population

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
    
def set_new_populatiopn(population, population_size, fitness, table_size, cross_prob, total_fitness, mutation_prob):
    new_population = np.zeros(shape=(population_size, table_size), dtype=int)
    i = 0
    while(i<population_size):
        cross_indv1, cross_indv2 = roulette(population_size,fitness,total_fitness)
        randomNumber = np.random.random()
        if(randomNumber<=cross_prob):
            newIndividual = gen_cross(population, mutation_prob, table_size,cross_indv1,cross_indv2)
            new_population[i] = newIndividual
            i+=1
    new_fitness, total_fitnes= calculate_fitness(new_population, population_size, table_size)
    atFitness = np.append(new_fitness,fitness)
    atPopulation = np.concatenate((new_population, population))
    best_fitness = np.argsort(atFitness)
    best_individuals = np.zeros(shape=(population_size, table_size), dtype=int)
    for i in range(population_size):
        best_individuals[i] = atPopulation[best_fitness[i]]
    return best_individuals

def gen_cross(population, cross_mutation, table_size, indexInd1, indexInd2):
    indices = np.random.randint(2, table_size)
    rngSplit = np.random.random()
    if(rngSplit>=0.6):
        genF1, genF2 = population[indexInd1][:indices], population[indexInd2][indices:]
    else:
        genF1, genF2 = population[indexInd2][:indices], population[indexInd1][indices:]
    genS = gen_cross_correction(np.concatenate((genF2,genF1)), table_size)
    return mutation(genS, cross_mutation, table_size)
    
def gen_cross_correction(genS, table_size):
    seenValues = np.zeros(table_size, dtype=int)
    indexDuplicate = []
    for i in range(len(genS)):
        if(seenValues[genS[i]-1]>0):
            indexDuplicate.append(i)
        else:
            seenValues[genS[i]-1]+=1
    for j in range(len(seenValues)):
        if(len(indexDuplicate)<=0):
            break
        if(seenValues[j]==0):
            genS[indexDuplicate.pop()] = j+1     
    return genS

def mutation(genS, cross_mutation, table_size):
    randomNumber = np.random.random()
    if(randomNumber <= cross_mutation):
        randomIndex2 = np.random.randint(1,table_size-1)
        randomIndex = np.random.randint(1, table_size-1)
        value = genS[randomIndex]
        genS[randomIndex] = genS[randomIndex2]
        genS[randomIndex2] = value
    return genS