let cam;
let img;
let particles = 50;

function preload() {
  img = loadImage('woman.jpg');
}

function setup() {
  createCanvas(500, 700, WEBGL);
  setAttributes('antialias', true);

  cam = createEasyCam();
  cam.setDistanceMin(300);
  cam.setDistanceMax(300);

  img.resize(500, 700);
}

function mouseWheel(event) {
  if (event.delta > 0) {
    --particles;
  } else {
    ++particles;
  }
}

function draw() {
  translate(width / -2, height / -2);
  background('#fff');
  fill('#111111');
  noStroke();
  ortho();

  let particleSize = parseInt(width / particles);
  img.loadPixels();
  for (let y = 0; y < img.height; y += particleSize) {
    for (let x = 0; x < img.width; x += particleSize) {
      let off = (y * img.width + x) * 4;
      let rgb = img.pixels.slice(off, off + 3);
      let darkness = 1 - (rgb.reduce((acc, x) => acc + x) / 3 / 255);

      push();
      let d = darkness <= 0.5 ? (2 * darkness) ** 0.5 : (2 * (darkness - 0.5)) ** 0.5;
      translate(x, y, d * 200);
      box(darkness * particleSize);
      pop();
    }
  }
}