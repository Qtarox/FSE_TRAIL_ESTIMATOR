import numpy as np
import random
from config.AES_DDT import DDT
import config.config as config
from GEN_L.GF28 import *
from TOOLS.BASIC_OP import *
num = random.randint(0, 255)
DC=config.DC
file_pth=config.file_path
round_num=config.round_num
MC=[[2,3,1,1],
    [1,2,3,1],
    [1,1,2,3],
    [3,1,1,2]]

X_IND=[[0,5,10,15],
       [1,6,11,12],
       [2,7,8,13],
       [3,4,9,14]]
SR=[0,1,2,3,5,6,7,4,10,11,8,9,15,12,13,14]
def propogate(input_array):
    res=input_array.copy()
    for i in range(16):
        res[i]=input_array[SR[i]]
    res2=res.copy()
    for i in range(16):
        row=i//4
        col=i%4
        res2[i]=gf_mul(MC[row][0],res[col])^gf_mul(MC[row][1],res[4+col])^gf_mul(MC[row][2],res[8+col])^gf_mul(MC[row][3],res[12+col])
    return res2.copy()

def gen_rnd(dc_arr):
    res_arr=dc_arr.copy()
    for i in range(16):
        if(dc_arr[i]!=0):
            res_arr[i]=random.randint(0, 255)
    return res_arr.copy()

def gen_valid_output(dc_in):
    dc_out=dc_in.copy()
    for i in range(16):
        if(dc_in[i]!=0):
            dc_out[i]=random.choice(DDT[dc_in[i]])
    return dc_out

def gen_output(dc_in):
    lst_dc=[0, 31, 20, 24, 145, 8, 12, 166, 83, 98, 4, 72, 157, 180, 200, 21, 169, 225, 170, 30, 153, 58, 36, 147, 206, 183, 193, 204, 255, 199, 17, 163, 212, 158, 240, 69, 85, 92, 148, 175, 87, 198, 134, 146, 18, 187, 82, 118, 103, 164, 64, 160, 123, 245, 102, 249, 100, 113, 227, 129, 136, 68, 209, 22, 106, 224, 79, 121, 120, 13, 57, 195, 49, 88, 181, 208, 74, 128, 76, 231, 48, 178, 99, 142, 67, 159, 210, 56, 9, 168, 221, 90, 41, 47, 59, 172, 179, 140, 201, 152, 32, 46, 80, 230, 38, 154, 97, 28, 51, 95, 252, 203, 50, 192, 35, 236, 241, 254, 91, 150, 223, 213, 185, 66, 115, 156, 144, 177, 174, 111, 112, 143, 60, 244, 39, 116, 167, 196, 29, 94, 7, 62, 122, 16, 3, 226, 44, 191, 65, 73, 243, 235, 37, 141, 219, 119, 189, 61, 104, 184, 131, 81, 89, 105, 42, 101, 71, 63, 161, 176, 207, 1, 242, 246, 135, 26, 132, 171, 84, 14, 238, 182, 45, 202, 15, 53, 151, 137, 6, 25, 205, 107, 217, 27, 70, 77, 127, 197, 215, 165, 139, 190, 23, 124, 40, 222, 232, 233, 19, 93, 214, 5, 43, 96, 149, 109, 2, 86, 52, 218, 229, 162, 126, 253, 130, 155, 251, 114, 10, 186, 237, 247, 248, 125, 228, 138, 173, 54, 75, 188, 239, 194, 234, 110, 220, 133, 33, 11, 34, 250, 78, 108, 211, 55, 216, 117]
    dc_out=dc_in.copy()
    for i in range(16):
        if(dc_in[i]!=0):
            dc_out[i]=(lst_dc[dc_in[i]])
    return dc_out
Sbox=config.Sbox
CNT=0
def gen_AESDDT():
    DC=[]

    for i in range(256):
        TMP=[]
        for j in range(256):
            if(len(xddt_list(i,j))>0):
                TMP.append(j)
        DC.append(TMP.copy())  
    return DC
N=3
def gen_AES_dc(DC0_IN):#INPUT IS A 0 ROUND INPUT OF AES
    DC_z=DC0_IN.copy()
    for i in range(N):
        DC_O=gen_valid_output(DC_z)
        print(DC_O)
        DC_z=propogate(DC_O)
        print(DC_z)

def gen_AES_dc2(DC0_IN):#INPUT IS A 0 ROUND INPUT OF AES
    DC_z=DC0_IN.copy()
    for i in range(N):
        DC_O=gen_output(DC_z)
        print(DC_O)
        DC_z=propogate(DC_O)
        print(DC_z)


DC1=[[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]]
if __name__=="__main__":
    dc1=[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    dc1=np.array(dc1)
    # print(propogate(dc1) )
    # dc1=[209 ,  0,   0,   0,   163,   0,   0,   0, 163,   0,   0,   0, 158,   0,   0,   0]
    # print(propogate(dc1))
    # dc2=[2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0]
    # dc2=np.array(dc2)
    # print(gen_valid_output(dc2))
    gen_AES_dc2(dc1)

    