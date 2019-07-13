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
      random(-bbox * f, bbox * f),
      random(-bbox * f, bbox * f)
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

  let ptMin = points[backBottomLeft(points)];
  normalMaterial();
  push();
  translate(ptMin.x, ptMin.y, ptMin.z);
  sphere(bbox / 50, 12, 12);
  pop();
  ambientMaterial(255);
}

function backBottomLeft(points) {
  // z, y, x
  let iMin = 0;
  for (let i = 1; i < points.length; ++i) {
    if (points[i].z < points[iMin].z) {
      iMin = i; // back most
    } else if (points[i].z == points[iMin].z) {
      if (-points[i].y < -points[iMin].y) {
        iMin = i; // bottom most
      } else if (points[i].y == points[iMin].y && points[i].x < points[iMin].x) {
        iMin = i; // left most
      }
    }
  }
  return iMin;
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
  stroke(255, 0, 0); // x (R)
  line(0, 0, 0, bbox / 10, 0, 0);
  stroke(0, 255, 0); // y (G)
  line(0, 0, 0, 0, bbox / 10, 0);
  stroke(0, 0, 255); // z (B)
  line(0, 0, 0, 0, 0, bbox / 10);
  pop();
}