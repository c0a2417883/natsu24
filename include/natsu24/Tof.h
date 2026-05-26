#pragma once
// #include <Arduino.h>

class Tof{
  public:
  float distance[4];
  Tof(){}
  void init(){

  }
  float getDistance(int i){
    return distance[i];
  }
};
