//
// Created by 25369 on 2024/12/22.
//
#include "LB_RNF.h"
#include "LB_CNST.h"
void show_4x4mat(const uint8_t *t)
{
    for(int i=0;i<16;i++)
    {
        if(i%4==0 && i!=0)
        {
            printf("\n");
        }
        printf(" %" PRIu8 "  ", t[i]);
    }
    printf("\n");
}
void AddKey(uint8_t *t1,const uint8_t* k)//text and key shape(16,)
{
    for (int i=0;i<8;i++)
    {
        t1[i]^=k[i];
    }
}
void SubCell(uint8_t* t1)
{
    for (int i=0;i<8;i++)
    {
        t1[i]=Sbox[i][t1[i]];
    }
}
void PermuCell(uint8_t* t1)
{
    uint8_t t2[16];
    t2[0]=t1[1];
    t2[1]=t1[3];
    t2[2]=t1[0];
    t2[3]=t1[2];
    t2[4]=t1[5];
    t2[5]=t1[7];
    t2[6]=t1[4];
    t2[7]=t1[6];
    for(int i=0;i<8;i++)
    {
        t1[i]=t2[i];
    }
}
void LR_Add(uint8_t* t1)
{
    for(int i=0;i<8;i++)
    {
        t1[i]=t1[i+8]^t1[i];
    }
}
void ShiftRow(uint8_t *t1)//text and key shape(16,)
{
    uint8_t t2[16];
    for (int i=10;i<16;i++)
    {
        t2[i]=t1[i-2];
    }
    t2[8]=t1[14];
    t2[9]=t1[15];
    for (int i=8;i<16;i++)
    {
        t1[i]=t2[i];
    }
}
void CellXOR(const uint8_t *t1, uint8_t *t2,int len)
{
    for (int i=0;i<len;i++)
    {
        t2[i]^=t1[i];
    }
}
void CellXOR2(const uint8_t *t1,const uint8_t *t2,uint8_t* res)
{

    for (int i=0;i<16;i++)
    {
        res[i]=t1[i]^t2[i];
    }
}
void LB_F(uint8_t *pt, const uint8_t *key, uint8_t* cpth)//pt is a 16 nibbles array, 0-7 stands for L, 8-15 stands for R
{
    uint8_t t_r[8];
    for(int i=0;i<8;i++)// save  pt[0]-pt[7]
    {
        t_r[i]=pt[i];
    }
    AddKey(pt,key);

//    std::cout<<"after add key\n";
//    show_4x4mat(pt);
    for(int i=0;i<8;i++)
    {
        cpth[i]=pt[i];//cpth[0-7] stores the input before Sbox
    }
    SubCell(pt);
//    std::cout<<"after Sbox\n";
//    show_4x4mat(pt);
    for(int i=0;i<8;i++)
    {
        cpth[8+i]=pt[i];//cpth[8-15] stores the output after Sbox
    }
    PermuCell(pt);
//    std::cout<<"after permute\n";
//    show_4x4mat(pt);
    ShiftRow(pt);
//    std::cout<<"after SR\n";
//    show_4x4mat(pt);
    LR_Add(pt);
//    std::cout<<"after LR_add\n";
//    show_4x4mat(pt);
    for(int i=0;i<8;i++)
    {
        pt[i+8]=t_r[i];
    }
}