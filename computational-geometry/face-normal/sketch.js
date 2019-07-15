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
  
  let [a, b, c] = points.slice(0, 4);
  let centroid = triangleCentroid(a, b, c);
  
  noStroke();
  push();
  translate(centroid.x, centroid.y, centroid.z);
  normalMaterial();
  sphere(radius, 12, 12);
  pop();
  
  drawPoly(a, b, c);
  
  let b_a = p5.Vector.sub(b, a); // YELLOW
  let c_a = p5.Vector.sub(c, a); // CYAN
  let normal = p5.Vector.cross(b_a, c_a).setMag(100); // BLACK
  push();
  translate(a);
  strokeWeight(3);
  stroke(255, 255, 0); // YELLOW
  line(0, 0, 0, b_a.x, b_a.y, b_a.z);
  stroke(0, 255, 255); // CYAN
  line(0, 0, 0, c_a.x, c_a.y, c_a.z);
  stroke(0); // BLACK
  line(0, 0, 0, normal.x, normal.y, normal.z);
  pop();
  push();
  translate(centroid);
  stroke(0); // BLACK
  strokeWeight(3);
  line(0, 0, 0, normal.x, normal.y, normal.z);  
  pop();
  
  // noLoop();

}

function triangleCentroid(a, b, c) {
  return [a, b, c].reduce((acc, pt) => acc.add(pt), createVector(0,0,0)).mult(1/3);
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