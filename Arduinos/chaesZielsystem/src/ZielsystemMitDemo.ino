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

int velocity; // in mm/s. This is a pseudo velocity as it does not take in to a account the actual path but rather the hypothenuse between two points

int targetX;
int targetY;

float stretchX = 1.1;
int offsetY = 50;

bool targetChanged = true; // Has to be true to trigger the calculations for the first time.

int mode; // holds the current Mode. This is partially set by the serial input
// e.g. 1 = STOP, 2 = ORIGIN, 3 = TRAVEL, 4 = TRANSPORT, 5 = IDLE, 6 = DEMO

bool demoEnabled = false;
 
// Objects
ArmCalculator calculator;

Servo servoMinus;
Servo servoPlus;

FireTimer intervalServoMinus;
FireTimer intervalServoPlus;

void setup(){

  Serial.begin(9600);
  Serial.setTimeout(10);

  pinMode(12, OUTPUT); // Relais Pin
  digitalWrite(12, HIGH); // Turn off Power to Servos

  servoMinus.attach(9, 500, 2500);
  servoPlus.attach(10, 500, 2500);

  currentX = 200;
  currentY = 200;

  currentAngleMinus = calculator.angleForPosition(currentX, currentY, "Minus");
  currentAnglePlus = calculator.angleForPosition(currentX, currentY, "Plus");

  //Serial.print("cAngleMinus: ");
  //Serial.println(currentAngleMinus);

  //Serial.print("cAnglePlus: ");
  //Serial.println(currentAnglePlus);

  servoMinus.writeMicroseconds(currentAngleMinus);
  servoPlus.writeMicroseconds(currentAnglePlus);

  origin();
  digitalWrite(12, LOW); // Enable Power to Servos
}

void loop(){
	checkForInput();
	if (targetChanged) {
		calculate();
		targetChanged = false;
	}
	drive();
}

void checkForInput() {
	// Basically just a SerialRead Function which looks for the following inputs:
	// STOP: Halt the Arms exactly where they are
	// ORIGIN: Set the Arms to the starting position
	// x/y: Coordinates, seperated by a slash. Set them as new Target coordinates. This part should also test if the coordinates are 'legal'
	// TRANS: Set the TransportMode

  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Read input until newline
    input.trim();  // Remove any whitespace

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

        x = xCoordStr.toInt() * stretchX;
        y = yCoordStr.toInt() + offsetY;
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
    else if (input == "TRANS") {
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
    } else if(input == "DEMO") {
      demoEnabled = true;
      mode = 6;
    } else if (input == "ID"){
      Serial.println("chaesZielsystem");
    }
    else {
      Serial.println("Error: Unknown command");
    }
  }
}

// Function to validate coordinates
bool isLegalCoordinate(int x, int y) {
    // Replace these with the actual valid ranges for x and y
    int minX = -255, maxX = 255;
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
      stop();
			break;
		case 2: 
			// origin
      origin();
			break;
		case 3:
			// TRAVEL
      travel();
			break;
		case 4:
			// transport
      transport();
			break;
		case 5:
			// IDLE
      if (demoEnabled){
        mode = 6;
      }
			break;
    case 6: 
      // DEMO IDLE FUNCTION
      demo();
      break;
  }
}

void stop() {
	// Write the current PWM to the Servo and dont update the variable
  demoEnabled = false;
  servoMinus.writeMicroseconds(currentAngleMinus);
  servoPlus.writeMicroseconds(currentAnglePlus);
  //getCurrentXandY(); // This does not yet work, but it is not important as it would not make a noticeable difference either way.
}

void origin(){
	// Go to the Origin with a predefined speed. Once there, set mode to IDLE
	// To decide: Should this action be haltable? Yes i think so. Maybe only through emergency halt and not through the input of new variables though.
  demoEnabled = false;
  targetX = 0;
  targetY = 400;
  velocity = 300;
  targetChanged = true;

  mode = 3;
}

void transport(){

  demoEnabled = false;

  targetX = 200;
  targetY = 200;
  velocity = 300;
  targetChanged = true;

  mode = 3;
}

void demo(){
  targetX = random(-200, 200);
  targetY = random(200, 600);

  velocity = 200;

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

void getCurrentXandY(){
  // THIS RETURNS INCORRECT VALUES
  float a1 = calculator.getAngleFromPWM(currentAnglePlus, "Plus");
  debugInt("a1: ", a1);
  float a2 = calculator.getAngleFromPWM(currentAngleMinus, "Minus");
  debugInt("a2: ", a2);
  currentX = calculator.getX(a1, a2);
  currentY = calculator.getY(a1, a2);
  debugInt("X: ", currentX);
  debugInt("Y: ", currentY);
}