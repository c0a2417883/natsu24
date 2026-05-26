#pragma once
#include <cmath>

class Encoder {
   public:
    Encoder() {
    }

    void init() {
    }
    int cnt[2];
    void getCounts(int & cnt1,int & cnt2){
        cnt1 = cnt[0];
        cnt2 = cnt[1];
    }
};
