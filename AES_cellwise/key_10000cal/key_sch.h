//
// Created by 25369 on 2025/5/19.
//
#include <stdint.h>
#include <stdio.h>
#include "GF28.h"
#include "CONST.h"
#ifndef KEY_10000CAL_KEY_SCH_H
#define KEY_10000CAL_KEY_SCH_H
void KeyNext(int key[][256], int expandedKeys[][256]);
void LstIntersec(int *l1,int *l2 ,int *l3);
int get_len(const int *lst);
void gen_interkey(const int key1[][256], int key2[][256]);
#endif //KEY_10000CAL_KEY_SCH_H
