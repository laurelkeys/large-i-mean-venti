// ref.: https://www.cs.jhu.edu/~misha/Spring16/09.pdf

let cam;
const bbox = 500;
const margin = 20;
const points = [];
const pointsCount = 50;

function setup() {
  createCanvas(bbox, bbox, WEBGL);
  setAttributes('antialias', true);

  cam = createEasyCam();

  let f = 0.2;
  for (let i = 0; i < pointsCount; ++i) {
    points.push(createVector(
      random(-bbox * f, bbox * f),
      0,
      0
    ));
  }
}

function draw() {
  background(220);
  // rotateY(0.01 * frameCount);

  drawAxis();
  drawBBox();
  drawPoints();

  drawPoly(points[0], points[1], points[2]);

  // colorPoint(points[backBottomLeft(points)]);
  edgeOnHull(points);
}

function colorPoint(pt) {
  normalMaterial();
  push();
  translate(pt.x, pt.y, pt.z);
  sphere(bbox / 50, 12, 12);
  pop();
  ambientMaterial(255);
}

function edgeOnHull(points) {
  let p = points[backBottomLeft(points)]; // backmost point
  let q = p;
  for (let r of points) {
    if (q.z == r.z && q.y == r.y && q.x < r.x)
      q = r // rightmost point on the same zy-plane as p
    
    if (q == p)
      q = createVector(1, 0, 0).add(p); // virtual reference point to the right of p
  }
  colorPoint(p);
  colorPoint(q);
  // TODO pivotOnEdge
}

function backBottomLeft(points) {
  let index = 0;
  
  for (let i = 1; i < points.length; ++i)
    if (points[i].z < points[index].z) index = i; // backmost
  
    else if (points[i].z == points[index].z)
      if (-points[i].y < -points[index].y) index = i; // bottommost
  
      else if (points[i].y == points[index].y && 
               points[i].x < points[index].x) index = i; // leftmost
  
  return index;
}

function drawPoly(...vertices) {
  push();
  stroke(255, 0, 255);
  fill(255, 0, 255, 50);

  beginShape();
  for (let v of vertices)
    vertex(v.x, v.y, v.z);
  endShape(CLOSE);

  pop();
}

function drawPoints() {
  for (let p of points) {
    push();
    translate(p.x, p.y, p.z);
    // normalMaterial();
    sphere(bbox / 50, 12, 12);
    pop();
  }
}

function drawBBox() {
  stroke(0);
  let f = 0.25;

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
  push();
  stroke(255, 0, 0); // R (x)
  line(0, 0, 0, bbox / 10, 0, 0);
  stroke(0, 255, 0); // G (y)
  line(0, 0, 0, 0, bbox / 10, 0);
  stroke(0, 0, 255); // B (z)
  line(0, 0, 0, 0, 0, bbox / 10);
  pop();
}