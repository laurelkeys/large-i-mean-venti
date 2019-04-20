# swarm-intelligence

## [particle_swarm.py](https://github.com/laurelkeys/large-i-mean-venti/blob/master/swarm-intelligence/particle_swarm.py "particle_swarm.py")

A simple implementation of Particle Swarm Optimization ([PSO](https://en.wikipedia.org/wiki/Particle_swarm_optimization)) for minimizing the [Rastrigin function](https://en.wikipedia.org/wiki/Rastrigin_function).

Heavily based on James McCaffrey's [talk](https://www.youtube.com/watch?v=bVDX_UwthZI).

### Example usage
```
>>> python particle_swarm.py
 Solving Rastrigin's function in 3 variables (known min = 0.0 at (0, 0, 0))
 Setting num_particles  = 50
         max_epochs     = 100
        [min_x, max_x]  = [-10.0, 10.0]

 Epoch = 10, best error = 6.569
 Epoch = 20, best error = 5.884
 Epoch = 30, best error = 2.446
 Epoch = 40, best error = 1.851
 Epoch = 50, best error = 1.239
 Epoch = 60, best error = 0.159
 Epoch = 70, best error = 0.042
 Epoch = 80, best error = 0.002
 Epoch = 90, best error = 0.000

 Best solution found:
  0.0003 0.0007 0.0002
 Error of best solution = 0.000111
```
