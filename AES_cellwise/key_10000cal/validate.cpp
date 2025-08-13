//
// Created by 25369 on 2025/5/18.
//
#include "validate.h"

bool validate(int key[][256]){
    for(int i=0;i<16;i++) {
        if(get_len(key[i])==0) return false;
    }
    return true;
}