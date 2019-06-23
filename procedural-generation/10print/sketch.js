// ref.: Daniel Shiffman https://www.youtube.com/watch?v=bEyTZ5ZZxZs
// 10 PRINT CHR$(205.5+RND(1)); : GOTO 10

const PINK = "#ffc0cb"

let rate = 30;
let size = 20;
let weight = 2;
let bias = 0.5;

let x = 0;
let y = 0;

function setup() {
    createCanvas(600, 600);
    frameRate(rate);
    background(PINK);
}

function draw() {
    if (y <= height) {
        push();
        translate(x, y);
        drawSlash(bias);
        pop();
    
        x += size;
        if (x > width) {
            x = 0;
            y += size;
        }
    }
}

function drawSlash() {
    stroke(0);
    strokeWeight(weight);
    if (random() < bias) {
        line(0, 0, size, size); // \
    } else {
        line(0, size, size, 0); // /
    }
}