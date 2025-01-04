#include <Arduino.h>
#include <util/atomic.h>

// Define the pins for the left motor
#define ENR 4   // pmw pin (speed)
#define IN4 25  // direction pin (forward)
#define IN3 24  // direction pin (backward)
#define C1R 18  // interupt (encoder)
#define C2R 19  // interupt (encoder)

// Define the pins for the right motor
#define ENL 5   // pmw pin (speed)
#define IN2 23  // direction pin (forward)
#define IN1 22  // direction pin (backward)
#define C1L 20  // interupt (encoder)
#define C2L 21  // interupt (encoder)

// Define the pins for the joysticks
#define joystickL A0
#define joystickR A1

// Define the pins for the left and right limit switch
#define limitSwitchL 3
#define limitSwitchR 2

// Constants
const long MIN_JVALR = 370;  // min value for joysticks
const long MIN_JVALL = 355;
const long MAX_JVALR = 725;  //  max value for joysticks
const long MAX_JVALL = 650;

const int BOARD_WIDTH = 533;
const int BOARD_HIGHT = 770;
const int COORD_SCAL = 1;  // mm = steps / SCAL
const int LIMIT_SWITCH_HIGHT = 770;

const long MAX_SPEED = 255;   // Maximum speed for the motors
const int NULL_SPEED1 = 125;  // nulling speeds
const int NULL_SPEED2 = 120;

const int DEADZONE = 30;       // deadzone for the joysticks
const int MAX_LATENCY = 1000;  // max latency in ms

//positions
const int EJECT_POSX = 10;
const int EJECT_POSY = 10;
const int NULLING_OFFSETX = 20;
const int NULLING_OFFSETY = 20;
const int RADIUS_TO_EJECTPOS = 10;

// Volatile variables
volatile int posVL = 0;  // position of the left motor
volatile int posVR = 0;  // position of the right motor

// Flags for nulling the coordinates
volatile bool nullLeft = false;
volatile bool nullRight = false;

// Flags for blocking movement
bool blockLeftPos = false;
bool blockLeftNeg = false;
bool blockRightPos = false;
bool blockRightNeg = false;

// Flags fot direction of travel of the rocket, true = pos = up
bool dirL;
bool dirR;

// settings from gui, defaulft
bool inverseSticks = false;
float rocketVelocity = 1;  //from 0 to 1
int latency = 0;           //ms
bool randomInverseSticks = false;
bool randomRocketVelocity = false;
bool randomLatency = false;
bool gameActive = false;

// coordinates of the rocket
int coords[2];

// enum for the different modes
enum Modes {
  INITIALIZATION_MODE,
  TRANSPORT_MODE,
  PLAYER_MODE,
  ERROR_MODE,
  ORIGIN_MODE,
  EJECT_MODE
};
// defaulft mode
Modes mode = PLAYER_MODE;

void setup() {
  // dc motor entcoder
  pinMode(C1L, INPUT);
  pinMode(C2L, INPUT);
  pinMode(C1R, INPUT);
  pinMode(C2R, INPUT);
  attachInterrupt(digitalPinToInterrupt(C1L), readEncoderL, RISING);
  attachInterrupt(digitalPinToInterrupt(C1R), readEncoderR, RISING);

  // dc motors pwm
  pinMode(ENL, OUTPUT);
  pinMode(ENR, OUTPUT);
  // dc motors direction
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // limit switches
  pinMode(limitSwitchL, INPUT);
  pinMode(limitSwitchR, INPUT);
  attachInterrupt(digitalPinToInterrupt(limitSwitchL), readLimitSwitchL, FALLING);
  attachInterrupt(digitalPinToInterrupt(limitSwitchR), readLimitSwitchR, FALLING);

  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  checkForInput();
  getCoords();
  blockCheck();
  executemode(analogRead(joystickL), analogRead(joystickR));
}

void checkForInput() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    if (input == "COORDS") {
      sendCoords();
      return;
    } else if (input == "ID") {
      Serial.println("chaesAntrieb");
      return;
    } else if (input == "EJECTPOS") {
      mode = EJECT_MODE;
      return;
    } else if (input == "STARTPOS") {
      mode = ORIGIN_MODE;
      return;
    } else if (input == "TRANSPORT") {
      mode = TRANSPORT_MODE;
      return;
    } else if (input == "null") {
      mode = INITIALIZATION_MODE;
      return;
    } else if (input == "reset") {
      mode = INITIALIZATION_MODE;
      return;
    }

    // Parse the input string
    int firstSlash = input.indexOf('/');
    int secondSlash = input.indexOf('/', firstSlash + 1);
    int thirdSlash = input.indexOf('/', secondSlash + 1);
    int fourthSlash = input.indexOf('/', thirdSlash + 1);
    int fifthSlash = input.indexOf('/', fourthSlash + 1);

    // Check if the input string is valid
    if (fifthSlash != -1) {
      inverseSticks = input.substring(0, firstSlash) == "1";
      rocketVelocity = input.substring(firstSlash + 1, secondSlash).toFloat();
      latency = input.substring(secondSlash + 1, thirdSlash).toInt();
      randomInverseSticks = input.substring(thirdSlash + 1, fourthSlash) == "1";
      randomRocketVelocity = input.substring(fourthSlash + 1, fifthSlash) == "1";
      randomLatency = input.substring(fifthSlash + 1) == "1";
      gameActive = true;
    }
  }
}

void executemode(int jValL, int jValR) {
  switch (mode) {
    case INITIALIZATION_MODE:
      findCoordOrigin();
      break;
    case TRANSPORT_MODE:
      transportMode();
      break;
    case PLAYER_MODE:
      bool inverse = randomInverseSticks ? random(0, 2) : inverseSticks;
      int speed = round((randomRocketVelocity ? random(0, 2) : rocketVelocity) * MAX_SPEED) * (inverse ? -1 : 1) * (gameActive ? 1 : 0);
      int leftSpeed = (int)round(mapFloat(jValL, MIN_JVALL, MAX_JVALL, -speed, speed));
      int rightSpeed = (int)round(mapFloat(jValR, MIN_JVALR, MAX_JVALR, -speed, speed));
      int lat = randomLatency ? random(0, MAX_LATENCY) : latency;
      delay(lat);
      moveRocket(leftSpeed, rightSpeed);
      break;
    case ORIGIN_MODE:
      moveToStartPos();
      break;
    case EJECT_MODE:
      moveToEjectPos();
      break;
    case ERROR_MODE:
      break;
  }
}

void sendCoords() {
  Serial.println(String(coords[0]) + "/" + String(coords[1]));
}

int* getCoords() {
  int posL, posR;
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    posL = posVL;
    posR = posVR;
  }
  // coordinates
  calculateCoords(BOARD_WIDTH, posL * COORD_SCAL, posR * COORD_SCAL);
  boxCoords(BOARD_WIDTH / 2, -BOARD_WIDTH / 2, 0, BOARD_HIGHT);
}

void blockCheck() {
  blockLeftPos = blockRightPos = (coords[0] + coords[1]) < BOARD_WIDTH;
  blockLeftPos = coords[0] < BOARD_HIGHT;
  blockRightPos = coords[1] < BOARD_HIGHT;
  blockLeftNeg = coords[0] > 0;
  blockRightNeg = coords[1] > 0;
}

void findCoordOrigin() {
  int phase = 0;
  while (phase < 4) {
    switch (phase) {
      case 0:
        phase = approachOrigin(NULL_SPEED1, phase);
        break;
      case 1:
        phase = distanceToOrigin(NULL_SPEED1, phase);
        break;
      case 2:
        phase = approachOrigin(NULL_SPEED2, phase);
        break;
      case 3:
        phase = distanceToOrigin(MAX_SPEED, phase);
        break;
    }
  }
  mode = ORIGIN_MODE;
}

void setMotorState(int in1, int in2, int en, int speed) {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(en, speed);
}
int approachOrigin(int speed, int phase) {
  if (!nullLeft) {
    setMotorState(IN1, IN2, ENL, speed);
  }
  if (!nullRight) {
    setMotorState(IN3, IN4, ENR, speed);
  }
  if (nullLeft && nullRight) {
    posVL = posVR = 0;
    phase++;
  }
  return phase;
}
int distanceToOrigin(int speed, int phase) {
  if (posVL < 50) {
    setMotorState(IN2, IN1, ENL, speed);
  }
  if (posVR < 50) {
    setMotorState(IN4, IN3, ENR, speed);
    delay(2000);
  }
  if (posVL < 50 && posVR < 50) {
    stopMotors();
    nullLeft = nullRight = false;
    phase++;
  }
  return phase;
}

void moveToEjectPos() {
  //move rocket to the eject position
  //to do: moving sequence
}

void moveToStartPos() {
  //move rocket to the start position
  //to do: moving sequence
}

float* calculateCoords(int distance, int left, int right) {
  float angle = (float)(left * distance) / (float)(left * left + right * right);
  coords[0] = round(left * angle);
  coords[1] = round(right * angle);
}

int* boxCoords(int leftBorder, int rightBorder, int lowerBorder,
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
  if (-DEADZONE <= rightSpeed && rightSpeed <= DEADZONE) {
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

void transportMode() {
  while (!blockLeftPos && !blockRightPos) {
    //moveRocket(MAX_SPEED, MAX_SPEED);
  }
}

void readEncoderL() {
  int x = digitalRead(C2L);
  if (x > 0) {
    posVL++;
  } else {
    posVL--;
  }
  /*  
  posVL += (x > 0) ? 1 : -1;
  Serial.print("L: ");
  Serial.println(posVL);
  */
}

void readEncoderR() {
  int x = digitalRead(C2R);
  if (x > 0) {
    posVR++;
  } else {
    posVR--;
  }
  //  posVR += (x > 0) ? 1 : -1;
}

void readLimitSwitchL() {
  stopMotors();
  if (mode != INITIALIZATION_MODE) {
    Serial.println("ERROR LEFT");
    Serial.println("Type in reset to renull the game");
    mode = ERROR_MODE;
  } else {
    nullLeft = true;
  }
}
void readLimitSwitchR() {
  stopMotors();
  if (mode != INITIALIZATION_MODE) {
    Serial.println("ERROR RIGHT");
    Serial.println("Type in reset to renull the game");
    mode = ERROR_MODE;
  } else {
    nullRight = true;
  }
}
void stopMotors() {
  digitalWrite(IN1, false);
  digitalWrite(IN2, false);
  digitalWrite(IN3, false);
  digitalWrite(IN4, false);
}

float mapFloat(long x, long in_min, long in_max, long out_min, long out_max) {
  return (float)(x - in_min) * (out_max - out_min) / (float)(in_max - in_min) + out_min;
}