//
// Created by 25369 on 2024/12/22.
//
#include "K_SCH.h"
#include "LB_CNST.h"
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
void key_shift(uint8_t* key)
{
    uint8_t k[80];
    for(int i=0;i<8;i++)
    {
        k[i]=key[72+i];
    }
    for(int i=8;i<80;i++)
    {
        k[i]=key[i-8];
    }
    for(int i=0;i<80;i++)
    {
        key[i]=k[i];
    }
}

//void SubKey(uint8_t* key)
//{
//    int k9=key[79]*8+key[78]*4+key[77]*2+key[76];
//    int k8=key[75]*8+key[74]*4+key[73]*2+key[72];
//    k9=Sbox[9][k9];
//    k8=Sbox[8][k8];
//    for(int i=0;i<4;i++)
//    {
//        key[76+i]=(k9>>i)&1;
//        key[72+i]=(k8>>i)&1;
//    }
//}

//void ADDrd(uint8_t* key,int i)
//{
//    for(int j=46;j<51;j++)
//    {
//        key[j]=(i>>(j-46))&1;
//    }
//}

void get_key(const uint8_t* key, uint8_t* round_key,int rn)
{
    for(int i=0;i<8;i++)
    {
        round_key[i]=key[i+rn*8];
    }
}
void key_sch(uint8_t* key,int i)
{
    key_shift(key);

}

