#include "ArmCalculator.h"

// Constructor
ArmCalculator::ArmCalculator(float distanceCenter, float lengthArm, float angleOverCenter) 
  : _distanceCenter(distanceCenter), _lengthArm(lengthArm), _angleOverCenter(angleOverCenter) {
  
  _pi = 3.14159;
  _minAngle = _pi / 180 * (-_angleOverCenter);
  _maxAngle = _pi / 180 * (180 - _angleOverCenter);
}

// Public method to calculate angle PWM
float ArmCalculator::angleForPosition(float x, float y, String side) {
  float x1, wtotal;
  float anglePWM;

  // Adjust x1 based on the side
  if (side == "Minus") {
    x1 = x + (_distanceCenter / 2);
  } else if (side == "Plus") {
    x1 = x - (_distanceCenter / 2);
  } else {
    Serial.println("Incorrect Input");
    return -1;  // Return error value if side is incorrect
  }

  // Calculate angles
  float w1 = atan(x1 / y);
  float w2 = acos(sqrt((x1 * x1) + (y * y)) / (2 * _lengthArm));

  // Adjust total angle based on the side
  if (side == "Minus") {
    wtotal = w2 - w1;
    anglePWM = mapFloat(wtotal, _minAngle, _maxAngle, 2500, 500);
  } else if (side == "Plus") {
    wtotal = w2 + w1;
    anglePWM = mapFloat(wtotal, _minAngle, _maxAngle, 500, 2500);
  } else {
    Serial.println("Incorrect Input");
    return -1;  // Return error value if side is incorrect
  }
  return anglePWM;
}

// Public Method to calculate distance and time for move, based on velocity
float ArmCalculator::timeForMove(int velocity, float currentX, float currentY, float targetX, float targetY){

  // Units		: Koordinaten : mm
  //            Distanzen   : mm
  //            Zeit        : ms oder us für Taktzeit Servo
  //            Geschw.     : mm/s
  //            

  // shortest distance variables
  float deltaX, deltaY;

  if (currentX > targetX) {
    deltaX = currentX - targetX;
  } else {
    deltaX = targetX - currentX;
  }
  
  //Serial.print("deltaX: ");
  //Serial.println(deltaX);

  if (currentY > targetY) {
    deltaY = currentY - targetY;
  } else {
    deltaY = targetY - currentY;
  }
  
  //Serial.print("deltaY: ");
  //Serial.println(deltaY);

  // Calculation of diagonal distance
  int distance = sqrt((pow(deltaX, 2) + pow(deltaY, 2)));
  
  //Serial.print("distance: ");
  //Serial.println(distance);
  
  // Calculate Time
  // Faktor 1000 um von Sekunden zu Millisekkunden zu kommen
  float temp = (float)distance / velocity;
  //Serial.print("Temp value: ");
  //Serial.println(temp);
  float moveTime = temp * 1000;

  return moveTime;
}

long ArmCalculator::t_inc(int moveTime, int angleIncrement, int deltaAngle){

  // Einheiten: time  : ms
  //            deltaAngle: us
  //            angleIncrement: us // Änderung des PWM Signals für die Servo Position

  long t_inc = (long)angleIncrement * moveTime / deltaAngle; // Beschreibt die Zeit, die zwischen den Iterationen der neuen Winkel gewartet werden muss

  return t_inc;
}

// Private method for mapping a float value from one range to another
float ArmCalculator::mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
