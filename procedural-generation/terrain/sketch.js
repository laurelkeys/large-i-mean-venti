// ref.: Daniel Shiffman https://www.youtube.com/watch?v=IKB1hWWedMk

let scale = 20;
let cols, rows;
let w = 1400;
let h = 1000;

let flightPos = 0;
// let flightSpeed = 0.08;
// let noiseDelta = 0.16;
let terrain = [];
// let terrainHeight = 112;

let Controls = function () {
    this.flightSpeed = 0.08;
    this.noiseDelta = 0.16;
    this.terrainHeight = 112;
    this.xTheta = 60;
    this.yTheta = 0;
    this.zTheta = 0;
};
let controls = new Controls();

function setupGUI() {
    let gui = new dat.GUI({
        width: 295
    });
    gui.close();
    gui.add(controls, 'flightSpeed', 0, 0.4).name("Flight speed").step(0.02);
    gui.add(controls, 'noiseDelta', 0.05, 0.4).name("Noise delta").step(0.01);
    gui.add(controls, 'terrainHeight', 0, 200).name("Terrain height").step(1);
    gui.add(controls, 'xTheta', 0, 180).name("X rotation").step(1);
    gui.add(controls, 'yTheta', 0, 180).name("Y rotation").step(1);
    gui.add(controls, 'zTheta', 0, 180).name("Z rotation").step(1);
}

function setup() {
    createCanvas(displayWidth, displayHeight, WEBGL);
    setupGUI();

    cols = w / scale;
    rows = h / scale;
    for (let x = 0; x < cols; ++x) {
        terrain[x] = [];
    }
}

function draw() {
    flightPos -= controls.flightSpeed;
    shiftNoiseSpace();

    background(51);
    stroke(255);
    noFill();

    rotateX(radians(controls.xTheta));
    rotateY(radians(controls.yTheta));
    rotateZ(radians(controls.zTheta));
    translate((-w / 2) + 1, (-h / 2) + 30);

    for (let y = 0; y < rows - 1; ++y) {
        beginShape(TRIANGLE_STRIP);
        for (let x = 0; x < cols; ++x) {
            vertex(x * scale, y * scale, terrain[x][y]);
            vertex(x * scale, (y + 1) * scale, terrain[x][y + 1]);
        }
        endShape();
    }
}

function shiftNoiseSpace() {
    let yOffset = flightPos;
    for (let y = 0; y < rows; ++y) {
        let xOffset = 0;
        for (let x = 0; x < cols; ++x) {
            terrain[x][y] = map(noise(xOffset, yOffset), 0, 1, -controls.terrainHeight, controls.terrainHeight);
            xOffset += controls.noiseDelta;
        }
        yOffset += controls.noiseDelta;
    }
}