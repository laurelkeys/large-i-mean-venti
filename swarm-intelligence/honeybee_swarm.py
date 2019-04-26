# ref.: "A modified Artificial Bee Colony algorithm for real-parameter optimization" article

from math import floor

import copy
import random
import numpy as np

infinity = float('inf')

# maps a value v from [low1, high1] to a value in [low2, high2]
bound = lambda v, low1, high1, low2, high2: (v - low1) * ((high2-low2) / (high1-low1)) + low2

class Honeybee:
    def __init__(self, lower_bound, upper_bound, objective_func, fitness_func=None):
        assert(len(lower_bound) == len(upper_bound))

        self.solution = list() # genome
        for min, max in zip(lower_bound, upper_bound):
            self.solution.append(min + random.random()*(max - min))
        
        self.objective_func = objective_func
        self.value = self.objective_func(self.solution) # objective function value for the solution
        
        self.fitness_func = (fitness_func if fitness_func != None else
            lambda x: 1 / (1 + x.value) if x.value >= 0 else 1 + abs(x.value))
        self.calculate_fitness()

        self.unimproved_trials = 0 # once this reaches the limit it becomes a scout bee (abandonment criteria)
    
    def calculate_fitness(self):
        self.fitness = self.fitness_func(self.solution)
    
    def mutate_locally_with_crossover(self, locus, partner, locus_lower_bound, locus_upper_bound):
        # the locus is the solution's dimension that will be crossed-over and mutated (i.e. the mutated gene index)
        mutated_gene = self.solution[locus] + random.uniform(-1, 1) * (self.solution[locus] - partner.solution[locus])

        if mutated_gene < locus_lower_bound:
            self.solution[locus] = locus_lower_bound
        elif mutated_gene > locus_upper_bound:
            self.solution[locus] = locus_upper_bound
        else:
            self.solution[locus] = mutated_gene


class Hive:
    def __init__(self, lower_bound, upper_bound, objective_func, fitness_func=None,
                 selection_func=None, swarm_size=20, max_cycles=200, max_unimproved_trials=None,
                 initial_number_of_scouts=1, initial_percentage_of_employees=0.5):

        assert(len(lower_bound) == len(upper_bound))
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.objective_func = objective_func

        self.fitness_func = fitness_func # FIXME test if None
        self.selection_func = selection_func # FIXME test if None

        self.swarm_size = swarm_size
        self.number_of_scouts = initial_number_of_scouts
        self.number_of_employees = int(initial_percentage_of_employees * self.swarm_size)
        self.number_of_onlookers = self.swarm_size - self.number_of_employees - self.number_of_scouts
        # assert(self.number_of_scouts + self.number_of_employees + self.number_of_onlookers == self.swarm_size)

        self.max_cycles = max_cycles

        self.dim = len(lower_bound) # problem dimension
        self.max_unimproved_trials = self.dim * self.number_of_onlookers if max_unimproved_trials == None else max_unimproved_trials

        self.best = infinity # fitness value of the best solution found (NOTE considers a minimization problem)
        self.best_solution = None # best solution found

        self.swarm = [Honeybee(lower_bound, upper_bound, objective_func, fitness_func) for _ in range(self.swarm_size)]
        self.evaluate() # find the best (most fit) honeybee
        # self.calculate_probabilities()

    def evaluate(self):
        current_best_index, current_best = min(enumerate([honeybee.fitness for honeybee in self.swarm]), key=lambda t: t[1]) # TODO test this
        if current_best < self.best:
            self.best = current_best
            self.best_solution = self.swarm[current_best_index].solution # TODO check if copy() is needed

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
        
        neighboor.value = self.objective_func(neighboor.solution) # neighboor.objective_func(neighboor.solution)
        neighboor.calculate_fitness()
        
        if neighboor.fitness > self.swarm[honeybee_index].fitness:
            self.swarm[honeybee_index] = copy.deepcopy(neighboor)
            self.swarm[honeybee_index].unimproved_trials = 0
        else:
            self.swarm[honeybee_index].unimproved_trials += 1