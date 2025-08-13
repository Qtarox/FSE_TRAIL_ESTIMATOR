//
// Created by 25369 on 2025/5/17.
//
#include "GF28.h"
int gf_mul(int a,int b) {
    int result = 0;
    while(b){
        if (b & 1)  {result ^= a;}
    a <<= 1;
    if (a & 0x100) a ^= 0x11b;
    b >>= 1;}
    return (result & 0xFF);
}