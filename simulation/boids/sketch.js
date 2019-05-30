// ref.: Daniel Shiffman https://thecodingtrain.com/CodingChallenges/124-flocking-boids.html

const boids = [];

let alignSlider, cohesionSlider, separationSlider;

let Controls = function() {
    this.alignment = 1;
    this.cohesion = 1;
    this.separation = 1;
    this.perceptionRadius = 50;
};

let controls = new Controls();

function setup() {
    createCanvas(windowWidth, windowHeight);

    let gui = new dat.GUI({width: 295});
    gui.close();
    gui.add(controls, 'alignment', 0, 2.5).name("Alignment").step(0.1);
    gui.add(controls, 'cohesion', 0, 2.5).name("Cohesion").step(0.1);
    gui.add(controls, 'separation', 0, 2.5).name("Separation").step(0.1);
    gui.add(controls, 'perceptionRadius', 0, 200).name("Perception radius").step(5);
    
    // alignmentSlider = createSlider(0, 2, 1, 0.1);
    // cohesionSlider = createSlider(0, 2, 1, 0.1);
    // separationSlider = createSlider(0, 2, 1, 0.1);
    
    // div = createDiv('');
    // alignmentSlider.parent(div);
    // cohesionSlider.parent(div);
    // separationSlider.parent(div);
    
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