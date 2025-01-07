#include <Arduino.h>
#include <util/atomic.h>
#include "PIDController.h"
#include <Adafruit_NeoPixel.h>
#include <FireTimer.h>

// Define the pins for the left motor
#define ENR 4   // pmw pin (speed)
#define IN3 24  // direction pin (forward)
#define IN4 25  // direction pin (backward)
#define C1R 18  // interupt (encoder)
#define C2R 19  // interupt (encoder)

// Define the pins for the right motor
#define ENL 5   // pmw pin (speed)
#define IN1 22  // direction pin (forward)
#define IN2 23  // direction pin (backward)
#define C1L 20  // interupt (encoder)
#define C2L 21  // interupt (encoder)

// Define the pins for the joysticks
#define joystickL A0
#define joystickR A1

// Define the pins for the left and right limit switch
#define limitSwitchL 3
#define limitSwitchR 2

// Define the pins for the NeoPixel
#define LED_BOARDER_PIN 9
#define LED_RING_PIN 10

// Define the number of LEDs
#define NUMPIXELS_BOARDER 131
#define NUMPIXELS_RING 22

// Constants
const long MIN_JVALR = 370;  // min value for joysticks
const long MIN_JVALL = 355;
const long MAX_JVALR = 725;  //  max value for joysticks
const long MAX_JVALL = 650;

const int BOARD_WIDTH = 533;
const int FEED_THROUGH_OFFSETX = 100;
const int FEED_THROUGH_OFFSETY = 100;
const int BOARD_HIGHT = 770;
const int WIRE_LENGHT = 1000;
const int COORD_SCAL = 1;  // mm = steps / SCAL
const int LIMIT_SWITCH_HIGHT = 770;
const int COORD_NULL_OFFSETY = 150; //needs finetuning

const long MAX_SPEED = 255;   // Maximum speed for the motors
const int NULL_SPEED1 = 100;  // nulling speeds
const int NULL_SPEED2 = 60;

const int DEADZONE = 50;       // deadzone for the joysticks
const int MAX_LATENCY = 1000;  // max latency in ms

//positions
const int EJECT_POS[2] = { 0, -10 };
const int NULLING_POS[2] = { 0, -50 };
const int RADIUS_TO_START = 10;

// Volatile variables
volatile int posVL = 0;  // position of the left motor
volatile int posVR = 0;  // position of the right motor

// Flags for nulling the coordinates
bool nullLeft = false;
bool nullRight = false;
int phase = 0;

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
bool gameActive = true;

// coordinates of the rocket
int coords[2];

// enum for the different modes
enum Modes {
  INITIALIZATION_MODE,
  TRANSPORT_MODE,
  PLAYER_MODE,
  ERROR_MODE,
  ORIGIN_MODE,
  EJECT_MODE,
  DEMO_MODE
};
// defaulft mode
Modes mode = PLAYER_MODE;

// PID Settings
float error, integral, derivative, previousError;

// NeoPixel Objects
Adafruit_NeoPixel boarderStrip(NUMPIXELS_BOARDER, LED_BOARDER_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel ringStrip(NUMPIXELS_RING, LED_RING_PIN, NEO_GRB + NEO_KHZ800);

// NeoPixel Elements
int initialisationCounter = 0;
int colorCounter = 0;
bool wave = false;
int waveCounter = 0;
int random1, random2, random3, random4, random5;
FireTimer waveTimer;
bool change = true;
uint32_t colorR;
uint32_t colorB;
bool on = false;

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

  // Setting up the NeoPixel
  boarderStrip.begin();
  ringStrip.begin();
  boarderStrip.show();
  ringStrip.show();
  boarderStrip.setBrightness(100);
  ringStrip.setBrightness(50);
  allGreen();

  waveTimer.begin(2000);

  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  checkForInput();
  getCoords();
  Serial.print(coords[0]) + Serial.println(coords[1]);
  /*Serial.print("R: ");
  Serial.println(posVR);
  Serial.print("L: ");
  Serial.println(posVL);*/
  blockCheck();
  executemode();
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
    } else if (input == "null" || input == "reset") {
      mode = INITIALIZATION_MODE;
      return;
    } else if (input == "play") {
      mode = PLAYER_MODE;
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

void executemode() {
  switch (mode) {
    case INITIALIZATION_MODE:
      findCoordOrigin();
      ledInitialisation();
      break;
    case TRANSPORT_MODE:
      transportMode();
      break;
    case PLAYER_MODE:
      playerMode();
      playLED();
      break;
    case ORIGIN_MODE:
      moveToStartPos();
      break;
    case EJECT_MODE:
      moveToEjectPos();
      break;
    case ERROR_MODE:
      ledError();
      break;
  }
}

void playerMode() {
  // Read the joystick values and set the speed of the motors
  bool inverse = randomInverseSticks ? random(0, 2) : inverseSticks;
  float velocity = randomRocketVelocity ? random(0, 2) : rocketVelocity;
  int baseSpeed = round(velocity * MAX_SPEED);
  int adjustedSpeed = baseSpeed * (inverse ? -1 : 1) * (gameActive ? 1 : 0);

  int joystickLValue = analogRead(joystickL);
  int joystickRValue = analogRead(joystickR);

  int leftSpeed = (int)round(mapFloat(joystickLValue, MIN_JVALL, MAX_JVALL, -adjustedSpeed, adjustedSpeed));
  int rightSpeed = (int)round(mapFloat(joystickRValue, MIN_JVALR, MAX_JVALR, -adjustedSpeed, adjustedSpeed));

  int latency = randomLatency ? random(0, MAX_LATENCY) : latency;

  //delay(latency);
  moveRocket(leftSpeed, rightSpeed);
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
  calculateCoords(BOARD_WIDTH + (2 * FEED_THROUGH_OFFSETX), posL / COORD_SCAL, posR / COORD_SCAL);
  //boxCoords(BOARD_WIDTH / 2, -BOARD_WIDTH / 2, 0, BOARD_HIGHT);
}

void blockCheck() {
  blockLeftPos = blockRightPos = (coords[0] + coords[1]) < BOARD_WIDTH;
  blockLeftPos = coords[0] < BOARD_HIGHT;
  blockRightPos = coords[1] < BOARD_HIGHT;
  blockLeftNeg = coords[0] > 0;
  blockRightNeg = coords[1] > 0;
}

void findCoordOrigin() {
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
    case 4:
      Serial.println("Vier");
      mode = EJECT_MODE;
      break;
  }
}

void setMotorState(int in1, int in2, int en, int speed) {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(en, speed);
}

int approachOrigin(int speed, int phaseR) {
  Serial.println("IJSd");
  if (!nullLeft) {
    setMotorState(IN1, IN2, ENL, speed);
  }
  if (!nullRight) {
    setMotorState(IN3, IN4, ENR, speed);
  }
  if (nullLeft && nullRight) {
    int cableLength = round(sqrt((FEED_THROUGH_OFFSETY + BOARD_HIGHT + COORD_NULL_OFFSETY)^2 + (BOARD_WIDTH/2+FEED_THROUGH_OFFSETX)^2)*COORD_SCAL);
    posVL = posVR = cableLength;
    phaseR++;
  }
  return phaseR;
}
int distanceToOrigin(int speed, int phaseD) {
  Serial.println(phaseD);
  if (posVL <= 100) {
    setMotorState(IN2, IN1, ENL, speed);
  }
  if (posVR <= 100) {
    setMotorState(IN4, IN3, ENR, speed);
  }

  if (posVL > 100 && posVR > 100) {
    Serial.println("O");
    stopMotors();
    nullLeft = nullRight = false;
    phaseD++;
  }
  Serial.println(phaseD);
  return phaseD;
}

void moveToEjectPos() {
  bool left = true;
  int goalDistance = (FEED_THROUGH_OFFSETX + (BOARD_WIDTH / 2) + EJECT_POS[0]) ^ 2 + (FEED_THROUGH_OFFSETY + BOARD_HIGHT - EJECT_POS[1]) ^ 2;
  int deltaLeft = posVL - goalDistance;
  int deltaRight = posVR - goalDistance;
  regulateSpeed(deltaLeft, left);
  regulateSpeed(deltaRight, !left);
}

void moveToStartPos() {
  bool left = true;
  int goalDistance = (FEED_THROUGH_OFFSETX + (BOARD_WIDTH / 2)) ^ 2 + (FEED_THROUGH_OFFSETY + BOARD_HIGHT) ^ 2;
  int deltaLeft = posVL - goalDistance;
  int deltaRight = posVR - goalDistance;
  if (posVL < RADIUS_TO_START) {
    setMotorState(IN2, IN1, ENL, MAX_SPEED);
  }
  regulateSpeed(deltaLeft, left);
  regulateSpeed(deltaRight, !left);
}

void regulateSpeed(int delta, bool left) {
  int speed = PIDController(delta);
  if (delta > 0) {
    if (left) {
      setMotorState(IN1, IN2, ENL, speed);
    } else {
      setMotorState(IN3, IN4, ENR, speed);
    }
  } else if (delta < 0) {
    if (left) {
      setMotorState(IN2, IN1, ENL, speed);
    } else {
      setMotorState(IN4, IN3, ENR, speed);
    }
  } else {
    if (left) {
      setMotorState(IN1, IN2, ENL, 0);
    } else {
      setMotorState(IN3, IN4, ENR, 0);
    }
  }
}

float* calculateCoords(int distance, int left, int right) {
  //Kathetensatz und Höhensatz von Euklid
  int p = left * left / distance;
  int q = right * right / distance;
  int h = sqrt(p*q);
  coords[0] = BOARD_WIDTH / 2 + FEED_THROUGH_OFFSETX - p;
  coords[1] = BOARD_HIGHT + FEED_THROUGH_OFFSETY - h;
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
  /*
  if ((dirL && blockLeftPos) || (!dirL && blockLeftNeg)) {
    digitalWrite(IN1, false);
    digitalWrite(IN2, false);
    analogWrite(ENL, 0);
    Serial.println("OSDKJ");
  } else {
    */
  analogWrite(ENL, abs(leftSpeed));
  /*}
  if ((dirR && blockRightPos) || (!dirR && blockRightNeg)) {
    digitalWrite(IN3, false);
    digitalWrite(IN4, false);
    analogWrite(ENR, 0);
  } else {*/
  analogWrite(ENR, abs(rightSpeed));
  //}
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
}

void readEncoderR() {
  int x = digitalRead(C2R);
  if (x > 0) {
    posVR--;
  } else {
    posVR++;
  }
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

void allGreen() {
  for (int i = 0; i < NUMPIXELS_BOARDER; i++) {
    boarderStrip.setPixelColor(i, boarderStrip.Color(0, 255, 0));
  }
  for (int i = 0; i < NUMPIXELS_RING; i++) {
    ringStrip.setPixelColor(i, ringStrip.Color(0, 255, 0));
  }
  ringStrip.show();
  boarderStrip.show();
}

void ledError() {
  if (!on) {
    for (int i = 0; i < NUMPIXELS_BOARDER; i++) {
      boarderStrip.setPixelColor(i, boarderStrip.Color(255, 0, 0));
      ringStrip.show();
    }
    for (int i = 0; i < NUMPIXELS_RING; i++) {
      ringStrip.setPixelColor(i, ringStrip.Color(255, 0, 0));
      boarderStrip.show();
      on = true;
    }
  }
}

void playLED() {
  if (waveTimer.fire() && !wave) {
    wave = true;
    random1 = random(100, 250);
    random2 = random(50, 250);
    random3 = random(0, 150);
    random4 = random(1, 200);
    random5 = random(1, 30);
    waveTimer.update(random(1000, 3000));
  }
  if (wave == true) {
    createWave();
  } else {
    for (int i = 0; i < NUMPIXELS_BOARDER; i++) {
      boarderStrip.setPixelColor(i, boarderStrip.Color(255, 255, 255));
    }
    for (int i = 0; i < NUMPIXELS_RING; i++) {
      ringStrip.setPixelColor(i, ringStrip.Color(255, 0, 0));
    }
    ringStrip.show();
    boarderStrip.show();
  }
}

void createWave() {
  if (waveCounter % random4 == 0) {
    if (waveCounter / random4 < NUMPIXELS_BOARDER + random5) {
      boarderStrip.setPixelColor(waveCounter / random4, boarderStrip.Color(255 - random1, 255 - random2, 255 - random3));
      boarderStrip.setPixelColor(waveCounter / random4 - random5, boarderStrip.Color(255, 255, 255));
    }
    if (waveCounter / random4 == NUMPIXELS_BOARDER + random5) {
      wave = false;
      waveCounter = 0;
    }
    boarderStrip.show();
  }
  waveCounter++;
}

void ledInitialisation() {
  on = false;
  const uint32_t colors[7][3] = {
    { 255, 0, 0 }, { 0, 255, 0 }, { 0, 0, 255 }, { 255, 255, 0 }, { 255, 0, 255 }, { 0, 255, 255 }, { 255, 255, 255 }
  };

  colorR = ringStrip.Color(colors[colorCounter][0], colors[colorCounter][1], colors[colorCounter][2]);
  colorB = boarderStrip.Color(colors[colorCounter][0], colors[colorCounter][1], colors[colorCounter][2]);

  if (initialisationCounter == 0) {
    ringStrip.clear();
    boarderStrip.clear();
  } else if (initialisationCounter % 5 == 0 && initialisationCounter / 5 < NUMPIXELS_BOARDER) {
    boarderStrip.setPixelColor((initialisationCounter / 5 - 1), colorB);
  } else if (initialisationCounter >= NUMPIXELS_BOARDER && initialisationCounter % 5 != 0) {
    ringStrip.setPixelColor((initialisationCounter / 5) - NUMPIXELS_BOARDER, colorR);
  }

  if (initialisationCounter / 5 == NUMPIXELS_RING + NUMPIXELS_BOARDER) {
    initialisationCounter = 0;
    colorCounter = (colorCounter + 1) % 7;
  }
  boarderStrip.show();  // Update strip with new contents
  ringStrip.show();     // Update strip with new contents
  initialisationCounter++;
}



int PIDController(float delta) {
  float Kp = 1.0;                     // Proportional gain
  float Ki = 0.0;                     // Integral gain
  float Kd = 0.0;                     // Derivative gain
  float maxSpeed = (float)MAX_SPEED;  // Maximum speed for the motors
  error = delta;
  integral += error;
  derivative = error - previousError;
  int speed = Kp * error + Ki * integral + Kd * derivative;
  speed = constrain(abs(speed), 0, maxSpeed);  // Begrenze die Geschwindigkeit auf maxSpeed
  previousError = error;
  return speed;
}