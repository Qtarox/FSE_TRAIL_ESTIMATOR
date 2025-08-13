//
// Created by 25369 on 2025/5/18.
//
#include <stdint.h>
#ifndef KEY_10000CAL_BASIC_OP_H
#define KEY_10000CAL_BASIC_OP_H
void get_xddt(int in, int out, int* xddt);
void get_yddt(int in, int out, int* yddt);
void lst_xor(const int *a,const int *b,int *c,int l1,int l2);
void lst_mul(uint8_t x,int *y,int *lst0);
#endif //KEY_10000CAL_BASIC_OP_H
