import numpy as np
from random import random, shuffle
from numpy.random import randint
from copy import copy


#######################################################################
class Chromosome:
    def __init__(self, n) -> None:
        self.n = n
        self.genes = [] #list of cities in order to be visited
        #all n genes in the chromosome must be unique #no repitition


    #print(chromosome) --> print the genes list
    def __repr__(self) -> str:
        return ''.join(str(gene) for gene in self.genes)



################################################################################################
class GeneticAlgorithm:
    def __init__(self, tsp, epochs, n,  pop_size, elitism_rate ,tournament_size, crossover_rate ,mutation_rate) -> None:
        self.tsp = tsp 
        self.epochs = epochs 

        self.n = n
        self.pop_size = pop_size #same for all generations
        self.population = [] #list of individuals in the pop

        self.N = elitism_rate
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        #randomly initialise the 0th generation 
        #sample chromosome
        sample = tsp.cities

        #each individual of the pop will be shuffled version of sample
        for _ in range(0, pop_size) :
            individual = Chromosome(self.n)

            shuffle(sample)
            individual.genes = copy(sample)  

            self.population.append(individual)



    #fitness function
    def fitness(self, genes) :
        cost = self.tsp.cost(genes)

        #high cost = low fitness
        return -1*cost



    #return the fittest individual in the population
    def get_fittest(self, pop) :
        fittest = pop[0]
        max = self.fitness(fittest.genes) #max fitness found yet

        for individual in pop :
            route = individual.genes
            fitness = self.fitness(route)
            if fitness > max:
                #this is the fittest chromosome yet
                fittest = individual
                max = fitness

        return fittest



    #the actual algorithm
    def run(self):
        pop = self.population
        gen = 0 #generation number

        best = self.get_fittest(pop).genes #the best state found yet
        max_fitness = self.fitness(best) #best fitness value found yet

        #while all possible states are not explored
        for _ in range(self.epochs):
            ##### selection and crossover #######
            next_gen = [] #list of individuals in next gen

            #elitism : top N fittest individuals of the pop are directly passed down to the next gen
            elite = self.elitism(pop, self.N)
            next_gen.extend(elite)

            #select parents through tournament method and perform crossover
            tourn_size = self.tournament_size
            for i in range(0, self.pop_size - self.N):
                p1 = self.tournament(tourn_size, pop)
                child = self.crossover(p1)

                #mutate the child
                self.mutate(child)

                #add child to next gen's population
                next_gen.append(child) 

            #is the fittest of this new gen the best state yet?
            fittest = self.get_fittest(next_gen).genes
            if self.fitness(fittest) > max_fitness:
                best = fittest
                max_fitness = self.fitness(best)

            #next gen becomes the population
            pop = next_gen
            gen += 1
        #training over

        print("Total distance of this route is ", self.tsp.cost(best) )
        self.tsp.display(best)
        


    #return the top N fittest individuals in the pop
    def elitism(self,pop, N):
        population = copy(pop)

        #sort population in decreasing order of fitness
        population.sort(key = lambda individual : self.fitness(individual.genes), reverse = True)

        #return first N elements
        return population[:N]



    #selection (tournament method)
        #tournament size = number of participants
    def tournament(self, tournament_size, pop):
        participants = [] 
        
        #select the particpants randomly from the population
        for _ in range(0, tournament_size):
            i = randint(self.pop_size)
            participants.append( pop[i] )

        #return the fittest participant
        return self.get_fittest(participants)



    #crossover  (1 parent 1 child approach)
    def crossover(self, p1):
        child = Chromosome(p1.n)
        prob = self.crossover_rate
        if random() < prob:
            #for two random indexes i1 and i2
            #reverse order of all elements btw i1 and i2

            i1 = randint(0,self.n)
            i2 = randint(0,self.n)

            if i1>i2:
                #exchange
                i1,i2 = i2, i1

            child.genes.extend(p1.genes[:i1])
            rem = copy(p1.genes[i1:i2])
            rem.reverse()
            child.genes.extend(rem)
            child.genes.extend(p1.genes[i2:])

            return child
        
        return p1
    


    #mutation
    #swap the genes at 2 random indexes
    def mutate(self, chromosome):
        #change the gene mutation_rate% of times
        if random() < self.mutation_rate :
            i1 = randint(0,self.n)
            i2 = randint(0,self.n)
            chromosome.genes[i1] , chromosome.genes[i2] = chromosome.genes[i2] , chromosome.genes[i1]
