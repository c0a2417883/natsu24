#pragma once

float motor_vel[4] = {0};

int motor_i_ = 0;

class Motor2 {
    int addr_;
    int i_;

   public:
    Motor2(int addr)
        : addr_(addr) {
    }

    void init() {
        i_ = motor_i_++;
        setSpeed(0, 0);
    }
    void setSpeed(float omega1, float omega2) {
        motor_vel[i_ * 2] = omega1;
        motor_vel[i_ * 2 + 1] = omega2;
    }
};
