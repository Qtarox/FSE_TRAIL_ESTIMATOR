//
// Created by 25369 on 2024/12/22.
//

#ifndef NEW_C_TW_RNF_H
#define NEW_C_TW_RNF_H
#include <stdint.h>
#include <cinttypes>
#include <math.h>
#include "stdio.h"
#include "iostream"
void show_4x4mat(const uint8_t *t);
void CellXOR(const uint8_t *t1, uint8_t *t2,int len);
void DIFFXOR( uint8_t *t1,const uint8_t *df,int len);
void AddKey(uint8_t *t1,const uint8_t* k);
void PermuCell(uint8_t* t1);
void LR_Add(uint8_t* t1);
void SubCell(uint8_t* t1);
void CellXOR2(const uint8_t *t1,const uint8_t *t2,uint8_t* res);
void LB_F(uint8_t *pt, const uint8_t *key,uint8_t* cpth);
#endif //NEW_C_TW_RNF_H
