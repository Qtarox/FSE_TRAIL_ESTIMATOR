//
// Created by 25369 on 2025/5/19.
//
#include "key_sch.h"
void LstEqu(const int *w1,int *w2)
{
    for(int i=0;i<256;i++){
        w2[i]=w1[i];
    }
}
void RotWordLst(int word[][256]) {
    int temp[256];
    LstEqu(word[0],temp);
    LstEqu(word[1],word[0]);
    LstEqu(word[2],word[1]);
    LstEqu(word[3],word[2]);
    LstEqu(temp,word[3]);
}

// SubWord: apply S-box to each byte
void SubWordLst(int word[][256]) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 256; j++) {
            if(word[i][j]==-1) break;
            word[i][j] = s_box[word[i][j]]; }
    }
}
void WordXOR(int *word,int a)
{
    for(int i=0;i<256;i++)
    {
        if(word[i]==-1) break;
        word[i]=word[i]^a;
    }
}
void LstXor(const int *a,const int *b,int *c){
    int res[256]={0};
    int tmp;
    int cnt=0;
    for(int i=0;i<256;i++)
    {
        c[i]=-1;
    }
    for(int i=0;i<256;i++)
    {
        if(a[i]==-1) break;
        for(int j=0;j<256;j++)
        {
            if(b[j]==-1) break;
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
void LstIntersec(const int *l1,const int *l2 ,int *l3)
{
    for(int i=0;i<256;i++)
    {
        l3[i]=-1;
    }
    int res[256]={0};
    for(int i=0;i<256;i++){
        if(l2[i]==-1) break;
        res[l2[i]]=1;
    }
    int cnt=0;
    for(int i=0;i<256;i++)
    {
        if(l1[i]==-1) break;
        if(res[l1[i]]==1) {
            l3[cnt]=l1[i];
            cnt++;
        }

    }
}
int get_len(const int *lst){
    int cnt=0;
    for(int i=0;i<256;i++)
    {
        if(lst[i]==-1) break;
        cnt++;
    }
    return  cnt;

}
void KeyNext(int key[][256], int expandedKeys[][256]) {
    int i;
    for (i = 0; i < 16; i++) {
        LstEqu(key[i],expandedKeys[i]);
    }
    int rconIteration = 0;
    int temp[4][256];
    int t_arr[256];

    for(int c=0;c<4;c++){
        if(c==0){
            for (i = 0; i < 4; i++) {
                LstEqu(key[3 + 4 * i], temp[i]);
            }
        }
        else {
            for (i = 0; i < 4; i++) {
                LstEqu(expandedKeys[c - 1 + 4 * i], temp[i]);
            }
        }
        if (c == 0) {
            RotWordLst(temp);
            SubWordLst(temp);
            WordXOR(temp[0], rcon[rconIteration++]);
        }

        for (i = 0; i < 4; i++) {
            LstXor(expandedKeys[c+4*i] , temp[i],t_arr);
            LstEqu(t_arr,expandedKeys[c+4*i]);
        }
    }
}

void gen_interkey(const int key1[][256], int key2[][256]){
    int t_arr[256];
    for(int i=0;i<16;i++)
    {
        LstIntersec(key1[i],key2[i],t_arr);
        LstEqu(t_arr,key2[i]);
    }
}