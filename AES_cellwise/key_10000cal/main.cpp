//
// Created by 25369 on 2025/5/18.
//
#include "GF28.h"
#include "random"
#include "BASIC_OP.h"
#include "gen_dc.h"
#include "key_sch.h"
//#include "CONST.h"
#include "validate.h"
const uint8_t MC[4][4]={{2,3,1,1},
                        {1,2,3,1},
                        {1,1,2,3},
                        {3,1,1,2}};
const uint8_t X_IND[4][4]={{0,5,10,15},
                           {1,6,11,12},
                           {2,7,8,13},
                           {3,4,9,14}};
void gen_rndkey(uint8_t* masterkey){
    static std::random_device rd2; // 获取随机设备种子
    static std::mt19937 eng2(rd2()); // 创建随机数生成器
    std::uniform_int_distribution<> distr2(0, 255);
    for(int i=0;i<16;i++)
    {
        masterkey[i]=distr2(eng2);
    }

}

void gen_key(int (*ycell)[16],int *xcell,int *kcell ,int cell)
{
    int row=cell/4,col=cell%4;
    int lst0[16],lst1[16],lst2[16],lst3[16],lst4[256],lst5[256],lst6[256];
    lst_mul(MC[row][0],ycell[X_IND[col][0]],lst0);
    lst_mul(MC[row][1],ycell[X_IND[col][1]],lst1);
    lst_mul(MC[row][2],ycell[X_IND[col][2]],lst2);
    lst_mul(MC[row][3],ycell[X_IND[col][3]],lst3);

    lst_xor(lst0,lst1,lst4,16,16);
    lst_xor(lst2,lst3,lst5,16,16);
    lst_xor(lst4,lst5,lst6,256,256);
    lst_xor(lst6,xcell,kcell,256,16);

}
void show_skey(int key[][256])
{

        printf("next key :\n");
        for(int c=0;c<16;c++)
        {
            printf("cell %d is: [",c);
            for(int i=0;i<256;i++)
            {
                if(key[c][i]==-1) break;
                printf("%d, ",key[c][i]);
            }
            printf("]\n");
        }

}
void show_keycells( int N,int kcell[][16][256])
{
    for(int r=0;r<N;r++)
    {
        printf("round %d:\n",r);
        for(int c=0;c<16;c++)
        {
            printf("cell %d is: [",c);
            for(int i=0;i<256;i++)
            {
                if(kcell[r][c][i]==-1) break;
                printf("%d, ",kcell[r][c][i]);
            }
            printf("]\n");
        }
    }
}
const int N=7;
uint8_t out[N][16];
uint8_t in[N][16];
int xcell[N][16][16];
int ycell[N][16][16];
int kcell[N-1][16][256];

int main(){
//    int a= gf_mul(204,2);
//    printf("%d",a);
    uint8_t DC0[16];
    int cnt=0;
    int exp_num=10000;
    int next_key[16][256];
    for(int t=0;t< exp_num;t++)
    {
    gen_rndkey(DC0);
    gen_AES_dc(DC0,N,in ,out);
//    for(int i=0;i<N;i++)
//    {
//        show_array(in[i]);
//        printf("\n");
//        show_array(out[i]);
//        printf("\n");
//    }
//gen xy cells
    for(int i=0;i<N;i++) {
        for (int c = 0; c < 16; c++) {
            get_xddt(in[i][c], out[i][c], xcell[i][c]);
            get_yddt(in[i][c], out[i][c], (ycell[i][c]));
        }
    }
    //gen key value
    for(int r=0;r<N-1;r++)
    {
        for(int c=0;c<16;c++)
        {
            gen_key(ycell[r], (xcell[r + 1][c]), kcell[r][c], c);
        }
    }
//    show_keycells(N-1,(kcell));
    for(int r=0;r<N-2;r++)
    {
        KeyNext(kcell[r],next_key);
        gen_interkey(next_key,kcell[r+1]);
    }
    if(!validate(kcell[N-2])) cnt++;}
    printf("invalid keys: %d",cnt);




}