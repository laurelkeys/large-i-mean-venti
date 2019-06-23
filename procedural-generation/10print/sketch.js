// ref.: Daniel Shiffman https://www.youtube.com/watch?v=bEyTZ5ZZxZs
// 10 PRINT CHR$(205.5+RND(1)); : GOTO 10

const PINK = "#ffc0cb"

const SIZE = 30;
const MARGIN = SIZE;
const WEIGHT = 2;

let x = MARGIN;
let y = MARGIN;

let Controls = function () {
    this.bias = 0.5;
};
let controls = new Controls();

function setupGUI() {
    let gui = new dat.GUI({
        width: 295
    });
    gui.close();
    gui.add(controls, 'bias', 0, 1).name("Bias").step(0.05);
}

function setup() {
    createCanvas(600, 600);
    setupGUI();
    frameRate(30);
    background(PINK);
}

function draw() {
    if (y < height - MARGIN) {
        push();
        translate(x, y);
        drawSlash(1.0 - controls.bias);
        pop();

        x += SIZE;
        if (x >= width - MARGIN) {
            x = MARGIN;
            y += SIZE;
        }
    }
}

function drawSlash(bias) {
    stroke(0);
    strokeWeight(WEIGHT);
    if (random() < bias) {
        line(0, 0, SIZE, SIZE); // \
    } else {
        line(0, SIZE, SIZE, 0); // /
    }
}