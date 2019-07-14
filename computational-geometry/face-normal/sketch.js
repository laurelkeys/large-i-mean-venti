let cam;
const bbox = 550;
const radius = 8;
const margin = 20;

let points = [];
const pointsCount = 3;

function setup() {
  createCanvas(bbox, bbox, WEBGL);
  setAttributes('antialias', true);

  cam = createEasyCam();

  let f = 0.25; // 0.2;
  for (let i = 0; i < pointsCount; ++i) {
    points.push(createVector(
      random(-bbox * f, bbox * f),
      random(-bbox * f, bbox * f),
      random(-bbox * f, bbox * f)
    ));
  }
}

function draw() {
  background(220);
  ambientMaterial(255);
  rotateY(0.01 * frameCount);
  ambientLight(60, 60, 60);
  directionalLight(110, 90, 110, -width, height, 0.05);
  directionalLight(240, 255, 240, width, height, 0.05);

  drawAxis();
  drawBBox();
  drawPoints();
  
  drawPoly(...points);
}

function drawPoly(...vertices) {
  strokeWeight(1);
  stroke(255, 0, 255);
  fill(255, 0, 255, 50);
  beginShape();
  for (let v of vertices)
    vertex(v.x, v.y, v.z);
  endShape(CLOSE);
}

function drawPoints() {
  noStroke();
  for (let p of points) {
    push();
    translate(p.x, p.y, p.z);
    // normalMaterial();
    sphere(radius, 12, 12);
    pop();
  }
}

function drawBBox() {
  let f = 0.25;
  
  stroke(0);
  strokeWeight(1);

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
  strokeWeight(2);
  stroke(255, 0, 0); // R (x)
  line(0, 0, 0, bbox / 10, 0, 0);
  stroke(0, 255, 0); // G (y)
  line(0, 0, 0, 0, bbox / 10, 0);
  stroke(0, 0, 255); // B (z)
  line(0, 0, 0, 0, 0, bbox / 10);
}