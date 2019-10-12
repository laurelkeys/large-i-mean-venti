let cam;
const bbox = 550;
const radius = 8;
const margin = 20;

let n = 2;
let d = 29;
let scale = 150;

const f = 0.000001;
let time = 0;
let slider1, slider2, slider3, slider4, slider5;

function setup() {
  createCanvas(bbox, bbox, WEBGL);
  setAttributes('antialias', true);
  cam = createEasyCam();
  
  // slider1 = createSlider(1, 180, 1);
  // slider2 = createSlider(1, 180, 1);
  // slider3 = createSlider(1, 180, 1);
  // slider4 = createSlider(1, 180, 1);
  // slider5 = createSlider(1, 180, 1);
}

function draw() {
  background(220);
  drawAxis();
  drawBBox();
  
  // stroke(0);
  // drawMaurerRose(n, d, scale);
  // stroke(255, 0, 255);
  // drawMaurerRose(n, 1, scale); // when d == 1 we have a usual rose (rhodonea curve)

  cam.rotateZ(0.001 * map(noise(f * time++), 0, 1, -2, 1));
  cam.rotateY(0.01 * map(noise(f * time++), 0, 1, -1, 1));
  cam.rotateX(0.005 * map(noise(f * time++), 0, 1, -1, 1));
  draw3DRose(scale,
             map(noise(f * time++), 0, 1, 1, 180),
             map(noise(f * time++), 0, 1, 1, 180),
             map(noise(f * time++), 0, 1, 1, 180),
             map(noise(f * time++), 0, 1, 1, 180),
             map(noise(f * time++), 0, 1, 1, 180));
}

function draw3DRose(scale, m=4, n=1, ds=1, dt=1, ct=0) {
  noFill();
  beginShape();
  for (let angle = 0; angle <= 360; ++angle) {
    const s = ds * radians(angle);
    const t = dt * s + ct;
    const r = scale * cos(m*t) * cos(n*s);
    const x = r * cos(t) * sin(s);
    const y = r * sin(t) * sin(s);
    const z = r * sin(s);
    vertex(x, y, z);
  }
  endShape();
}

function drawMaurerRose(n, d, scale) {
  noFill();
  beginShape();
  for (let angle = 0; angle <= 360; ++angle) {
    const theta = d * radians(angle);
    const r = scale * sin(n * theta);
    const x = r * cos(theta);
    const y = r * sin(theta);
    vertex(x, y);    
  }
  endShape();
}

function drawBBox() {
  stroke(0);
  strokeWeight(1);

  const f = 0.25;
  // z = bbox
  line(-bbox * f, bbox * f, bbox * f, bbox * f, bbox * f, bbox * f);
  line(bbox * f, bbox * f, bbox * f, bbox * f, -bbox * f, bbox * f);
  line(bbox * f, -bbox * f, bbox * f, -bbox * f, -bbox * f, bbox * f);
  line(-bbox * f, -bbox * f, bbox * f, -bbox * f, bbox * f, bbox * f);
  // z = -bbox
  line(-bbox * f, bbox * f, -bbox * f, bbox * f, bbox * f, -bbox * f);
  line(bbox * f, bbox * f, -bbox * f, bbox * f, -bbox * f, -bbox * f);
  line(bbox * f, -bbox * f, -bbox * f, -bbox * f, -bbox * f, -bbox * f);
  line(-bbox * f, -bbox * f, -bbox * f, -bbox * f, bbox * f, -bbox * f);
  // x = bbox
  line(bbox * f, bbox * f, bbox * f, bbox * f, bbox * f, -bbox * f);
  line(bbox * f, -bbox * f, bbox * f, bbox * f, -bbox * f, -bbox * f);
  // x = -bbox
  line(-bbox * f, bbox * f, bbox * f, -bbox * f, bbox * f, -bbox * f);
  line(-bbox * f, -bbox * f, bbox * f, -bbox * f, -bbox * f, -bbox * f);
}

function drawAxis() {
  strokeWeight(1);
  stroke(255, 0, 0); // R (x)
  line(0, 0, 0, bbox / 10, 0, 0);
  stroke(0, 255, 0); // G (y)
  line(0, 0, 0, 0, bbox / 10, 0);
  stroke(0, 0, 255); // B (z)
  line(0, 0, 0, 0, 0, bbox / 10);
}