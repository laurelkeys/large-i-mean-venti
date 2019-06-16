// ref.: Daniel Shiffman https://www.youtube.com/watch?v=IKB1hWWedMk

let scale = 20;
let cols, rows;
let w = 1400;
let h = 1000;

let flightPos = 0;
let flightSpeed = 0.08;
let noiseDelta = 0.16;
let terrain = [];

function setup() {
    createCanvas(600, 600, WEBGL);
    cols = w / scale;
    rows = h / scale;
    for (let x = 0; x < cols; ++x) terrain[x] = [];
}

function draw() {
    flightPos -= flightSpeed;
    shiftNoiseSpace();

    background(51);
    stroke(255);
    noFill();

    rotateX(PI / 3);
    translate((-w / 2) + 1, (-h / 2) + 50);

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
            terrain[x][y] = map(noise(xOffset, yOffset), 0, 1, -100, 100);
            xOffset += noiseDelta;
        }
        yOffset += noiseDelta;
    }
}