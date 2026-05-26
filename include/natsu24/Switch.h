#pragma once
// #include <Arduino.h>

#define SWITCH_SIZE 4
bool switch_[SWITCH_SIZE];
int switch_i_ = 0;

class Switch {
    int pin_;
    int i_;

   public:
    Switch(int pin)
        : pin_(pin) {
    }
    void init() {
        i_ = switch_i_++;
        // pinMode(pin_,INPUT);
    }
    bool isPushed() {  // boolを返すときは関数の名前がisから始まる
        // return !digitalRead(pin_);//ボタンを押すとLOWが返ってくる。！をつけるとHIGHになる。
        return switch_[i_];
    }
};
