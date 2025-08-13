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
void SubKey(uint8_t* key);
void ADDrd(uint8_t* key,int i);
void get_key(const uint8_t* key, uint8_t* round_key);
void key_sch(uint8_t* key,int i);
void key_rf2(uint8_t* key,int ii);
void key_rf(uint8_t* key,int ii);
#endif //NEW_C_K_SCH_H
