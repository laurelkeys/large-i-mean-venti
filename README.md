
<!-- -->
# genetic-algorithms

## to_be_or_not_to_be[.py](https://github.com/laurelkeys/large-i-mean-venti/blob/master/genetic-algorithms/to_be_or_not_to_be.py)

A genetic algorithm to find the phrase "*To be or not to be.*" in a pool of random strings.
Based on Daniel Shiffman's "The **Nature** of Code", [chapter 9](https://natureofcode.com/book/chapter-9-the-evolution-of-code/).

### Example usage
```
>>> python to_be_or_not_to_be.py
```
[![Image from Gyazo](https://i.gyazo.com/992ad6d9a4d433988d85b437e5d67032.gif)](https://gyazo.com/992ad6d9a4d433988d85b437e5d67032)

<!-- -->
# swarm-intelligence

## particle_swarm[.py](https://github.com/laurelkeys/large-i-mean-venti/blob/master/swarm-intelligence/particle_swarm.py)

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

## honeybee_swarm[.py](https://github.com/laurelkeys/large-i-mean-venti/blob/master/swarm-intelligence/honeybee_swarm.py)

A simple implementation of Artificial Bee Colony ([ABC](http://www.scholarpedia.org/article/Artificial_bee_colony_algorithm)), a numerical optimization meta-heuristic.

### The Hive problem model class
**Arguments**
```
lower_bound: Variable's domain lower bound
upper_bound: Variable's domain upper bound
swarm_size: Total number of bees
max_cycles: Maximum number of cycles before halting
objective_func: Objective function
objective_value: Objective function's target value
max_unimproved_trials: Maximum number of cycles a bee can exploit it's "food source" 
                       before becoming a scout bee
```

### Example usage
**Model**
```python
target = "supercalifragilistic"
def poppins(vector):
    score = 0
    for gene, target_char in zip(vector, target):
        if gene == ord(target_char):
            score += 1
    return score

model = Hive(lower_bound=[ord('a')]*dim, 
             upper_bound=[ord('z')]*dim, 
             swarm_size=100,  
             max_cycles=3000, 
             objective_func=poppins,
             objective_value=len(target))
```

**Execution**
```
>>> python honeybee_swarm.py
 @cycle  100: best = sdpurkajifnagcliqtia
 @cycle  200: best = sdpercalifnagcliqtia
 @cycle  300: best = sdpercalifnagclistia
 @cycle  400: best = sudercalifragicistic
 @cycle  500: best = sudercalifragicistic
 @cycle  600: best = sudercalifragicistic
 @cycle  700: best = sudercalifragicistic
 @cycle  800: best = sudercalifragicistic
 @cycle  900: best = sudercalifragicistic
 @cycle 1000: best = supercalefragilistic
 @cycle 1006: best = supercalifragilistic
 value    : 20
 solution : ['s','u','p','e','r','c','a','l','i','f','r','a','g','i','l','i','s','t','i','c']
```

