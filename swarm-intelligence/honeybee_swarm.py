# ref.: "A modified Artificial Bee Colony algorithm for real-parameter optimization" article

from math import floor

import copy
import math
import random
import numpy as np

class Honeybee:
    def __init__(self, lower_bound, upper_bound, objective_func):
        self.solution = list() # genome
        for min, max in zip(lower_bound, upper_bound):
            self.solution.append(min + random.random()*(max - min))
        
        self.objective_func = objective_func
        self.unimproved_trials = 0 # once this reaches the limit it becomes a scout bee (abandonment criteria)
    
    def get_value(self):
        # objective function value (solution cost)
        return self.objective_func(self.solution) # phenotype
    
    def get_fitness(self):
        # TODO test other fitness functions
        return self.get_value()
    
    def mutate(self, locus, partner, locus_lower_bound, locus_upper_bound):
        # the locus is the solution's dimension that will be crossed-over and mutated (i.e. the mutated gene index)
        mutated_gene = self.solution[locus] + random.uniform(-1, 1) * (self.solution[locus] - partner.solution[locus])
        if mutated_gene < locus_lower_bound:
            self.solution[locus] = locus_lower_bound
        elif mutated_gene > locus_upper_bound:
            self.solution[locus] = locus_upper_bound
        else:
            self.solution[locus] = mutated_gene

class Hive:
    def __init__(self, lower_bound, upper_bound, objective_func, 
                 swarm_size=20, max_cycles=200, max_unimproved_trials=None):
        assert(len(lower_bound) == len(upper_bound))

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.objective_func = objective_func

        self.swarm_size = swarm_size

        self.dim = len(lower_bound) # problem dimension
        self.cycle = 0
        self.max_cycles = max_cycles
        self.max_unimproved_trials = max_unimproved_trials if max_unimproved_trials != None else 0.5 * self.swarm_size * self.dim

        self.best = None # best solution found so far
        self.best_fitness = float('inf') # best solution's fitness value (NOTE considers a minimization problem)

        self.swarm = [Honeybee(self.lower_bound, self.upper_bound, self.objective_func) for _ in range(self.swarm_size)]
        self.evaluate() # find the best (most fit) honeybee
    
    def solve(self):
        self.cycle = 1
        while self.cycle <= self.max_cycles:
            self.send_employees()

            self.calculate_probabilities()
            self.send_onlookers()
            
            self.send_scouts()
            
            self.evaluate() # memorize the best solution achieved so far
            self.cycle += 1
        
        return self.best

    def evaluate(self):
        for i in range(self.swarm_size):
            fitness = self.swarm[i].get_fitness()
            if fitness < self.best_fitness:
                self.best = copy.deepcopy(self.swarm[i])
                self.best_fitness = fitness

    def calculate_probabilities(self):
        # calculates the probability of selection of each honeybee based on roulette wheel selection
        fitness = [honeybee.get_fitness() for honeybee in self.swarm]
        fitness_sum = sum(fitness)
        self.selection_probability = [fitness[i] / fitness_sum if fitness_sum != 0 else 1.0 for i in range(self.swarm_size)]
    
    def explore(self, honeybee_index):
        neighboor = copy.deepcopy(self.swarm[honeybee_index])
        
        locus = random.randint(0, self.dim-1)
        potential_partners_index = [i for i in range(self.swarm_size) if i != honeybee_index]
        neighboor.mutate(locus=locus, 
                         partner=self.swarm[random.choice(potential_partners_index)], 
                         locus_lower_bound=self.lower_bound[locus], 
                         locus_upper_bound=self.upper_bound[locus])
        
        fitness = neighboor.get_fitness()
        if fitness < self.swarm[honeybee_index].get_fitness(): # NOTE considers a minimization problem (and the fitness is the objective function)
            self.swarm[honeybee_index] = copy.deepcopy(neighboor)
            self.swarm[honeybee_index].unimproved_trials = 0
        else:
            self.swarm[honeybee_index].unimproved_trials += 1

    def send_employees(self):
        for honeybee_index in range(self.swarm_size):
            self.explore(honeybee_index)
    
    def send_onlookers(self):
        honeybee_index = 0
        number_of_onlookers = 0
        while number_of_onlookers < self.swarm_size:
            if random.random() < self.selection_probability[honeybee_index]:
                number_of_onlookers += 1
                self.explore(honeybee_index)
            honeybee_index = (honeybee_index + 1) % self.swarm_size

    def send_scouts(self):
        for honeybee_index in range(self.swarm_size):
            if self.swarm[honeybee_index].unimproved_trials >= self.max_unimproved_trials:
                self.swarm[honeybee_index] = Honeybee(self.lower_bound, self.upper_bound, self.objective_func)

# ______________________________________________________________________________

def rastrigin(vector):
    err = 0.0
    for i in range(len(vector)):
        xi = vector[i]
        err += (xi * xi) - (10 * math.cos(2 * math.pi * xi)) + 10
    return err

dim = 3
swarm_size = 20
max_cycles = 200
max_unimproved_trials = 0.5 * swarm_size * dim
model = Hive(lower_bound=[-5.12]*dim, 
             upper_bound=[5.12]*dim, 
             objective_func=rastrigin, 
             swarm_size=swarm_size, 
             max_cycles=max_cycles, 
             max_unimproved_trials=max_unimproved_trials)
solution = model.solve()
print(f"value    : {solution.get_value()}")
print(f"solution : {solution.solution}")
