#include <Arduino.h>
#include <FireTimer.h>
#include <ArmCalculator.h>
#include <Servo.h>


// Global Variables:
int currentAnglePlus; // Best case: Store as PWM
int currentAngleMinus; // Best case: Store as PWM

int targetAnglePlus; // Best case: Store as PWM
int targetAngleMinus; // Best case: Store as PWM

bool servoMinusDirection; // Direction of the servo. True = from 500 to 2500, false = from 2500 to 500
bool servoPlusDirection; // same

int angleIncrement = 10; // Increment in PWM

int currentX; // Does this actually have to be a global variable?
int currentY;

int velocity;

int targetX;
int targetY;

bool targetChanged = true; // Has to be true to trigger the calculations for the first time.

int mode; // holds the current Mode. This is partially set by the serial input
// e.g. 1 = STOP, 2 = ORIGIN, 3 = TRAVEL, 4 = TRANSPORT, 5 = IDLE 

// Objects
ArmCalculator calculator;

Servo servoMinus;
Servo servoPlus;

FireTimer intervalServoMinus;
FireTimer intervalServoPlus;

int i;

void setup(){

  Serial.begin(9600);
  Serial.setTimeout(10);

  servoMinus.attach(9, 500, 2500);
  servoPlus.attach(10, 500, 2500);

  // implement servo write last known servo positions from EEPROM soon. For now:

  currentX = 0;
  currentY = 300;

  currentAngleMinus = calculator.angleForPosition(currentX, currentY, "Minus");
  currentAnglePlus = calculator.angleForPosition(currentX, currentY, "Plus");

  //Serial.print("cAngleMinus: ");
  //Serial.println(currentAngleMinus);

  //Serial.print("cAnglePlus: ");
  //Serial.println(currentAnglePlus);

  servoMinus.writeMicroseconds(currentAngleMinus);
  servoPlus.writeMicroseconds(currentAnglePlus);

  origin();
  i = 0;
}

void loop(){
	checkForInput();/*
	if (targetChanged) {
		calculate();
		targetChanged = false;
	}
	drive();*/
}

void setCoordinates(){
  int coordinateArryX [4] = {0, 220, -220, 200};
  int coordinateArryY [4] = {400, 300, 400, 600};
  
  if (currentX != coordinateArryX[i]){
    targetX = coordinateArryX[i];
    targetY = coordinateArryY[i];
    targetChanged = true;
  }

  if (currentX == targetX){
    i++;
  }

  if(i == 4){
    i = 0;
  }
  

}

void checkForInput() {
	// Basically just a SerialRead Function which looks for the following inputs:
	// STOP: Halt the Arms exactly where they are
	// ORIGIN: Set the Arms to the starting position
	// x/y/v: Coordinates, seperated by a slash. Set them as new Target coordinates. This part should also test if the coordinates are 'legal'
	// trans: Set the TransportMode
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    if (input == "ID") {
      Serial.println("chaesZielsystem");
      return;
    }
    // Check if input is in x/y or x/y/velocity format
    int firstSlash = input.indexOf('/');
    int secondSlash = input.indexOf('/', firstSlash + 1);

    if (firstSlash != -1) {
      String xCoordStr = input.substring(0, firstSlash);
      String yCoordStr;
      String velocityStr;
      float x;
      float y;
      int tempVelocity;

      if (secondSlash != -1) {
        // Input is in x/y/velocity format
        yCoordStr = input.substring(firstSlash + 1, secondSlash);
        velocityStr = input.substring(secondSlash + 1);

        x = xCoordStr.toInt();
        y = yCoordStr.toInt();
        tempVelocity = velocityStr.toInt();

        Serial.print("Registered X: ");
        Serial.println(x);

        Serial.print("Registered Y: ");
        Serial.println(y);

        Serial.print("Registered velocity: ");
        Serial.println(velocity);


        if (isLegalCoordinate(x, y)) {
          mode = 3;
          targetX = x;
          targetY = y;
          velocity = tempVelocity;
          targetChanged = true;
        } else {
          Serial.println("Error: Illegal coordinates");
        }
      }
    } else if (input == "STOP") {
      mode = 1;
    } else if (input == "ORIGIN") {
      mode = 2;
      targetChanged = true;
    } 
    else if (input == "trans") {
      mode = 4; // Transport Mode
    } else if (input == "INFO") {
      Serial.print("targetAnglePlus: ");
      Serial.println(targetAnglePlus);
      Serial.print("targetAngleMinus: ");
      Serial.println(targetAngleMinus);
      Serial.print("currentAnglePlus: ");
      Serial.println(currentAnglePlus);
      Serial.print("currentAngleMinus: ");
      Serial.println(currentAngleMinus);
      Serial.print("target Coordinates: ");
      Serial.print(targetX);
      Serial.print(" / ");
      Serial.println(targetY);
      Serial.print("current Coordinates: ");
      Serial.print(currentX);
      Serial.print(" / ");
      Serial.println(currentY);
      Serial.print("Mode: ");
      Serial.println(mode);
      Serial.println("Info: 1 = STOP, 2 = ORIGIN, 3 = TRAVEL, 4 = TRANSPORT, 5 = IDLE");
      Serial.println("");
    }  
    else {
      //Serial.println("Error: Unknown command");
    }
  }
}

// Function to validate coordinates
bool isLegalCoordinate(int x, int y) {
    // Replace these with the actual valid ranges for x and y
    int minX = -250, maxX = 250;
    int minY = 200, maxY = 600;

    bool xValid = (x >= minX && x <= maxX);
    //Serial.print("xValid: ");
    //Serial.println(xValid);

    bool yValid = (y >= minY && y <= maxY);
    //Serial.print("yValid: ");
    //Serial.println(yValid);

    return (x >= minX && x <= maxX) && (y >= minY && y <= maxY);
}


void drive(){
	switch (mode) {
		case 1:
			// STOP
      servoMinus.writeMicroseconds(currentAngleMinus);
      servoPlus.writeMicroseconds(currentAnglePlus);
			break;
		case 2: 
			// origin
			break;
		case 3:
			// TRAVEL
      travel();
			break;
		case 4:
			// transport
			break;
		case 5:
			// IDLE
			break;
  }
}

void stop() {
	// Write the current PWM to the Servo and dont update the variable
}

void origin(){
	// Go to the Origin with a predefined speed. Once there, set mode to IDLE
	// To decide: Should this action be haltable? Yes i think so. Maybe only through emergency halt and not through the input of new variables though.
  targetX = 0;
  targetY = 400;
  velocity = 300;
  targetChanged = true;

  mode = 3;
}

void travel(){
	// Go to the target PWM signals with a variable speed, once there, set mode to IDLE.
	// This process should be haltable whenever
  if (intervalServoMinus.fire()){
    //Serial.println("Entered Minus Interval");
    // Add PWm increment to current PWM
    int newAngle = newPWM(servoMinusDirection, targetAngleMinus, currentAngleMinus);
    // Minus servo 'step' forward
    servoMinus.writeMicroseconds(newAngle);
    // Save new PWM
    currentAngleMinus = newAngle;
  }
  if (intervalServoPlus.fire()){
    //Serial.println("Entered Plus Interval");
    // Add PWm increment to current PWM
    int newAngle = newPWM(servoPlusDirection, targetAnglePlus, currentAnglePlus);
    // Minus servo 'step' forward
    servoPlus.writeMicroseconds(newAngle);
    // Save new PWM
    currentAnglePlus = newAngle;
  }
  delay(1);
}

int newPWM(bool direction, int targetPWM, int currentPWM){
  int newPWM;
  if (direction) {
    if ((currentPWM + angleIncrement) < targetPWM){
      newPWM = currentPWM + angleIncrement;
    } else {
      newPWM = targetPWM;
      currentX = targetX;
      currentY = targetY;
      mode = 5;
    }
  } else {
    if ((currentPWM - angleIncrement) > targetPWM){
      newPWM = currentPWM - angleIncrement;
    } else {
      newPWM = targetPWM;
      currentX = targetX;
      currentY = targetY;
      mode = 5;
    }
  }
  //delay(10);
  //debugInt("newPWM: ", newPWM);
  return newPWM;
}


void calculate() {
	// Do all the calculations. This means take in the current and target coordinates. Calculate the required PWM signals for those coordinates.
  // This will also calcultate the speeds for the different Motors and set the intervals.
  targetAnglePlus = calculator.angleForPosition(targetX, targetY, "Plus");
  targetAngleMinus = calculator.angleForPosition(targetX, targetY, "Minus");

  Serial.print("targetAnglePlus: ");
  Serial.println(targetAnglePlus);

  Serial.print("targetAngleMinus: ");
  Serial.println(targetAngleMinus);

  debugInt("velocity: ", velocity);
  float timeForMove = calculator.timeForMove(velocity, currentX, currentY, targetX, targetY);

  Serial.print("time for move: ");
  Serial.println(timeForMove);

  // determine directions:
  if (currentAnglePlus < targetAnglePlus){
    servoPlusDirection = true;
  } else {
    servoPlusDirection = false;
  }
  if (currentAngleMinus < targetAngleMinus){
    servoMinusDirection = true;
  } else {
    servoMinusDirection = false;
  }

  int deltaAnglePlus = abs(currentAnglePlus - targetAnglePlus);
  int deltaAngleMinus = abs(currentAngleMinus - targetAngleMinus);

  Serial.print("deltaAnglePlus: ");
  Serial.println(deltaAnglePlus);

  Serial.print("deltaAngleMinus: ");
  Serial.println(deltaAngleMinus);

  // Set the respective Firetimers
  long t_inc_Minus = calculator.t_inc(timeForMove, angleIncrement, deltaAngleMinus);
  long t_inc_Plus = calculator.t_inc(timeForMove, angleIncrement, deltaAnglePlus);

  Serial.print("t_inc_M: ");
  Serial.println(t_inc_Minus);

  Serial.print("t_inc_P: ");
  Serial.println(t_inc_Plus);

  intervalServoMinus.begin(t_inc_Minus);
  intervalServoPlus.begin(t_inc_Plus);
}

void debugInt(String message, int value){
  Serial.print(message);
  Serial.println(value);
}