let cam;
const bbox = 550;
const radius = 8;
const margin = 20;

let n = 2;
let d = 29;
let scale = 150;

function setup() {
  createCanvas(bbox, bbox, WEBGL);
  setAttributes('antialias', true);
  cam = createEasyCam();
}

function draw() {
  background(220);
  drawAxis();
  drawBBox();
  
  stroke(0);
  drawMaurerRose(n, d, scale);
  
  stroke(255, 0, 255);
  drawMaurerRose(n, 1, scale); // when d == 1 we have a usual rose (rhodonea curve)
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