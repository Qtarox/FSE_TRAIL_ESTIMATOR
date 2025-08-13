#include "gen_dc.h"
#include "GF28.h"
#include "CONST.h"
const uint8_t SR[16]= {0,1,2,3,5,6,7,4,10,11,8,9,15,12,13,14};
const uint8_t MC[4][4]={{2,3,1,1},
                    {1,2,3,1},
                    {1,1,2,3},
                    {3,1,1,2}};
const uint8_t X_IND[4][4]={{0,5,10,15},
                           {1,6,11,12},
                            {2,7,8,13},
                            {3,4,9,14}};
void propogate(uint8_t * input_array){
    uint8_t res[16];
    for(int i=0;i<16;i++){
        res[i]=input_array[SR[i]];
    }
    int row,col;
    for(int i=0;i<16;i++)
    {
        row=i/4;  col=i%4;
        input_array[i]= gf_mul(MC[row][0],res[col])^gf_mul(MC[row][1],res[4+col])^gf_mul(MC[row][2],res[8+col])^gf_mul(MC[row][3],res[12+col]);
    }
}

void gen_valid_output(uint8_t* dc_in){
    static std::random_device rd1; // 获取随机设备种子
    static std::mt19937 eng1(rd1()); // 创建随机数生成器
    std::uniform_int_distribution<> distr1(0, 255);
    uint8_t rnd_x,dx;
    for(int i=0;i<16;i++)
    {
        rnd_x=distr1(eng1);
        dx=dc_in[i];
        dc_in[i]=s_box[rnd_x]^s_box[rnd_x^dx];
    }


}
void show_array(uint8_t * DC){
    for(int i=0;i<16;i++)
    {
        if(i%4==0) printf("\n");
        printf("%d, ",(int)DC[i]);

    }
}
void gen_AES_dc(uint8_t * DC0_IN,int N,uint8_t (*in)[16],uint8_t (*out)[16])
{
    //INPUT IS A 0 ROUND INPUT OF AES
//    show_array(DC0_IN);
    for(int i=0;i<N;i++){
        for(int j=0;j<16;j++)
        {
            in[i][j]=DC0_IN[j];
        }
        gen_valid_output(DC0_IN);
        for(int j=0;j<16;j++)
        {
            out[i][j]=DC0_IN[j];
        }
//        show_array(DC0_IN);
//        printf("\n");
        propogate(DC0_IN);
//        show_array(DC0_IN);

    }
}

