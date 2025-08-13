//
// Created by 25369 on 2024/12/22.
//
#include <stdint.h>
#include <cinttypes>
#include "stdio.h"
#ifndef NEW_C_K_SCH_H
#define NEW_C_K_SCH_H
void show_key(uint8_t* key);
void key_shift(uint8_t* key);//key is a 80 bit array
//void SubKey(uint8_t* key);
//void ADDrd(uint8_t* key,int i);
void get_key(const uint8_t* key, uint8_t* round_key,int rn);
void key_sch(uint8_t* key,int i);
#endif //NEW_C_K_SCH_H
