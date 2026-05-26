#include <iostream>
using namespace std;

class Aim{
    public:
    float x;
    
    Aim(){}
    
};

int main(void){
    // Your code here!
//Class名　変数名
    Aim aim;
//変数名.x aimのxに１を代入
    aim.x = 1;
    
    float x2 = aim.x;//x2に１を代入
    
    Aim* addr = &aim;//Aimというclassのポインタ型addrにaimのアドレスを代入
//    aim  .x = 2
    (*addr).x = 2;//addrという実体(aim)のxに2を代入
    addr->x = 3;//addrという実体のxに3を代入
}
