//
// Created by 25369 on 2025/5/18.
//
#include <stdint.h>
#include <stdio.h>
#include "random"
#ifndef KEY_10000CAL_GEN_DC_H
#define KEY_10000CAL_GEN_DC_H
void propogate(uint8_t * input_array);
void gen_AES_dc(uint8_t * DC0_IN,int N,uint8_t (*in)[16],uint8_t (*out)[16]);
void show_array(uint8_t * DC);
void gen_valid_output(uint8_t* dc_in);
#endif //KEY_10000CAL_GEN_DC_H
