#include <iostream>
using namespace std;

class Motor {
    public:
        float vel;
        
        Motor(){}
        void init(){
            setSpeed(0);
        }
        void setSpeed(float omega){
            vel = omega;
        }
    
};

class OmniDrive {
    
    Motor *m1_, *m2_, *m3_, *m4_;
    
    public:
    OmniDrive(float wheel_base, float wheel_radius, Motor *m1, Motor *m2, Motor *m3, Motor *m4)
        : m1_(m1),
          m2_(m2),
          m3_(m3),
          m4_(m4)
        {
            setRobotSpeed(0,0,0,0);
        }
    void setRobotSpeed(float vx, float vy, float vt, float t){ 
        float omega;
        m1_->setSpeed(omega);
        m2_->setSpeed(omega);
        m3_->setSpeed(omega);
        m4_->setSpeed(omega);
        
    }
    

    
};
Motor m1, m2, m3, m4;
OmniDrive omni_drive(0.193, 0.05, &m1, &m2, &m3, &m4);    
int main(void){
    // Your code here!
   
    
    
}
