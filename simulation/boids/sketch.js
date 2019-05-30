// ref.: Daniel Shiffman https://thecodingtrain.com/CodingChallenges/124-flocking-boids.html

const boids = [];

let alignSlider, cohesionSlider, separationSlider;

function setup() {
    createCanvas(640, 480);
    
    alignmentSlider = createSlider(0, 2, 1, 0.1);
    cohesionSlider = createSlider(0, 2, 1, 0.1);
    separationSlider = createSlider(0, 2, 1, 0.1);
    
    div = createDiv('');
    alignmentSlider.parent(div);
    cohesionSlider.parent(div);
    separationSlider.parent(div);
    
    for (let i = 0; i < 200; i++) {
        boids.push(new Boid());
    }
}

function draw() {
    background(51);
    let boidsSnapshot = [...boids];
    for (let boid of boids) {
        boid.flock(boidsSnapshot);
        boid.update();
        boid.wraparound();
        boid.show();
    }
}