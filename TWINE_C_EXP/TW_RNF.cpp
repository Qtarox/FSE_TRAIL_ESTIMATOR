//
// Created by 25369 on 2024/12/22.
//
#include "TW_RNF.h"
#include "TW_CNST.h"
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
        t1[2*i]^=k[i];
    }
}
void SubCell(uint8_t* t1)
{
    for (int i=0;i<8;i++)
    {
        t1[2*i]=Sbox[t1[2*i]];
    }
}
void PermuCell(uint8_t* t1)
{
    uint8_t t2[16];
    for(int i=0;i<16;i++)
    {
        t2[Pt[i]]=t1[i];
    }
    for(int i=0;i<16;i++)
    {
        t1[i]=t2[i];
    }
}
void LR_Add(uint8_t* t1, const uint8_t* tr)
{
    uint8_t tmp[16];
    for(int i=0;i<8;i++)
    {
        tmp[2*i+1]=t1[2*i]^t1[2*i+1];
        tmp[2*i]=tr[i];
    }
    for(int i=0;i<16;i++)
    {
        t1[i]=tmp[i];
    }
}

void DIFFXOR( uint8_t *t1,const uint8_t *df,int len)
{
    for (int i=0;i<len;i++)
    {
        t1[2*i]^=df[i];
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
    uint8_t tr[8];// used to save pt[2*i]
    for(int i=0;i<8;i++)
    {
        tr[i]=pt[2*i];
    }
//    std::cout<<"before add key\n";
//    show_4x4mat(pt);
    AddKey(pt,key);

//    std::cout<<"after add key\n";
//    show_4x4mat(pt);
    for(int i=0;i<8;i++)
    {
        cpth[i]=pt[2*i];//cpth[0-7] stores the input before Sbox
    }
    SubCell(pt);
//    std::cout<<"after Sbox\n";
//    show_4x4mat(pt);
    for(int i=0;i<8;i++)
    {
        cpth[8+i]=pt[2*i];//cpth[8-15] stores the output after Sbox
    }
    LR_Add(pt,tr);
//    std::cout<<"after LR XOR\n";
//    show_4x4mat(pt);
    PermuCell(pt);
//    std::cout<<"after permute\n";
//    show_4x4mat(pt);


}