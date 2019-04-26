# ref.: "A modified Artificial Bee Colony algorithm for real-parameter optimization" article,  
#       and Algorithm 2 of https://abc.erciyes.edu.tr/pub/NevImpOfABC.pdf

from math import floor

import copy
import random
import numpy as np

class Honeybee:
    def __init__(self, lower_bound, upper_bound, objective_func):
        assert(len(lower_bound) == len(upper_bound))

        self.solution = list() # genome
        for min, max in zip(lower_bound, upper_bound):
            self.solution.append(min + random.random()*(max - min))
        
        self.objective_func = objective_func
        self.unimproved_trials = 0 # once this reaches the limit it becomes a scout bee (abandonment criteria)
    
    def get_value(self):
        # objective function value (solution cost)
        return self.objective_func(self.solution) # phenotype
    
    def get_fitness(self):
        # considers a minimization problem (the value itself could be used on a maximization problem)
        value = self.get_value()
        if value >= 0:
            return 1 / (1 + value)
        else:
            return 1 + abs(value)
    
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
                 swarm_size=20, max_cycles=200, max_unimproved_trials=4,
                 initial_number_of_scouts=1, initial_percentage_of_employees=0.5):

        assert(len(lower_bound) == len(upper_bound))
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.objective_func = objective_func

        self.swarm_size = swarm_size
        self.number_of_scouts = initial_number_of_scouts
        self.number_of_employees = int(initial_percentage_of_employees * self.swarm_size)
        self.number_of_onlookers = self.swarm_size - self.number_of_employees - self.number_of_scouts
        # assert(self.number_of_scouts + self.number_of_employees + self.number_of_onlookers == self.swarm_size)

        self.dim = len(lower_bound) # problem dimension
        self.cycle = 0
        self.max_cycles = max_cycles
        self.max_unimproved_trials = max_unimproved_trials # self.dim * self.number_of_onlookers

        self.best = None # best solution found so far
        self.best_fitness = float('inf') # best solution's fitness value

        self.swarm = [Honeybee(lower_bound, upper_bound, objective_func) for _ in range(self.swarm_size)]
        self.evaluate() # find the best (most fit) honeybee
    
    def solve(self):
        self.cycle = 1
        while self.cycle < self.max_cycles:
            # employed bees phase
            for honeybee_index in range(self.swarm_size):
                self.send_employee(honeybee_index)
            self.evaluate() # memorizes the best solution achieved so far
            # scout bees phase
            # TODO

    def evaluate(self):
        for i in range(self.swarm_size):
            fitness = self.swarm[i].get_fitness()
            if fitness < self.best_fitness:
                self.best = copy.deepcopy(self.swarm[i])
                self.best_fitness = fitness

    def calculate_probabilities(self):
        # TODO use the fitness_func if it's not None
        
        # calculates the probability of selection of each honeybee based on roulette wheel selection
        fitness_sum = sum([honeybee.fitness for honeybee in self.swarm])
        self.selection_probability = [honeybee.fitness / fitness_sum for honeybee in self.swarm]

        return [sum(self.selection_probability[:x+1]) for x in range(self.swarm)] # probability intervals (TODO assert the last value equals 1)
    
    def send_employee(self, honeybee_index):
        neighboor = copy.deepcopy(self.swarm[honeybee_index])
        
        potential_partners_index = [i for i in range(self.swarm_size) if i != honeybee_index]
        neighboor.mutate_locally_with_crossover(locus=random.randint(0, self.dim-1), 
                                                partner=random.choice(potential_partners_index), 
                                                locus_lower_bound=self.lower_bound[honeybee_index], 
                                                locus_upper_bound=self.upper_bound[honeybee_index])
        
        # neighboor.calculate_value()
        neighboor.calculate_fitness()
        
        if neighboor.fitness > self.swarm[honeybee_index].fitness: # FIXME check this comparison
            self.swarm[honeybee_index] = copy.deepcopy(neighboor)
            self.swarm[honeybee_index].unimproved_trials = 0
        else:
            self.swarm[honeybee_index].unimproved_trials += 1