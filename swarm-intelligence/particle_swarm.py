# note: this is a numerical optimization heuristic
# ref.: James McCaffrey: Swarm Intelligence Optimization using Python

'''Minimization of the Rastrigin function using particle swarm optimization (PSO)'''

import random
import math
from copy import copy

def error(position):
    err = 0.0
    for i in range(len(position)):
        xi = position[i]
        err += (xi * xi) - (10 * math.cos(2 * math.pi * xi)) + 10
    return err

class Particle:
    def __init__(self, dim, min_x, max_x, seed):
        '''Parameters
            dim : int
                Rastrigin function's dimension (i.e. the number of x_i variables, i ∈ [1, dim])
            min_x : int
                Minimum x_i value (x_i ∈ [min_x, max_x])
            max_x : int
                Maximum x_i value (x_i ∈ [min_x, max_x])
            seed : int
                Random seed
        '''
        rand = random.Random(seed)
        self.position = [0.0] * dim
        self.velocity = [0.0] * dim
        for i in range(dim):
            self.position[i] = ((max_x - min_x) * rand.random() + min_x)
            self.velocity[i] = ((max_x - min_x) * rand.random() + min_x)

        self.error = error(self.position) # current error
        
        self.best_pos = copy(self.position) # particle's best reached position
        self.best_err = self.error               # particle's best reached error

def Solve(max_epochs, n, dim, min_x, max_x, seed=0):
    '''Parameters
        max_epochs : int
            Epochs limit (halts when reached)
        n : int
            Number of particles (population size)
        dim : int
            Rastrigin function's dimension (i.e. the number of x_i variables, i ∈ [1, dim])
        min_x : int
            Minimum x_i value (x_i ∈ [min_x, max_x])
        max_x : int
            Maximum x_i value (x_i ∈ [min_x, max_x])
        seed : int
            Random seed
    '''
    rand = random.Random(seed) # TODO change this seed for different results

    swarm = [Particle(dim, min_x, max_x, seed = i) for i in range(n)] # creates n random particles

    swarm_best_pos = [0.0] * dim
    swarm_best_err = float('inf')
    for i in range(n): # check each particle
        if swarm[i].error < swarm_best_err:
            swarm_best_err = swarm[i].error
            swarm_best_pos = copy(swarm[i].position)

    # TODO play with the following values for different results
    w  = 0.729   # inertia
    c1 = 1.49445 # cognitive (particle)
    c2 = 1.49445 # social (swarm)

    epoch = 0
    while epoch < max_epochs:    
        if epoch % 10 == 0 and epoch > 1:
            print(f'Epoch = {epoch} best error = {swarm_best_err:.3f}')
            
        # process each particle
        for i in range(n):
            # compute the current particle's new velocity
            for k in range(dim):
                swarm[i].velocity[k] = (
                    (w  * swarm[i].velocity[k]) +                                           # towards curr direction
                    (c1 * rand.random() * (swarm[i].best_pos[k] - swarm[i].position[k])) +  # towards self best
                    (c2 * rand.random() * (swarm_best_pos[k]    - swarm[i].position[k]))    # towards swarm best
                )
                if swarm[i].velocity[k] < min_x:
                    swarm[i].velocity[k] = min_x
                elif swarm[i].velocity[k] > max_x:
                    swarm[i].velocity[k] = max_x

            # compute the current particle's new position using it's new velocity
            for k in range(dim): 
                swarm[i].position[k] += swarm[i].velocity[k]
    
            # compute the error of the new position
            swarm[i].error = error(swarm[i].position)

            # is the new position a new best for the particle?
            if swarm[i].error < swarm[i].best_err:
                swarm[i].best_err = swarm[i].error
                swarm[i].best_pos = copy(swarm[i].position)

            # is the new position a new best overall?
            if swarm[i].error < swarm_best_err:
                swarm_best_err = swarm[i].error
                swarm_best_pos = copy(swarm[i].position)
    
        epoch += 1

    return swarm_best_pos

dim = 3
print(f'Solving Rastrigin\'s function in {dim} variables (known min = 0.0 at ({(dim - 1) * "0, "}0))')

# TODO play with the following values for different results
num_particles = 50
max_epochs    = 100
min_x, max_x  = -10.0, 10.0
print(f'Setting num_particles  = {num_particles}')
print(f'        max_epochs     = {max_epochs}')
print(f'        [min_x, max_x] = [{min_x}, {max_x}]\n')

best_position = Solve(max_epochs, num_particles, dim, min_x, max_x) # TODO set Solve's seed for different results

print(f'\nBest solution found: \n {" ".join(map(lambda i: f"{i:.4f}", best_position))}')
print(f'Error of best solution = {error(best_position):.6f}')