// ref.: https://www.cs.jhu.edu/~misha/Spring16/09.pdf

let cam;
const bbox = 500;
const radius = 5;
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

let firstRun = true;
let convexHull = [];

function draw() {
  background(220);
  ambientMaterial(255);
  rotateY(0.01 * frameCount);

  drawAxis();
  drawBBox();
  drawPoints();
  
  if (firstRun) {
    convexHull = giftWrap();
    firstRun = false;
  } else {
    for (let t of convexHull) {
      drawTriangleOnHull(t[0], t[1], t[2]);
    }
  }
}

function giftWrap() {
  let [a, b, c] = triangleOnHull();

  let queue = [
    [a, b],
    [b, c],
    [c, a]
  ];

  let hull = [];
  hull.push([a, b, c]);
  // drawTriangleOnHull(a, b, c);

  let visitedEdges = [];
  while (queue.length != 0) {
    let p, q;
    [[p, q], ...queue] = queue;
    if (!visited(visitedEdges, p, q)) {
      let pt = pivotAroundEdge(p, q);
      hull.push([p, q, pt]);
      // drawTriangleOnHull(p, q, pt);

      queue = [...queue,
        [q, pt],
        [pt, p]
      ];

      visitedEdges.push([p, q]);
    }
  }
  
  return hull;
}

function visited(edges, p, q) {
  for (let [a, b] of edges) {
    if (a == p && b == q) return true;
    if (a == q && b == p) return true;
  }
  return false;
}

function triangleOnHull() {
  let [p, q] = edgeOnHull(points);
  let r = pivotAroundEdge(p, q, points);
  return [p, q, r];
}

function edgeOnHull() {
  let p = points[backBottomLeft()]; // backmost point
  let q = p;
  for (let r of points) {
    if (q.z == r.z && q.y == r.y && q.x < r.x)
      q = r; // rightmost point on the same zy-plane as p

    if (q == p)
      q = createVector(1, 0, 0).add(p); // virtual reference point to the right of p
  }
  q = pivotAroundEdge(p, q);
  return [p, q]; // edge
}

function pivotAroundEdge(p, q) {
  let pt = points[0];
  let area2 = area(p, q, pt) ** 2;
  for (let i = 1; i < points.length; ++i) {
    let pt_ = points[i];
    let volume = signedVolume(p, q, pt, pt_);
    if (volume < 0) {
      pt = pt_;
    } else if (volume == 0) {
      // pt_ is on the same (p, q, pt)-plane
      let area2_ = area(p, q, pt_) ** 2;
      if (area2_ > area2) {
        pt = pt_;
        area2 = area2_;
      }
    }
  }
  return pt;
}

function backBottomLeft() {
  let index = 0;

  for (let i = 1; i < points.length; ++i) {
    if (points[i].z < points[index].z) {
      index = i; // backmost
    } else if (points[i].z == points[index].z) {
      if (-points[i].y < -points[index].y) {
        index = i; // bottommost
      } else if (points[i].y == points[index].y && 
                 points[i].x < points[index].x) {
        index = i; // leftmost
      }
    }
  }

  return index;
}

function area(a, b, c) {
  let b_a = p5.Vector.sub(b, a);
  let c_a = p5.Vector.sub(c, a);
  return (1 / 2) * b_a.cross(c_a).mag();
}

function signedVolume(a, b, c, d) {
  let b_a = p5.Vector.sub(b, a);
  let c_a = p5.Vector.sub(c, a);
  let d_a = p5.Vector.sub(d, a);
  return (1 / 6) * d_a.dot(b_a.cross(c_a));
}

function colorPoint(pt) {
  normalMaterial();
  push();
  translate(pt.x, pt.y, pt.z);
  sphere(1.1 * radius, 12, 12);
  pop();
  ambientMaterial(255);
}

function drawTriangleOnHull(a, b, c) {
  drawPoly(a, b, c);
  colorPoint(a);
  colorPoint(b);
  colorPoint(c);
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
    sphere(radius, 12, 12);
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