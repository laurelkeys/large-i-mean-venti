let img;

function preload() {
  img = loadImage('woman.jpg');
}

function setup() {
  createCanvas(500, 700);
  background('#ffffff');
  img.resize(500, 700);
}

function draw() {
  background('#ffffff');
  fill('#111111');
  noStroke();

  let particles = map(mouseX, 0, width, 10, 100);
  let particleSize = parseInt(img.width / particles);
  
  img.loadPixels();
  for (let y = 0; y < img.height; y += particleSize) {
    for (let x = 0; x < img.width; x += particleSize) {
      let off = (y * img.width + x) * 4;
      let rgb = img.pixels.slice(off, off+3);
      let darkness = map(rgb.reduce((acc, x) => acc + x) / 3, 0, 255, 1, 0);

      push();
      translate(x, y);
      circle(0, 0, darkness * particleSize);
      pop();

    }
  }
}