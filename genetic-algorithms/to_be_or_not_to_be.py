# ref.: Daniel Shiffman's "The Nature of Code" book, Chapter 9

'''Finding the "To be or not to be." string through evolution'''

import random
from math import floor

from os import system, name
# clears the console
def clear():
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')  

# maps a value v from [low1, high1] to a value in [low2, high2]
def bound(v, low1, high1, low2, high2):
    return (v - low1) * ((high2-low2) / (high1-low1)) + low2

# ______________________________________________________________________________
class DNA:
    def __init__(self, length):
        self.char_codes = [ord(' '), ord('.')] + list(range(ord('A'), ord('Z') + 1)) + list(range(ord('a'), ord('z') + 1))
        self.fitness = 0
        self.length = length
        self.genes = [chr(random.choice(self.char_codes)) for _ in range(self.length)]
    
    def get_phrase(self):
        return ''.join(self.genes)
    
    def calculate_fitness(self, target):
        score = 0
        for gene, target_char in zip(self.genes, target):
            if gene == target_char:
                score += 1
        self.fitness = score / len(target)
    
    def crossover(self, partner):
        child = DNA(len(self.genes))
        
        # selects a "midpoint" and gets half of self's genes and half of partner's
        midpoint = random.randint(0, self.length - 1)
        for i in range(self.length):
            child.genes[i] = self.genes[i] if i < midpoint else partner.genes[i]
        
        return child
    
    def mutate(self, mutation_rate):
        for i in range(self.length):
            if (random.random() < mutation_rate):
                self.genes[i] = chr(random.choice(self.char_codes))

# ______________________________________________________________________________
class Population:
    def __init__(self, target, population_size, mutation_rate):
        self.target = target
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.population = [DNA(len(self.target)) for _ in range(self.population_size)]
        
        self.mating_pool = list() # individuals added proportionally to it's fitness
        self.generation = 0
        self.best = ""
        self.perfect_score = 1

        self.finished = False
        self.calculate_fitness()
    
    def calculate_fitness(self):
        for individual in self.population:
            individual.calculate_fitness(self.target)
    
    # makes a new mating pool
    def natural_selection(self):
        self.mating_pool = list() # clears the pool
        max_fitness = max(map(lambda individual: individual.fitness, self.population))
        for individual in self.population:
            n = floor(bound(individual.fitness, 0, max_fitness, 0, 100)) # number of times to add it on the mating pool
            for _ in range(n):
                self.mating_pool.append(individual)
    
    # creates a new generation
    def generate(self):
        for i in range(self.population_size):
            partner1 = random.choice(self.mating_pool)
            partner2 = random.choice(self.mating_pool)
            
            child = partner1.crossover(partner2)
            child.mutate(self.mutation_rate)
            self.population[i] = child
        
        self.generation += 1
    
    # compute the current "most fit" member of the population
    def evaluate(self):
        best_fitness = - float('inf')
        best_fit_individual_index = 0
        for i in range(self.population_size):
            if self.population[i].fitness > best_fitness:
                best_fitness = self.population[i].fitness
                best_fit_individual_index = i
        
        self.best = self.population[best_fit_individual_index].get_phrase()
        if best_fitness == self.perfect_score:
            self.finished = True
    
    def is_finished(self):
        return self.finished
    
    def get_best(self):
        return self.best
    
    def get_generation(self):
        return self.generation
    
    def get_average_fitness(self):
        return sum(map(lambda individual: individual.fitness, self.population)) / self.population_size
    
    def get_phrases(self, limit=50):
        phrases = ""
        limit = min(self.population_size, limit)
        for i in range(limit):
            phrases += self.population[i].get_phrase() + "\n"
        return phrases

# ______________________________________________________________________________
# TODO play with the following values for different results
target_phrase   = "To be or not to be." # (changing this may require adding new values to Population's char_codes)
population_size = 500
mutation_rate   = 0.008

population = Population(target_phrase, population_size, mutation_rate)

while not population.is_finished():
    population.natural_selection() # makes a new mating pool
    population.generate() # creates the next generation
    population.calculate_fitness()

    population.evaluate()
    display_info = f"population size:   {population_size}\n" + \
                   f"mutation rate:     {mutation_rate * 100}%\n" + \
                   f"total generations: {population.get_generation()}\n" + \
                   f"average fitness:   {population.get_average_fitness():.4f}\n" + \
                   f"Best phrase: \n {population.get_best()}\n"

    clear()
    print(display_info)