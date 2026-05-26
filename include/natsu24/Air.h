#pragma once

class Air {
    int pin_;

   public:
    Air(int pin, int b)
        : pin_(pin) {
    }
    void init() {
        // pinMode(pin_,OUTPUT);
    }
    void expand() {
        // digitalWrite(pin_,HIGH);
    }
    void shrink() {
        // digitalWrite(pin_,LOW);
    }
    void write(bool flag) {
        // digitalWrite(pin_,flag);
    }
};
