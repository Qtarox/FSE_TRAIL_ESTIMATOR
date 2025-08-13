//
// Created by 25369 on 2025/5/18.
//
#include "GF28.h"
uint8_t gf_mul(uint8_t a1,uint8_t b1) {
    int a=a1,b=b1;
    uint8_t result = 0;
    while(b){
        if (b & 1)  {result ^= a;}
        a <<= 1;
        if (a & 0x100) a ^= 0x11b;
        b >>= 1;}
    return (result & 0xFF);
}