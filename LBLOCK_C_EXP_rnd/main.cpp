#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include "random"
#include <cinttypes>
#include "LB_CNST.h"
#include "LB_RNF.h"
#include "K_SCH.h"
const int N_KEY=1000;
const int ROUND_NUM=4;
void show_4x2mat(const uint8_t *t)
{
    for(int i=0;i<8;i++)
    {
        if(i%4==0 && i!=0)
        {
            printf("\n");
        }
        printf(" %" PRIu8 "  ", t[i]);
    }
    printf("\n");
}


///////////////////////preparation end/////////////////////////////


void gen_rnd(uint8_t* txt,const uint8_t *x_4t)
{
    static std::random_device rd; // 获取随机设备种子
    static std::mt19937 eng(rd()); // 创建随机数生成器
    std::uniform_int_distribution<> distr(0, 15); // 创建一个整数分布，范围为1到100
//    auto* rnd_mat= Create(16);
    for(int i=0;i<16;i++)
    {
        if(i==4)
        {
            txt[i]=x_4t[distr(eng)];
        }
        else
        {
            txt[i]=distr(eng);
        }
        }
}
//generate key

void gen_rnd_key(uint8_t* txt)//generate 80 bit key
{
    static std::random_device rd2; // 获取随机设备种子
    static std::mt19937 eng2(rd2()); // 创建随机数生成器
    std::uniform_int_distribution<> distr2(0, 15);
//    auto* rnd_mat= Create(16);
    for(int i=0;i<80;i++)
    {
            txt[i]=distr2(eng2);
    }
}
void gen_rk(uint8_t* rk)
{
    static std::random_device rndk;
    static std::mt19937 eng_k(rndk());
    std::uniform_int_distribution<> distr_k(0,15);
    for(int i=0;i<8;i++)
    {
        rk[i]=distr_k(eng_k);
    }
}

//============================= Check function==================================
bool mSame(const uint8_t *t1,const uint8_t *t2)
{
    for (int i = 0; i < 8; ++i) {
            if(t1[i]!=t2[i]) return false;
        }
    return true;
}

bool check_CH( uint8_t *pt_1,uint8_t *pt_2, uint8_t *key, uint8_t *c_pth1,uint8_t *c_pth2,
              int rn=ROUND_NUM)//c_pth length is 16, record the values of 8 input cells and 8 output cells
{
    uint8_t rk[8];
    for (int i=0;i<rn;i++)
    {
        get_key(key,rk,i);
//        std::cout<<"befor round "<<i<<" pt1: \n";
//        show_4x4mat(pt_1);
//        std::cout<<"before round "<<i<<" pt2: \n";
//        show_4x4mat(pt_2);
        LB_F(pt_1,rk,c_pth1);
        uint8_t cp_1_0[8];
        uint8_t cp_1_1[8];
        for(int j=0;j<8;j++)
        {
            cp_1_0[j]=c_pth1[j];//input of the first pt1
            cp_1_1[j]=c_pth1[j+8];
        }
        LB_F(pt_2,rk,c_pth2);
//        std::cout<<"round "<<i<<" pt1: \n";
//        show_4x2mat(rk);
//        std::cout<<"round "<<i<<" pt2: \n";
//        show_4x4mat(pt_2);
        uint8_t cp_2_0[8];
        uint8_t cp_2_1[8];
        for(int j=0;j<8;j++)
        {
            cp_2_0[j]=c_pth2[j];
            cp_2_1[j]=c_pth2[j+8];
        }
//        key_sch(key,i+1);

        //chech if satisify the characteristic
        for(int l=0;l<8;l++)
        {
            cp_1_0[l]^=cp_2_0[l];
            cp_1_1[l]^=cp_2_1[l];
        }


        uint8_t true_ch1[8];//before S_box
        uint8_t true_ch2[8];// after S_box
        for(int k=0;k<8;k++)
        {
            true_ch1[k]=T[i][0][k];
            true_ch2[k]=T[i][1][k];
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
//===============================================
int main() {
    uint8_t key[80];
    uint8_t exp_key[80];
    uint8_t char_diff2[16]={0,0,0,0,4,0,0,0,0,0,0,4,2,4,0,0};
    uint8_t c_pth1[16]={0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0 };
    uint8_t c_pth2[16]={0 ,0,  0, 0,  0,  0, 0,  0, 0,  0, 0,  0, 0,  0,  0,  0};
    uint8_t rk0[8]={0,0,0,0,0,0,0,0};
    uint8_t x_0_4[16]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    int count;
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
        gen_rnd_key(key);
        if(c%(N_KEY/100)==0){
            std::cout<<"Progress"<<(pro++)<<"%\n";
        }
        get_key(key,rk0,0);
        int k_4=rk0[4];
        for(int ind=0;ind<16;ind++)
        {
            x_0_4[ind]=x_4[ind]^k_4;
        }//generate x_0_4 possible space

        for (int i=0;i<exp_t;i++)
        {
            for(int ind=0;ind<80;ind++)
            {
                exp_key[ind]=key[ind];
            }
            gen_rnd(pt,x_0_4);
            CellXOR2(pt,char_diff2,pt1);
            bool flag=check_CH(pt,pt1,exp_key,c_pth1,c_pth2,4);
            if(flag)
            {
                count++;
            }
        }
        res[c]=count;
    }
    for(int i=0;i<N_KEY;i++)
    {
        if(i%20==0) std::cout<<std::endl;
        std::cout<<res[i]<<", ";

    }

    //show_prob(count,exp_t);

//    std::cout<<"possibility: "<<count<<"/"<<exp_t<<";   count : "<<count;
    return 0;
}