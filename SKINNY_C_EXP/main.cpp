#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include "random"
#include <cinttypes>
const int ROUND_NUM=2;
const uint8_t PLT_CONS[16][16]=
        {{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15,10, 11, 14, 15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}};
const uint8_t PLT_CONS1[16][16]=
        {{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {5, 7, 13, 15,5, 7, 13, 15,5, 7, 13, 15,5, 7, 13, 15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {5, 7, 13, 15,5, 7, 13, 15,5, 7, 13, 15,5, 7, 13, 15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {5, 7, 13, 15,5, 7, 13, 15,5, 7, 13, 15,5, 7, 13, 15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},
         {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}};
const uint8_t CH_MAT[3][2][16] =
        {{{0,0,4,0,4,4,4,4, 4,4,4,0, 4,4,0,0},{0,0,2,0, 2,2,2,2, 2,2,2,0, 2,2,0,0}},
         {{0,0,0,0, 0,0,2,0, 0,2,0,0, 2,0,0,2},{0,0,0,0, 0,0,1,0, 0,1,0,0, 1,0,0,1}},
         {{0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,1},{0,0,8,0, 0,0,0,0, 0,0,0,0, 0,0,0,8}}};
//const uint8_t CH_MAT[2][2][16] =
//        {{{0,0,0,0, 0,0,0,2, 0,0,2,0, 0,2,0,0},{0,0,0,0, 0,0,0,1, 0,0,1,0, 0,1,0,0}},
//         {{1,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0},{11,0,0,0, 8,0,0,0, 0,0,0,0, 0,0,0,0}}};

const uint8_t KEY_DIFF[5][2][16]=
        {{{8,0,0,0,15,0,4,0,0,0,0,0,0,0,0,0},{14,0,0,0,15,0,1,0,0,0,0,0,0,0,0,0}},
         {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 },{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 }},
         {{0,0,8,0,0,4,15,0,0,0,0,0,0,0,0,0},{0,0,12,0,0,2,14,0,0,0,0,0,0,0,0,0}},
         {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 },{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 }},
         {{0,0,0,4,8,14,0,0,0,0,0,0,0,0,0,0},{0,0,0,4,8,12,0,0,0,0,0,0,0,0,0,0}}};

//const uint8_t TST_MAT[5][2][16]=
//        {{{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}},
//         {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}},
//         {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}},
//         {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}},
//         {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}}};
// S-box substitution table
const uint8_t SBOX[16] = {
    0xc , 0x6 , 0x9 , 0x0 ,
    0x1 , 0xa , 0x2 , 0xb ,
    0x3 , 0x8 , 0x5 , 0xd ,
    0x4 , 0xe , 0x7 , 0xf };

// Permutation table
const uint8_t SR[16] = {
    0,  1,  2, 3,
    7,  4,  5, 6,
    10, 11, 8, 9,
    13, 14, 15, 12
};

const uint8_t K_PERM[16] = {
9 , 15 , 8 , 13 ,
10 , 14 , 12 , 11 ,
0 , 1 , 2 , 3 ,
4 , 5 , 6 , 7
};

// Round constant table
// const uint8_t round_constants[16] = {
//     0x00, 0x01, 0x02, 0x04,
//     0x08, 0x10, 0x20, 0x40,
//     0x41, 0x42, 0x44, 0x48,
//     0x50, 0x60, 0x70, 0x00
// };

// Key schedule
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
uint8_t * Create(int len)
{
    auto *res=new uint8_t [len];
    return res;
}
void deleteArray(uint8_t* arr)
{
    delete[] arr;
}

///////////////////////preparation end/////////////////////////////

//================================key operation===================================================
uint8_t LFSR2(uint8_t input)// input is a int value and output another int variable
{
    uint8_t x=input;
    uint8_t res=0;
    uint8_t x3=x/8;
    x=x%8;
    uint8_t x2=x/4;
    x=x%4;
    uint8_t x1=x/2;
    x=x%2;
    uint8_t x0=x;
    res=x2*8+x1*4+x0*2+x3^x2;
    return res;
}
void key_pt(uint8_t *k)
{
    uint8_t tmp[16];
    for (int i=0;i<16;i++)
    {
        tmp[i]=k[K_PERM[i]];//key[i]=key[Pt[i]]
    }
    for (int i=0;i<16;i++)
    {
        k[i]=tmp[i];//key[i]=key[Pt[i]]
    }
}
uint8_t* keyXOR(const uint8_t *t1,const uint8_t *t2)//text and key shape(4,4)
{
    auto*  res= Create(16);
    for (int i=0;i<16;i++)
    {
        if(i<8)
        {
            res[i]=t1[i]^t2[i];
        }
        else
        {
            res[i]=0;
        }
    }
    return res;
}
void  key_sch2(uint8_t* k2)// for tk2
{
    key_pt(k2);
    for (int i=0;i<8;i++) {
        k2[i] = LFSR2(k2[i]);
    }
}
void key_sch1(uint8_t *tk1)
{
    key_pt(tk1);//pass
}
// ======================round func================================//
void SubCell(uint8_t* t1)//input text shape(4*4)
{
    for (int i=0;i<16;i++)
    {
            t1[i]=SBOX[t1[i]];
    }

}

void AddKey(uint8_t *t1,const uint8_t* k)//text and key shape(16,)
{
    for (int i=0;i<8;i++)
    {
            t1[i]=t1[i]^k[i];
    }
}
void ShiftRow(uint8_t *t1)//text and key shape(16,)
{
    uint8_t t2[16];
    for (int i=0;i<16;i++)
    {
        t2[i]=t1[SR[i]];
    }
    for (int i=0;i<16;i++)
    {
        t1[i]=t2[i];
    }
}
uint8_t* CellXOR(const uint8_t *t1,const uint8_t *t2)//text and key shape(16,)
{
    auto*  res= Create(16);
    for (int i=0;i<16;i++)
    {
            res[i]=t1[i]^t2[i];
    }
    return res;
}
void CellXOR2(const uint8_t *t1,const uint8_t *t2,uint8_t* res)//text and key shape(16,)
{

    for (int i=0;i<16;i++)
    {
        res[i]=t1[i]^t2[i];
    }

}
void gen_rnd(uint8_t* txt)
{
    static std::random_device rd; // 获取随机设备种子
    static std::mt19937 eng(rd()); // 创建随机数生成器
    std::uniform_int_distribution<> distr(0, 15); // 创建一个整数分布，范围为1到100
//    auto* rnd_mat= Create(16);
    for(int i=0;i<16;i++)
    {txt[i]=PLT_CONS[i][distr(eng)];}
}
//generate key
const uint8_t  k_13[12]={0,1,2,3,4,5,6,7,8,9,12,13};
const uint8_t k_2[16]={0,2,8,10,0,2,8,10,0,2,8,10,0,2,8,10};
const uint8_t k_i[16]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
void gen_rnd_key(uint8_t* txt)
{
    static std::random_device rd2; // 获取随机设备种子
    static std::mt19937 eng2(rd2()); // 创建随机数生成器
    std::uniform_int_distribution<> distr1(0, 12); // 创建一个整数分布，范围为1到100
    std::uniform_int_distribution<> distr2(0, 15);
//    auto* rnd_mat= Create(16);
    for(int i=0;i<16;i++)
    {if(i==13){
            txt[i]=k_13[distr1(eng2)];
    }
    else if(i==2){
            txt[i]=k_2[distr2(eng2)];
    }
    else
        {
            txt[i]=k_i[distr2(eng2)];}
        }

}

void MixCol(uint8_t* t1)
{
    uint8_t t2[16];
    for (int j=0;j<16;j++)
    {
        if(j<4)
        {
            t2[j]=t1[j]^t1[j+8]^t1[j+12];
        }
        else if(j<8)
        {
            t2[j]=t1[j-4];
        }
        else if(j<12)
        {
            t2[j]=t1[j-4]^t1[j];
        }
        else
        {
            t2[j]=t1[j-12]^t1[j-4];
        }
    }
    for (int j=0;j<16;j++)
    {
        t1[j]=t2[j];
    }
}
//=================================pair func=================================
uint8_t* get_tk(const uint8_t * tk1,const uint8_t* diff,uint8_t* tk2)
{

    for (int i=0;i<16;i++)
    {
        tk2[i]=tk1[i]^diff[i];
    }

}

//============================= Check function==================================
void rn_fn_exp( uint8_t *t0, uint8_t *rn_key,uint8_t* c_PTH)//return a array of shape (32,) where 0-15 is before SB, 16-31 is after SB
{
//    uint8_t *c_PTH=Create(32);
    for(int i=0;i<16;i++)
    {
        c_PTH[i]=t0[i];
    }
    SubCell(t0);//t0,t1 is to be checked
    for(int i=16;i<32;i++)
    {
        c_PTH[i]=t0[i-16];
    }
    AddKey(t0,rn_key);
    ShiftRow(t0);
    MixCol(t0);//t4 is the new round_function
//    return c_PTH;
}
bool mSame(const uint8_t *t1,const uint8_t *t2)
{
//    printf("Calculated one:\n");
//    show_4x4mat(t1);
//    printf("True one:\n");
//    show_4x4mat(t2);

    for (int i = 0; i < 16; ++i) {
            if(t1[i]!=t2[i]) return false;
        }
    return true;
}
bool check_CH( uint8_t *pt_1,uint8_t *pt_2,const uint8_t *tk_1,const uint8_t *tk_2, uint8_t *c_pth1,uint8_t *c_pth2,
              int rn=ROUND_NUM)
{
    uint8_t tk1[16];
    uint8_t tk2[16];

    for(int m=0;m<16;m++)
    {
        tk1[m]=tk_1[m];
        tk2[m]=tk_2[m];
    }


    for (int i=0;i<rn;i++)
    {
        rn_fn_exp(pt_1,tk1,c_pth1);
        uint8_t cp_1_0[16];
        uint8_t cp_1_1[16];
        for(int j=0;j<16;j++)
        {
            cp_1_0[j]=c_pth1[j];
            cp_1_1[j]=c_pth1[j+16];
        }
        key_sch1(tk1);


        rn_fn_exp(pt_2,tk2,c_pth2);
//        std::cout<<"test: "<<i<<std::endl;
        uint8_t cp_2_0[16];
        uint8_t cp_2_1[16];
        for(int j=0;j<16;j++)
        {
            cp_2_0[j]=c_pth2[j];
            cp_2_1[j]=c_pth2[j+16];
        }
        key_sch1(tk2);

//        std::cout<<"pth1_0: \n";
//        show_4x4mat(cp_1_0);
//        std::cout<<"pth1_1: \n";
//        show_4x4mat(cp_1_1);
//        std::cout<<"pth2_0: \n";
//        show_4x4mat(cp_2_0);
//        std::cout<<"pth2_1: \n";
//        show_4x4mat(cp_2_1);
//        std::cout<<"k1: \n";
//        show_4x4mat(key1);
//        std::cout<<"k2: \n";
//        show_4x4mat(key2);
        //chech if satisify the characteristic
        for(int l=0;l<16;l++)
        {
            cp_1_0[l]^=cp_2_0[l];
            cp_1_1[l]^=cp_2_1[l];
        }
//        uint8_t *ch1=CellXOR( cp_1_0,cp_2_0);
//        uint8_t *ch2=CellXOR( cp_1_1,cp_2_1);
//        std::cout<<"round"<<i<<"ch1: \n";
//        show_4x4mat(ch1);
//        std::cout<<"round"<<i<<"ch2: \n";
//        show_4x4mat(ch2);
        uint8_t true_ch1[16];//before S_box
        uint8_t true_ch2[16];// after S_box
        for(int k=0;k<16;k++)
        {
            true_ch1[k]=CH_MAT[i][0][k];
            true_ch2[k]=CH_MAT[i][1][k];
        }
        if(mSame(cp_1_0, true_ch1) && mSame(cp_1_1, true_ch2))
        {
            //pass
        }
        else
        {
            return false;
        }
    }
    return true;
}
const int N_KEY=1000;
//===============================================
int main() {
    uint8_t tk1[16]={0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0 };
    uint8_t tk2[16]={0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0 };
    uint8_t tkdiff[16]={0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0};
//    uint8_t char_diff1[16]={2,0,0,2,0,2,0,0,0,0,0,0,2,2,8,0};
    uint8_t char_diff2[16]={0,0,4,0,4,4,4,4, 4,4,4,0, 4,4,0,0};
    uint8_t c_pth1[32]={0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0,0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0};
    uint8_t c_pth2[32]={0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0,0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0};
    int count=0;
    long int exp_t=1<<14;
    int pro=0;
    //std::default_random_engine e;
    uint8_t pt[16]={0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0 };
    uint8_t pt1[16]={0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0 };
    std::cout<<"running....\n";
    int res[N_KEY];
//    std::srand(static_cast<unsigned int>(std::time(NULL)));
    for(int c=0;c<N_KEY;c++)
    {
        count=0;
        gen_rnd_key(tk1);
        CellXOR2(tk1,tkdiff,tk2);
        if(c%(N_KEY/100)==0){
            std::cout<<"Progress"<<(pro++)<<"%\n";
        }
        for (int i=0;i<exp_t;i++)
        {

            gen_rnd(pt);
            CellXOR2(pt,char_diff2,pt1);
            bool flag=check_CH(pt,pt1,tk1,tk2,c_pth1,c_pth2,3);

            if(flag)
            {
                count=count+1;
//                std::cout<<"got "<<count<<" valid samples\n";
            }
        }
        res[c]=count;
    }
    std::cout<<"results: "<<std::endl;
    for(int i=0;i<N_KEY;i++)
    {
        if(i%20==0) std::cout<<std::endl;
        std::cout<<res[i]<<", ";

    }

    //show_prob(count,exp_t);

//    std::cout<<"possibility: "<<count<<"/"<<exp_t<<";   count : "<<count;
    return 0;
}