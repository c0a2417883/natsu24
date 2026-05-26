#pragma once
#include <bits/stdc++.h>
#include <unistd.h>

#include <chrono>
#include <cstring>

#define BUFF_SIZE 1024

class HardwareSerial {
   public:
    char buf[BUFF_SIZE];
    int n = 0;
    HardwareSerial() {}

    void begin(int baud) {
    }
    void print(const char* message) {
        int len = std::sprintf(buf + n, "%s", message);
        n += len;
    }
    void print(float data) {
        char c[32];
        int len = std::sprintf(c, "%f", data);
        check(len);
        print(c);
    }
    void println(float data) {
        char c[32];
        int len = std::sprintf(c, "%f", data);
        check(len);
        println(c);
    }
    void print(int data) {
        char c[32];
        int len = std::sprintf(c, "%d", data);
        check(len);
        print(c);
    }
    void println(int data) {
        char c[32];
        int len = std::sprintf(c, "%d", data);
        check(len);
        println(c);
    }
    void println(const char* message = "") {
        print(message);
        // buf[n++] = '\n';
    }

   private:
    void check(int len) {
        if ((n + len) >= BUFF_SIZE)
            n = 0;
    }
};

HardwareSerial Serial;

unsigned long micros() {
    using namespace std::chrono;
    unsigned long timestamp = duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
    return timestamp;
}

unsigned long millis() {
    return micros() * 0.001;
}

void delay(unsigned long ms) {
    unsigned long ts = micros();
    ms = ts + ms * 1000;
    while (micros() < ms) {
    }
}

#define constrain(amt, low, high) ((amt) < (low) ? (low) : ((amt) > (high) ? (high) : (amt)))

#define PIN_LED1 0
#define PIN_LED3 0
#define HIGH 1
#define LOW 0
#define OUTPUT 0
void pinMode(int a, int b) {}
void digitalWrite(int a, int b) {}
