//
// Created by 25369 on 2025/5/18.
//
#include "BASIC_OP.h"
#include "CONST.h"
#include "GF28.h"

void get_xddt(int in, int out, int* xddt){
    for(int i=0;i<16;i++)
    {xddt[i]=-1;}
    int x1,x2;
    int cnt=0;
    for(int x=0;x<256;x++)
    {
        x1=x;
        x2=x^in;
        if((s_box[x1]^s_box[x2])==out)
        {
            xddt[cnt]=x;
            cnt++;
        }
    }
}
void get_yddt(int in, int out, int* yddt){
    for(int i=0;i<16;i++)
    {yddt[i]=-1;}
    int x1,x2;
    int cnt=0;
    for(int x=0;x<256;x++)
    {
        x1=x;
        x2=x^in;
        if((s_box[x1]^s_box[x2])==out)
        {
            yddt[cnt]=s_box[x];
            cnt++;
        }
    }
}

void lst_xor(const int *a,const int *b,int *c,int l1,int l2){
    uint8_t res[256]={0};
    uint8_t tmp;
    int cnt=0;
    for(int i=0;i<256;i++)
    {
        c[i]=-1;
    }
    for(int i=0;i<256;i++)
    {
        if(a[i]==-1 or i>=l1) break;
        for(int j=0;j<256;j++)
        {
            if(b[j]==-1 or j>=l2) break;
            tmp=a[i]^b[j];
            if(res[tmp]==0)
            {
                res[tmp]=1;
                c[cnt]=tmp;
                cnt++;
            }
        }
    }
}

void lst_mul(uint8_t x,int *y,int *lst0){
    for(int i=0;i<16;i++)
    {
        lst0[i]=-1;
    }
    for(int i=0;i<16;i++)
    {
        if(y[i]==-1) break;
        lst0[i]= gf_mul(x,y[i]);
    }
}