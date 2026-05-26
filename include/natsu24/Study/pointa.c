#include <stdio.h>

// ポインタを関数に渡して、関数内から値を変える
//引数に代入すると値だけコピーされる
//voidだからreturunがない
void set(int* b)
{
    //bはaのアドレス
    //*bはaの実体
    *b = 2;//a = 2
    int *c = b; // アドレスをコピー
}
void set2(int b)//bに1が入る
{
    b = 2;//bを1から2に上書き
}

int main(void){
    // Your code here!
    int a = 1;
    int * addr = &a;
    
    //set(&a);//set(addr);と同じ
    //set2(a);
    
    printf("%d",a);//setのときa = 2,set2のときa = 1
    
}
