#include <Arduino.h>
// macro prevents the interrupt from changing part of the posi variable while it
// is being read. Without the ATOMIC_BLOCK macro, it is possible for the
// interrupt to change part of the posi while it is being read, leading to a
// completely different reading of the variable.
#include <util/atomic.h>

// Define the pins for the left motor
#define ENL 9  // pmw pin
#define IN1 8
#define IN2 7
#define C1L 18  // interupt
#define C2L 19  // interupt
// Define the pins for the right motor
#define ENR 4  // pmw pin
#define IN3 6
#define IN4 5
#define C1R 20  // interupt
#define C2R 21  // interupt
// define the pins for the joysticks
#define JL A0
#define JR A1
// define the pins for the left and right limit switch
#define LSL 2
#define LSR 3

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

// if boarder is near
bool blockLeftPos = false;
bool blockLeftNeg = false;
bool blockRightPos = false;
bool blockRightNeg = false;

// direction of travel of the rocket, true = pos = up
bool dirL;
bool dirR;

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
  attachInterrupt(digitalPinToInterrupt(LSL), readLSL, RISING);
  attachInterrupt(digitalPinToInterrupt(LSR), readLSR, RISING);

  // null the coords at begining
  findCoordOrigin();
  Serial.begin(9600);
}

void loop() {
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
 int* coords = corectCoords(calculateCoords(BOARD_WIDTH, posL, posR), COORD_SCAL, (BOARD_WIDTH / 2), BOARD_HIGHT);
 blockCheck(coords);
 Serial.println();
  // joystickvalues
  int jValL = analogRead(JL);
  int jValR = analogRead(JR);

  // rasperry serial com
  int gameMode = getGameMode();

  // rocket move with player input and mode
  executeGameMode(jValL, jValR, gameMode);
}

void executeGameMode(int jValL, int jValR, int gameMode) {
  switch (gameMode) {
    case 0:
      // move the motors in the direction of the joystick and different speed,
      // depending on joysticktilt
      moveRocket(
          (int)round(mapFloat(jValL, 0, MAX_JVAL, -MAX_SPEED, MAX_SPEED)),
          (int)round(mapFloat(jValR, 0, MAX_JVAL, -MAX_SPEED, MAX_SPEED)));
      break;
  }
}

int getGameMode() {
  // todoooooo
  return 0;
}

void blockCheck(int coords[2]) {
  blockLeftPos = blockRightPos = (coords[0]+coords[0]) > BOARD_WIDTH;
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

void moveRocket(int leftSpeed, int rightSpeed) {
  // Control the direction of the left motor
  dirL = leftSpeed > 0;
  if (leftSpeed == 0) {
    digitalWrite(IN1, false);
    digitalWrite(IN2, false);
  } else {
    digitalWrite(IN1, dirL);
    digitalWrite(IN2, !dirL);
  }

  // Control the direction of the right motor
  dirR = rightSpeed > 0;
  if (rightSpeed == 0) {
    digitalWrite(IN3, false);
    digitalWrite(IN4, false);
  } else {
    digitalWrite(IN3, dirR);
    digitalWrite(IN4, !dirR);
  }

  // catch if rocket is at boarder
  if ((dirL && blockLeftPos) || (!dirL && blockLeftNeg)) {
    digitalWrite(IN1, false);
    digitalWrite(IN2, false);
    analogWrite(ENL, 0);
  }
  if ((dirR && blockRightPos) || (!dirR && blockRightNeg)) {
    digitalWrite(IN3, false);
    digitalWrite(IN4, false);
    analogWrite(ENR, 0);
  }
  // Set the speed of the motors
  analogWrite(ENL, abs(leftSpeed));
  analogWrite(ENR, abs(rightSpeed));
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

void readLSL() {
  blockLeftPos = dirL;
  blockLeftNeg = !dirL;
}

void readLSR() {
  blockRightPos = dirR;
  blockRightNeg = !dirR;
}

float mapFloat(long x, long in_min, long in_max, long out_min, long out_max) {
  return (float)(x - in_min) * (out_max - out_min) / (float)(in_max - in_min) +
         out_min;
}