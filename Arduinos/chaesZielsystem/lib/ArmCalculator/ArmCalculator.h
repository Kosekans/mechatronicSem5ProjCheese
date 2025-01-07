#ifndef ARM_CALCULATOR_H
#define ARM_CALCULATOR_H

#include "Arduino.h"

class ArmCalculator {
  public:
    ArmCalculator(float distanceCenter = 30.0, float lengthArm = 321.0, float angleOverCenter = 18.5);
    
    float angleForPosition(float x, float y, String side);
    
    float timeForMove(int velocity, float currentX, float currentY, float targetX, float targetY);
    
    long t_inc(int moveTime, int angleIncrement, int deltaAngle);
    
    int getX(float angle1, float angle2);
    
    int getY(float angle1, float angle2);
    
    float getAngleFromPWM(int pwm, String side);

  private:
    float mapFloat(float x, float in_min, float in_max, float out_min, float out_max);
    
    float _distanceCenter;
    float _lengthArm;
    float _angleOverCenter;
    float _pi;
    float _minAngle;
    float _maxAngle;
};

#endif
