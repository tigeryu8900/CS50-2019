double depth;
// change this to true if you want to invert the mouse control
boolean mouseIsInverted = false;

// mapKey is used to track multiple keypresses
boolean[] mapKey = new boolean[256];

// set all values of mapKey to false
for (int i = 0; i < mapKey.length; i++) {
  mapKey[i] = false;
}

// set a certain key as true when the key is pressed
void keyPressed() {
  mapKey[keyCode] = true;
}

// set a key as false when a certain key is released
void keyReleased() {
  mapKey[keyCode] = false;
}

void Sphere(double x, double y, double z, double r) {
  pushMatrix();
  translate(x, y, z);
  sphere(r);
  popMatrix();
}

class Ball {
  public PVector pos = new PVector(width / 2, height / 2, (width + height) / 4);
  public PVector v = new PVector(0, 0, 0);
  public int m = 7;
  color c = color(128, 128, 128);
  public double r = 49;
  public Ball(double x, double y, double z, double vx, double vy, double vz, double m, color c) {
    int r = Math.cbrt(m) * 20;
    this.pos = new PVector(x, y, z);
    this.v = new PVector(vx, vy, vz);
    this.m = m;
    this.c = c;
    this.r = r;
  }
  public Ball(double x, double y, double z, double m, color c) {
    this(x, y, z, random(-3, 4), random(-4, 3), random(-4, 3), m, c);
  }
  public Ball(double x, double y, double z, color c) {
    this(x, y, z, floor(random(5, 30)), c);
  }
  public Ball(double x, double y, double z, double m) {
    this(x, y, z, m, color(random(0, 255), random(0, 255), random(0, 255)));
  }
  public Ball(double x, double y, double z) {
    this(x, y, z, floor(random(5, 30)), color(random(0, 255), random(0, 255), random(0, 255)));
  }
  public Ball() {
    this(random(r, width - r), random(r, height - r), random(r, depth - r));
  }
  public void draw() {
    noStroke();
    fill(color);
    Sphere(pos.x, pos.y, pos.z, r);
    fill(255, 255, 255);
    fill(0, 0, 0);
    textSize(11);
    text(this.m, pos.x, pos.y, pos.z + r + 6.5);
  }
  PVector collide(Ball that) {
    double d = this.r + that.r;  /* dist between centers at impact */
    PVector p = PVector.sub(this.pos, that.pos);  /* delta positions */
    return p.dot(p) <= d * d;
  }
  void align(Ball that) {
    double d = this.r + that.r;  /* dist between centers at impact */
    PVector p = PVector.sub(this.pos, that.pos),  /* delta positions */
      v = PVector.sub(this.v, that.v);  /* delta velocities */
      /* Quadratic formula for (a)t² + (b)t + c = 0 */
    double a = v.dot(v),  /* t² coefficient */
      b = p.dot(v) * 2,  /* t coefficient */
      c = p.dot(p) - d * d,  /* constant */
      t = (-b - sqrt(b * b - 4 * a * c)) / (2 * a);  /* the answer! */

    /* Back them up to the touching point ... */
    this.pos.add(PVector.mult(this.v, t));
    that.pos.add(PVector.mult(that.v, t));
    this.t = that.t = -t;  /* partial time left on this iteration */
  }
  void bounce(Ball that) {
    PVector p = PVector.sub(this.pos, that.pos),  /* delta positions */
      v = PVector.sub(this.v, that.v);  /* delta velocities */
    double cf = this.r + that.r;  /* common factor */
    cf = 2 * v.dot(p) / (cf * cf * (this.m + that.m));

    this.v.sub(PVector.mult(p, cf * that.m));
    that.v.add(PVector.mult(p, cf * this.m));

    that.pos.add(PVector.mult(that.v, that.t)); /* resume partial journey */
    this.pos.add(PVector.mult(this.v, this.t)); /* resume partial journey */
  }
  void update() {
    if (pos.x <= r) v.x = abs(v.x);
    else if (pos.x >= width - r) v.x = -abs(v.x);
    if (pos.y <= r) v.y = abs(v.y);
    else if (pos.y >= height - r) v.y = -abs(v.y);
    if (pos.z <= r) v.z = abs(v.z);
    else if (pos.z >= depth - r) v.z = -abs(v.z);
    pos.add(v);
  }
}

class CollisionSystem {
  ArrayList<Ball> balls;
  public CollisionSystem(ArrayList<Ball> balls) {
    this.balls = balls;
  }
  public CollisionSystem() {
    this.balls = new ArrayList<Ball>;
  }
  public void run() {
    for (Ball b : balls) {
      b.update();
    }
    for (i = 0; i < balls.size() - 1; i++) {
      Ball s = balls.get(i);
      for (int j = i + 1; j < balls.size(); j++) {
        Ball t = balls.get(j);
        if (s.collide(t)) {
          s.align(t);
          s.bounce(t);
        }
      }
    }
    for (Ball b : balls) {
      b.draw();
    }
  }
  void addBase(Ball b) {
    int i;
    for (boolean collision = true; collision; b.pos.add(b.v)) {
      for (collision = false, i = 0; (!collision) && i < balls.size(); i++) {
        collision = b.collide(balls.get(i));
      }
    }
    balls.add(b);
  }
  public void add(double x, double y, double z, double vx, double vy, double vz, double m, color c) {
    addBase(new Ball(x, y, z, vx, vy, vz, m, c));
  }
  public void add(double x, double y, double z, double m, color c) {
    addBase(new Ball(x, y, z, m, c));
  }
  public void add(double x, double y, double z, color c) {
    addBase(new Ball(x, y, z, c));
  }
  public void add(double x, double y, double z, double m) {
    addBase(new Ball(x, y, z, m));
  }
  public void add(double x, double y, double z) {
    addBase(new Ball(x, y, z));
  }
  public void add() {
    addBase(new Ball());
  }
  public void remove(int a) {
    balls.remove(a);
  }
  public void remove() {
    remove(0);  /* snip */
  }
  public int getBallNum() {
    return balls.size();
  }
}

PVector pos = new PVector(width / 2, height / 2, (height / 2.0) / Math.tan(PI * 60.0 / 360.0));
PVector rot = new PVector(0, 0);

void drawBorder() {
  noLights();
  line(0, 0, 0, width, 0, 0);
  line(0, 0, 0, 0, height, 0);
  line(0, 0, 0, 0, 0, depth);
  line(0, height, depth, width, height, depth);
  line(width, 0, depth, width, height, depth);
  line(0, height, 0, 0, height, depth);
  line(0, 0, depth, 0, height, depth);
  line(width, height, 0, width, height, depth);
  line(0, 0, depth, width, 0, depth);
  line(width, 0, 0, width, 0, depth);
  line(0, height, 0, width, height, 0);
  line(width, 0, 0, width, height, 0);
  lights();
}

int timeStamp = millis();
double getFrameRate() {
  double fps = 1000/(millis() - timeStamp);
  timeStamp = millis();
  return fps;
}

void mousePressed() {
  /*if (!mouse.isLocked) lockPointer();
  else */if (mouseButton === LEFT) {
    int dist = random(0, depth); // jshint ignore:line
    int x = -Math.cos(rot.y) * Math.sin(rot.x) * dist + pos.x; // jshint ignore:line
    int y = Math.sin(rot.y) * dist + pos.y; // jshint ignore:line
    int z = -Math.cos(rot.y) * Math.cos(rot.x) * dist + pos.z; // jshint ignore:line
    collisionSystem.add(x, y, z);
    // collisionSystem2.add(mouseX, mouseY);
  } else {
    collisionSystem.remove(0);  /* snip */
    // collisionSystem2.remove(0);  /* snip */
  }
}

collisionSystem collisionSystem;

void setup() {
  size(600, 600, P3D);
  textMode(SCREEN);
  textAlign(CENTER, CENTER);
  lights();
  textFont(createFont("monospace"));
  depth = (width + height) / 2;
  collisionSystem = new CollisionSystem();
  collisionSystem.add();
  collisionSystem.add();
}

void draw() {
  if (mapKey[38] || mapKey[87]) { // forward
    // beginCamera();
    // rotateX(-rot.y);
    // translate(0, 0, mapKey[17] ? -12 : -3);
    pos.z -= mapKey[17] ? 12 : 3;
    // rotateX(rot.y);
    // endCamera();
  }
  if (mapKey[37] || mapKey[65]) { // left
    // beginCamera();
    // translate(mapKey[17] ? -12 : -3, 0, 0);
    pos.x -= mapKey[17] ? 12 : 3;
    // endCamera();
  }
  if (mapKey[40] || mapKey[83]) { // back
    // beginCamera();
    // rotateX(-rot.y);
    // translate(0, 0, mapKey[17] ? 12 : 3);
    pos.z += mapKey[17] ? 12 : 3;
    // rotateX(rot.y);
    // endCamera();
  }
  if (mapKey[39] || mapKey[68]) { // right
    // beginCamera();
    // translate(mapKey[17] ? 12 : 3, 0, 0);
    pos.x += mapKey[17] ? 12 : 3;
    // endCamera();
  }
  if (mapKey[32]) { // up
    // beginCamera();
    // rotateX(-rot.y);
    // translate(0, mapKey[17] ? -12 : -3, 0);
    pos.y -= mapKey[17] ? 12 : 3;
    // rotateX(rot.y);
    // endCamera();
  }
  if (mapKey[16]) { // down
    // beginCamera();
    // rotateX(-rot.y);
    // translate(0, mapKey[17] ? 12 : 3, 0);
    pos.y += mapKey[17] ? 12 : 3;
    // rotateX(rot.y);
    // endCamera();
  }
  // if (mouseIsPressed) {
  // }
  background(255, 255, 255);
  stroke(0, 0, 0);
  pushMatrix();
  beginCamera();
  translate(pos.x, pos.y, pos.z);
  // rotateX(rot.y);
  // rotateY(rot.x);
  drawBorder();
  endCamera();
  collisionSystem.run();
  popMatrix();
  // collisionSystem2.run();
  // line(width/2 - 5, height/2, width/2 + 5, height/2);
  // line(width/2, height/2 - 5, width/2, height/2 + 5);
  // image(screen, 0, 0);
  fill(0, 0, 0);
  text("frameRate: " + getFrameRate() + "\nx: " + pos.x + "\ny: " + pos.y + "\nz: " + pos.z + "\nrotx: " + rot.x +
    "\nroty: " + rot.y + "\nballs: " + collisionSystem.getBallNum(), width - 100, 20);
  text("➕", width/2, height/2);
    // ellipse(300, 300, 300, 300);
//println(mouse.vel.x);
    // println("x: " + (-Math.cos(rot.y) * Math.sin(rot.x)) + " y: " + (-Math.sin(rot.y)) + " z: " + (-Math.cos(rot.y) * Math.cos(rot.x)));
}
