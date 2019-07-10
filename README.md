
# Topics

> - [clustering](#clustering)
> - [computer-graphics](#computer-graphics)
> - [genetic-algorithms](#genetic-algorithms)
> - [procedural-generation](#procedural-generation)
> - [simulation](#simulation)
> - [swarm-intelligence](#swarm-intelligence)

<!-- -->
# clustering
## k_means[.py](https://github.com/laurelkeys/large-i-mean-venti/blob/master/clustering/k_means.py)
Image color clustering into k groups using the [k-means](https://en.wikipedia.org/wiki/K-means_clustering) method and pixel color visualization on 3D space (where x=R, y=G and z=B).

### Example usage
```
>>> python k_means.py i\mondrian.jpg 5 o\
 (normalize) Δt: 0.0010 seconds
 (cluster) Δt: 0.4169 seconds
 Image saved to o\mondrian5.jpg
```

**Original image**         |  **Result image (with k=5)** 
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/laurelkeys/large-i-mean-venti/master/clustering/i/mondrian.jpg)  |  ![](https://raw.githubusercontent.com/laurelkeys/large-i-mean-venti/master/clustering/o/mondrian5.jpg)

**Result image color palette**

![](https://raw.githubusercontent.com/laurelkeys/large-i-mean-venti/master/clustering/o/mondrian5_histogram.png)

**Pixels with original color**         |  **Pixels grouped into k=5 clusters** 
:-------------------------:|:-------------------------:
<img src="https://raw.githubusercontent.com/laurelkeys/large-i-mean-venti/master/clustering/o/mondrian_plot.png" width="500"/>  |  <img src="https://raw.githubusercontent.com/laurelkeys/large-i-mean-venti/master/clustering/o/mondrian5_clusters.png" width="500"/>

<!-- -->
# computer-graphics
## halftone[/](https://github.com/laurelkeys/large-i-mean-venti/tree/master/computer-graphics/halftone)
Halftone images made with boxes on a 3D plane using orthographic projection, in both [Processing](https://github.com/laurelkeys/large-i-mean-venti/tree/master/computer-graphics/halftone/processing) and [p5](https://github.com/laurelkeys/large-i-mean-venti/tree/master/computer-graphics/halftone/p5js).

Based on this [post](https://timrodenbroeker.de/how-to-rasterize-an-image-with-processing/) by Tim Rodenbröker.

### Live demo
[Demo](https://editor.p5js.org/laurelkeys/sketches/6nMK4ljw7) on the p5.js Web Editor. Use the scroll wheel to change the amount of "particles".  You can also try other images by linking them on the `preload()` function.

<!-- [![](https://i.gyazo.com/4a6a17d90a7f8ccd3e70f7e3bde2fee5.gif)](https://editor.p5js.org/laurelkeys/sketches/6nMK4ljw7) -->

<a  href="https://editor.p5js.org/laurelkeys/sketches/6nMK4ljw7"><img  src="https://media.giphy.com/media/d9Ng621LiwumgM8hKC/giphy.gif"/></a>

<!-- -->
# genetic-algorithms

## to_be_or_not_to_be[.py](https://github.com/laurelkeys/large-i-mean-venti/blob/master/genetic-algorithms/to_be_or_not_to_be.py)

A genetic algorithm to find the phrase "*To be or not to be.*" in a pool of random strings.

Based on Daniel Shiffman's "The **Nature** of Code", [chapter 9](https://natureofcode.com/book/chapter-9-the-evolution-of-code/).

### Example usage
```
>>> python to_be_or_not_to_be.py
```
![](https://i.gyazo.com/992ad6d9a4d433988d85b437e5d67032.gif)

<!-- -->
# procedural-generation

## terrain[/](https://github.com/laurelkeys/large-i-mean-venti/blob/master/procedural-generation/terrain)

3D terrain generation with [Perlin noise](https://en.wikipedia.org/wiki/Perlin_noise), based on a [video](https://www.youtube.com/watch?v=IKB1hWWedMk) by Daniel Shiffman.

### Live demo
Check out a [live demo](https://www.openprocessing.org/sketch/729536) on OpenProcessing (click on **Open Controls** in the top right to change the terrain height and flight speed).

[![](https://gist.githubusercontent.com/laurelkeys/58bc9deb3a913ab65f2de6d41097f4f2/raw/7d9a7f6154c96bf7f43e1362bd81976bb855473a/terrain.png)](https://www.openprocessing.org/sketch/729536)

<!-- -->
# simulation
## boids[/](https://github.com/laurelkeys/large-i-mean-venti/blob/master/simulation/boids)
Build upon Daniel Shiffman's [Flocking Simulation](https://www.youtube.com/watch?v=mhjuuHl6qHM), based on Craig Reynolds [Boids](http://www.red3d.com/cwr/boids/).

### Live demo
[Live demo](https://editor.p5js.org/laurelkeys/full/PLeU1a7F1) on the p5.js Web Editor:

[![](https://i.gyazo.com/63a62214cf2fba0bab4356d336a3652d.gif)](https://editor.p5js.org/laurelkeys/full/PLeU1a7F1)

Click on **Open Controls** in the top right to change the boids' behavior:

[![](https://gist.githubusercontent.com/laurelkeys/58bc9deb3a913ab65f2de6d41097f4f2/raw/397a4ff192ee7c1d98873636bd41be4bbdfbe323/boids_controls.png)](https://editor.p5js.org/laurelkeys/sketches/PLeU1a7F1)

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
- `lower_bound`: Variable domain lower bound
- `upper_bound`: Variable domain upper bound
- `swarm_size`: Total number of bees
- `max_cycles`: Maximum number of cycles before halting
- `objective_func`: Objective function
- `objective_value`: Objective function target value
- `max_unimproved_trials`: Maximum number of cycles a bee can exploit it's "food source" before becoming a scout bee

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
dim = len(target)

model = Hive(lower_bound=[ord('a')]*dim, 
             upper_bound=[ord('z')]*dim, 
             swarm_size=100,  
             max_cycles=3000, 
             objective_func=poppins,
             objective_value=dim)
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
