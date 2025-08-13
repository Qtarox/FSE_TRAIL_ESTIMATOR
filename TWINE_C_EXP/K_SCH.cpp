//
// Created by 25369 on 2024/12/22.
//
#include "K_SCH.h"
#include "TW_CNST.h"
void show_key(uint8_t* key)
{
    for(int i=0;i<80;i++)
    {
        if(i%20==0 && i!=0)
        {
            printf("\n");
        }
        printf(" %" PRIu8 "  ", key[i]);
    }
    printf("\n");
}

void key_rf(uint8_t* key,int i)
{
    int tmp0, tmp1,tmp2,tmp3;


        key[1] = key[1] ^ Sbox[key[0]];
        key[4] = key[4] ^ Sbox[key[16]];
        key[7]^=7&(KEY_CONS[i-1]>>3);
        key[19]^=7&(KEY_CONS[i-1]);
        tmp0=key[0]; tmp1=key[1]; tmp2=key[2]; tmp3=key[3];
        for(int j=0;j<=3;j++)
        {
            key[j*4]=key[j*4+4];
            key[j*4+1]=key[j*4+5];
            key[j*4+2]=key[j*4+6];
            key[j*4+3]=key[j*4+7];
        }
        key[16]=tmp1;
        key[17]=tmp2;
        key[18]=tmp3;
        key[19]=tmp0;

}

void key_rf2(uint8_t* key,int ii)
{
    uint8_t k[20];
    for(int i=0;i<20;i++)
    {
        k[i]=key[(i+8)%20];
    }
    for(int i=0;i<20;i++)
    {
        key[i]=k[i];
    }
}

void get_key(const uint8_t* key, uint8_t* round_key)// key is a 20 element array, rk is a 8 element array
{
    uint8_t key_sind[8]={1,3,4,6,13,14,15,16};
    for(int i=0;i<8;i++)
    {
        round_key[i]=key[key_sind[i]];
    }
}
void key_sch(uint8_t* key,int i)
{
    key_rf2(key,i);
}

