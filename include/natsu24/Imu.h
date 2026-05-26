#pragma once

class Imu {
   public:
    Imu(int a) {}
    float yaw;
    void init() {
    }
    float getYaw() {
        return yaw;
    }
};
