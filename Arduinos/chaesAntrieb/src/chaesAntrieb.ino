#include <Arduino.h>
// macro prevents the interrupt from changing part of the posi variable while it
// is being read. Without the ATOMIC_BLOCK macro, it is possible for the
// interrupt to change part of the posi while it is being read, leading to a
// completely different reading of the variable.
#include <util/atomic.h>

// Define the pins for the left motor
#define ENL 9  // pmw pin
#define IN1 21
#define IN2 22
#define C1L 18  // interupt
#define C2L 19  // interupt
// Define the pins for the right motor
#define ENR 4  // pmw pin
#define IN3 23
#define IN4 22
#define C1R 20  // interupt
#define C2R 21  // interupt
// define the pins for the joysticks
#define JL A0
#define JR A1
// define the pins for the left and right limit switch
#define LSL 3
#define LSR 2

// volatile keyword prevents the compiler from performing optimizations on the
// variable that could potentially lead to it being misread. In addition to the
// volatile directive, an ATOMIC_BLOCK macro is needed to access the position
// variable.
volatile int posVL = 0;
volatile int posVR = 0;

const long MAX_SPEED = 255;  // Maximum speed for the motors
const long MAX_JVAL = 1023;  // 1023 max value for joysticks. min value is 0
const int BOARD_WIDTH = 533;
const int BOARD_HIGHT = 770;
const int COORD_SCAL = 1;  // coord = encodersteps / SCAL
const int DEADZONE = 30;  // deadzone for the joysticks

// if boarder is near
bool blockLeftPos = false;
bool blockLeftNeg = false;
bool blockRightPos = false;
bool blockRightNeg = false;

// direction of travel of the rocket, true = pos = up
bool dirL;
bool dirR;

// modi: -1 = dont move/ default, 0 = transportmode, 1 = joystick,...
int gameMode = -1;
// coordinates of the rocket
int* coords;

void setup() {
  // dc motor entcoder
  pinMode(C1L, INPUT);
  pinMode(C2L, INPUT);
  pinMode(C1R, INPUT);
  pinMode(C2R, INPUT);
  attachInterrupt(digitalPinToInterrupt(C1L), readEncoderL, RISING);
  attachInterrupt(digitalPinToInterrupt(C1R), readEncoderR, RISING);

  // motor
  pinMode(ENL, OUTPUT);
  pinMode(ENR, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // limit switches
  pinMode(LSL, INPUT);
  pinMode(LSR, INPUT);
  attachInterrupt(digitalPinToInterrupt(LSL), readRisingLSL, RISING);
  attachInterrupt(digitalPinToInterrupt(LSR), readRisingLSR, RISING);
  attachInterrupt(digitalPinToInterrupt(LSL), readFallingLSL, FALLING);
  attachInterrupt(digitalPinToInterrupt(LSR), readFallingLSR, FALLING);

  // null the coords at begining
  //findCoordOrigin();
  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  checkForInput();/*
  coords = getCoords();
  blockCheck(coords);*/
  executeGameMode(analogRead(JL), analogRead(JR), gameMode);
}

void checkForInput() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    if (input == "ID") {
      Serial.println("chaesAntrieb");
      return;
    }
    if (input == "transportmode") {
      gameMode = 0;
      return;
    }
    if (input == "gameOver"){
      sentCoords(coords);
      gameMode = -1;
      return;
    }
  }
}

void executeGameMode(int jValL, int jValR, int gameMode) {
  switch (gameMode) {
    case -1: //default
      moveRocket(0, 0);
      break;
    case 0: //transportmodus
      transportmodus();
      break;
    case 1:
      // move the motors in the direction of the joystick and different speed,
      // depending on joysticktilt
      moveRocket(
          (int)round(mapFloat(jValL, 0, MAX_JVAL, -MAX_SPEED, MAX_SPEED)),
          (int)round(mapFloat(jValR, 0, MAX_JVAL, -MAX_SPEED, MAX_SPEED)));
      break;
  }
}

void sentCoords(int coords[2]){
  Serial.println(String(coords[0]) + "/" + String(coords[1]));
}

int* getCoords() {
  // Read the position of the motors in an atomic block to avoid a potential
  // misread if the interrupt coincides with this code running see:
  // https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
  int posL = 0;
  int posR = 0;
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    posL = posVL;
    posR = posVR;
  }
  // coordinates
  return boxCoords(corectCoords(calculateCoords(BOARD_WIDTH, posL, posR),
                                COORD_SCAL, BOARD_WIDTH / 2, BOARD_HIGHT),
                   BOARD_WIDTH / 2, -BOARD_WIDTH / 2, 0, BOARD_HIGHT);
}

void blockCheck(int coords[2]) {
  blockLeftPos = blockRightPos = (coords[0] + coords[1]) < BOARD_WIDTH;
}

void findCoordOrigin() {
  while (!blockLeftNeg && !blockRightNeg) {
    moveRocket(-MAX_SPEED, -MAX_SPEED);
  }
  posVL = 0;
  posVR = 0;
}

float* calculateCoords(int distance, int left, int right) {
  float angle = (float)(left * distance) / (float)(left * left + right * right);
  float x = left * angle;
  float y = right * angle;
  float* coords = new float[2]{x, y};
  return coords;
}

int* corectCoords(float coords[2], int scal, int xCor, int yCor) {
  int* corectedCoords = new int[2];
  corectedCoords[0] = coords[0] / scal;
  corectedCoords[1] = coords[0] / scal;
  corectedCoords[0] = coords[0] - xCor;
  corectedCoords[1] = coords[0] - yCor;
  return corectedCoords;
}

int* boxCoords(int coords[2], int leftBorder, int rightBorder, int lowerBorder,
               int upperBorder) {
  if (coords[0] < leftBorder) {
    coords[0] = leftBorder;
  }
  if (coords[0] > rightBorder) {
    coords[0] = rightBorder;
  }
  if (coords[1] < lowerBorder) {
    coords[1] = lowerBorder;
  }
  if (coords[1] > upperBorder) {
    coords[1] = upperBorder;
  }
  return coords;
}

void moveRocket(int leftSpeed, int rightSpeed) {
  // Control the direction of the left motor
  dirL = leftSpeed > 0;
  if (-DEADZONE <= leftSpeed && leftSpeed <= DEADZONE) {
    digitalWrite(IN1, false);
    digitalWrite(IN2, false);
  } else {
    digitalWrite(IN1, dirL);
    digitalWrite(IN2, !dirL);
  }

  // Control the direction of the right motor
  dirR = rightSpeed > 0;
  if (-DEADZONE <= leftSpeed && leftSpeed <= DEADZONE) {
    digitalWrite(IN3, false);
    digitalWrite(IN4, false);
  } else {
    digitalWrite(IN3, dirR);
    digitalWrite(IN4, !dirR);
  }

  // catch if rocket is at boarder and set the speed of the motors
  if ((dirL && blockLeftPos) || (!dirL && blockLeftNeg)) {
    digitalWrite(IN1, false);
    digitalWrite(IN2, false);
    analogWrite(ENL, 0);
  } else {
    analogWrite(ENL, abs(leftSpeed));
  }
  if ((dirR && blockRightPos) || (!dirR && blockRightNeg)) {
    digitalWrite(IN3, false);
    digitalWrite(IN4, false);
    analogWrite(ENR, 0);
  } else {
    analogWrite(ENR, abs(rightSpeed));
  }
}

void transportmodus(){
  while (!blockLeftPos && !blockRightPos) {
    moveRocket(MAX_SPEED, MAX_SPEED);
  }
}

void readEncoderL() {
  int x = digitalRead(C2L);
  if (x > 0) {
    posVL++;
  } else {
    posVL--;
  }
}

void readEncoderR() {
  int x = digitalRead(C2R);
  if (x > 0) {
    posVR++;
  } else {
    posVR--;
  }
}

void readRisingLSL() {
  blockLeftPos = dirL;
  blockLeftNeg = !dirL;
}

void readRisingLSR() {
  blockRightPos = dirR;
  blockRightNeg = !dirR;
}

void readFallingLSL() { blockLeftPos = blockLeftNeg = false; }

void readFallingLSR() { blockRightPos = blockRightNeg = false; }

float mapFloat(long x, long in_min, long in_max, long out_min, long out_max) {
  return (float)(x - in_min) * (out_max - out_min) / (float)(in_max - in_min) +
         out_min;
}