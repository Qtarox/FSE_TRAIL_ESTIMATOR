//
// Created by 25369 on 2025/5/17.
//
#include <stdint.h>
#include <stdio.h>
//#include "GF28.h"
#include "random"
#define Nb 4       // Number of columns (32-bit words) comprising the state
#define Nk 4       // Number of 32-bit words in the key (AES-128)
#define Nr 1      // Number of rounds (AES-128)
uint8_t gf_mul(uint8_t a1,uint8_t b1) {
    int a=a1,b=b1;
    uint8_t result = 0;
    while(b){
        if (b & 1)  {result ^= a;}
        a <<= 1;
        if (a & 0x100) a ^= 0x11b;
        b >>= 1;}
    return (result & 0xFF);
}
uint8_t s_box[256] = {
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};

uint8_t rcon[10] = { 0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36 };

// RotWord: rotate 4-byte word left
void RotWord(uint8_t* word) {
    uint8_t temp = word[0];
    word[0] = word[1];
    word[1] = word[2];
    word[2] = word[3];
    word[3] = temp;
}

// SubWord: apply S-box to each byte
void SubWord(uint8_t* word) {
    for (int i = 0; i < 4; i++)
        word[i] = s_box[word[i]];
}

// Key Expansion: from 16-byte key to 176-byte expanded key
void KeyExpansion(const uint8_t* key, uint8_t* expandedKeys) {
    int i;
    for (i = 0; i < 16; i++) {
        expandedKeys[i] = key[i];
    }

    int bytesGenerated = 16;
    int rconIteration = 0;
    uint8_t temp[4];

    while (bytesGenerated < 32) {
        for (i = 0; i < 4; i++)
            temp[i] = expandedKeys[bytesGenerated - 12 + i];

        if (bytesGenerated % 16 == 0) {
            RotWord(temp);
            SubWord(temp);
            temp[0] ^= rcon[rconIteration++];
        }

        for (i = 0; i < 4; i++) {
            expandedKeys[bytesGenerated] = expandedKeys[bytesGenerated - 16] ^ temp[i];
            bytesGenerated++;
        }
    }
}

// Print round keys
void PrintRoundKeys(uint8_t* roundKeys) {
    for (int i = 0; i <= Nr; i++) {
        printf("Round %2d: ", i);
        for (int j = 0; j < 16; j++) {
            printf("%02x ", roundKeys[i * 16 + j]);
        }
        printf("\n");
    }
}
void gen_rndkey(uint8_t* masterkey){
    static std::random_device rd2; // 获取随机设备种子
    static std::mt19937 eng2(rd2()); // 创建随机数生成器
    std::uniform_int_distribution<> distr2(0, 255);
    for(int i=0;i<16;i++)
    {
        masterkey[i]=distr2(eng2);
    }

}
const uint8_t cons0[16]= {160, 98, 68, 134, 232, 42, 12, 206, 208, 18, 52, 246, 152, 90, 124, 190};
//95 [y^0_0] + 23 [x^1_0] + 47 [x^1_4] + 246 [x^1_8] + 145 [x^1_12] +23 k_0_0 +47 k_0_4 +246 k_0_8 +145 k_0_12= 0

//170 [y^1_12] + 194 [x^2_1] + 19 [x^2_5] + 141 [x^2_9] + 246 [x^2_13] +194 k_1_1 +19 k_1_5 +141 k_1_9 +246 k_1_13= 0
const uint8_t cons1[16]={248, 26, 68, 228, 166, 6, 168, 8, 74, 234, 180, 20, 86, 246, 88, 186};

//64 [y^1_0] + 173 [x^2_0] + 246 [x^2_4] + 109 [x^2_8] + 118 [x^2_12] +173 k_1_0 +246 k_1_4 +109 k_1_8 +118 k_1_12= 0
const uint8_t cons2[16]={64, 227, 68, 231, 41, 138, 45, 142, 80, 243, 84, 247, 57, 154, 61, 158};

//163 [y^1_4] + 204 [x^2_3] + 136 [x^2_7] + 145 [x^2_11] + 118 [x^2_15] +204 k_1_3 +136 k_1_7 +145 k_1_11 +118 k_1_15= 0
const uint8_t cons3[16]={160, 99, 68, 135, 104, 171, 140, 79, 17, 210, 245, 54, 217, 26, 61, 254};

//96 [y^1_8] + 214 [x^2_2] + 77 [x^2_6] + 118 [x^2_10] + 141 [x^2_14] +214 k_1_2 +77 k_1_6 +118 k_1_10 +141 k_1_14= 0
const uint8_t cons4[16]={129, 66, 101, 166, 73, 138, 173, 110, 48, 243, 212, 23, 248,59,28,223};
bool is_in(const uint8_t* cons, int size,uint8_t num){
    for(int i=0;i<size;i++)
    {
        if(num==cons[i]) return true;
    }
    return false;
}
bool check(uint8_t* rk0,uint8_t* rk1){
    int res0=0,res1=0,res2=0,res3=0,res4=0;
    res0= gf_mul(23,rk0[0])^gf_mul(47,rk0[4])^gf_mul(246,rk0[8])^gf_mul(145,rk0[12]);
    res1=gf_mul(194,rk1[1])^gf_mul(19,rk1[5])^gf_mul(141,rk1[9])^gf_mul(246,rk1[13]);
    res2=gf_mul(173,rk1[0])^gf_mul(246,rk1[4])^gf_mul(109,rk1[8])^gf_mul(118,rk1[12]);
    res3=gf_mul(204,rk1[3])^gf_mul(136,rk1[7])^gf_mul(145,rk1[11])^gf_mul(118,rk1[15]);
    res4=gf_mul(214,rk1[2])^gf_mul(77,rk1[6])^gf_mul(118,rk1[10])^gf_mul(141,rk1[14]);
    if(is_in(cons0,16,res0) and is_in(cons1,16,res1)and is_in(cons2,16,res2)and is_in(cons3,16,res3)and is_in(cons4,16,res4))   return true;
    return false;
}
int main() {
    // Example master key (16 bytes)
//    uint8_t a=204,b=2;
//    printf("res: %d", gf_mul(a,b));
    uint8_t key[16] = {
            0x2b, 0x7e, 0x15, 0x16,
            0x28, 0xae, 0xd2, 0xa6,
            0xab, 0xf7, 0x15, 0x88,
            0x09, 0xcf, 0x4f, 0x3c
    };
    int exp_num=1<<30;

    uint8_t expandedKeys[32]; // 2 round keys × 16 bytes
    uint8_t rk0[16];
    uint8_t rk1[16];
    int cnt=0;
    for(int t=0;t<exp_num;t++)
    {
        gen_rndkey(key);
        KeyExpansion(key, expandedKeys);
        for(int i=0;i<16;i++)
        {
            int row=i/4,col=i%4;
            rk0[col*4+row]=expandedKeys[i];
            rk1[col*4+row]=expandedKeys[i+16];
        }
        if(check(rk0,rk1)) cnt++;
        if(t%(exp_num/100)==0)      printf("Process: %d %\n",t/(exp_num/100));
    }
    printf("Valid keys number: %d",cnt);

//    PrintRoundKeys(expandedKeys);

    return 0;
}
