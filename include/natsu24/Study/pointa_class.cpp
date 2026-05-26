//クラス(C++)とポインタ
#include <iostream>
#include <stdio.h>

using namespace std;

class Pointatest{
    int* b_;
    public:
     Pointatest(int *b)//コンストラクタといって、classの名前と同じにする。*bにaのアドレスを入れる
        :b_(b)//b_にbを代入（aのアドレスを代入）
    {
    }
    
    void set (int new_data){
        *b_ = new_data;//*b_(aのアドレスを実体にしたもの=aのこと)（実体）にnew_dataを代入
    }
};

int main(void){
    // Your code here!
    int a = 0;
     Pointatest pointa(&a);
     pointa.set(2);
     printf("%d", a);//２が出力される
}
