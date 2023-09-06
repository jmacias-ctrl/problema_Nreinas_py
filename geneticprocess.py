import numpy as np
from numpy import random
import math
import sys
import random as rng
from roulette import *

def initiate_population(seed, population_size, table_size):
    
    population = np.zeros(shape=(population_size, table_size), dtype=int)
    for i in range(population_size):
        setRng = np.random.default_rng(seed+i)
        x = np.arange(1, table_size+1)
        setRng.shuffle(x)
        population[i] = x
    return population

def calculate_fitness(population, population_size, table_size):
    fitness = np.zeros(population_size, dtype=int)
    totalFitness = 0
    pos=0
    for gen in population:
        #print("gen: ", gen)
        set_fitness = 0
        for i in range(table_size):
            queenPosX = gen[i]
            #print("Original Queen Pos X: "+ str(queenPosX), "i=", i)
            j = i+1
            iteration = 1
            colision = 0
            #print("checking right side")
            while j < table_size:
                queenPosY = gen[j]
                l_x = queenPosX - iteration
                r_x = queenPosX + iteration
                #print("j=",j,",Queen Pos Y: ", queenPosY, ",Queen Pos X-iteration: ",  queenPosX-iteration,",Queen Pos X+iteration: ",  queenPosX+iteration, ",queenPosY == queenPosX+iteration: o  queenPosY == queenPosX-iteration:", (queenPosY == r_x) or (queenPosY == l_x))
                if((queenPosY == l_x) or (queenPosY == r_x)):
                    set_fitness+=1
                    colision+=1
                j+=1
                iteration+=1
                
            j = i-1
            iteration = 1
            #print("checking left side")
            while j>=0:
                #print("j=",j,",Queen Pos Y: ", queenPosX+iteration, ",Queen Pos X-iteration: ",  queenPosX-iteration,",queenPosY == queenPosX+iteration o  queenPosY == queenPosX-iteration:", queenPosY == r_x or queenPosY == l_x)
                queenPosY = gen[j]
                l_x = queenPosX - iteration
                r_x = queenPosX + iteration
                if((queenPosY == l_x) or (queenPosY == r_x)):
                    set_fitness+=1
                    colision+=1
                iteration+=1
                j-=1
            #print("Colisiones:", colision)
            #print()
        fitness[pos] = set_fitness
        totalFitness+=set_fitness
        #print("fitness", set_fitness)
        pos+=1
    return fitness, totalFitness
    
def set_new_populatiopn(population, population_size, fitness, table_size, cross_prob, total_fitness, mutation_prob):
    new_population = np.zeros(shape=(population_size, table_size), dtype=int)
    i = 0
    while(i<population_size):
        cross_indv1, cross_indv2 = roulette(population_size,fitness,total_fitness)
        rng.seed(datetime.now().timestamp())
        randomNumber = rng.uniform(0,1)
        if(randomNumber<=cross_prob):
            newIndividual = gen_cross(population, mutation_prob, table_size,cross_indv1,cross_indv2)
            new_population[i] = newIndividual
            i+=1
    return new_population

def gen_cross(population, cross_mutation, table_size, indexInd1, indexInd2):
    indices = int(table_size/2)+1
    genF1, genF2 = population[indexInd1][:indices], population[indexInd2][:table_size-indices]
    genS = mutation(np.append(genF1,genF2), cross_mutation, table_size)
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
    rng.seed(datetime.now().timestamp())
    randomNumber = rng.uniform(0,1)
    if(randomNumber <= cross_mutation):
        randomIndex2 = rng.randint(1,table_size-1)
        rng.seed(datetime.now().timestamp())
        randomIndex = rng.randint(1, table_size-1)
        genS[randomIndex] = genS[randomIndex2]
    return genS