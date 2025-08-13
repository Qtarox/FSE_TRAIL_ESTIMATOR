import numpy as np
from GAUSS.GAUSS_COLLECTOR import row_mul
from GEN_L.GF28 import *
from TOOLS.Visual import show_L_equ_AES
from TOOLS.BASIC_OP import *
import config.config as config
file_pth=config.file_path
round_num=config.round_num
x_dic=load_dic(config.file_path+"act_x.json")
y_dic=load_dic(config.file_path+"act_y.json")
def lst_mul(lst,num):
    res=[]
    for i in lst:
        res.append(gf_mul(i,num))
    return res
    

def gf_add(gmat,equ,coef):
    l=len(equ)
    tmp_mat=gmat[equ,:].copy()
    # print(np.shape(tmp_mat))
    for i in range(l):
        row_mul(tmp_mat,i,coef[i])
    res=np.zeros((1,np.shape(tmp_mat)[1]),dtype=int)
    for i in range(l):
        res[0]^=tmp_mat[i]
    show_L_equ_AES(res)
    #calculate the exact value for kay variables
    RES=[0]
    for j in range(np.shape(res)[1]//48*32):
        if(res[0][j]>=1):
            #check the j's corresponding element
            r=j//32
            ind=j%32
            lst=[]
            if(ind<16):# x
                lst=x_dic['x_'+str(r)+'_'+str(ind)]
            else:
                lst=y_dic['y_'+str(r)+'_'+str(ind-16)]
            r_l=lst_mul(lst,res[0][j])
            # print(r_l)
            RES=list_xor(RES,r_l)
    print(RES)
            



cons_lst=[[17, 21, 25, 29], [16, 20, 24, 28], [0, 4, 8, 12], [19, 23, 27, 31], [18, 22, 26, 30]]
cons_coe=[[194, 19, 141, 246], [173, 246, 109, 118], [23, 47, 246, 145], [204, 136, 145, 118], [214, 77, 118, 141]]
CONS3=[cons_lst,cons_coe]
cons_lst1=[[0, 4, 8, 12]]
cons_coe1=[[23, 47, 246, 145]]
CONS2=[cons_lst1,cons_coe1]
DC3=[[[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[72,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]],
[[144 ,  0,   0,   0,  72,   0,   0,   0,  72,   0,   0,   0, 216,   0,   0,   0],[121 ,  0,   0,   0,   4,   0,   0,   0, 228,   0,   0,   0, 129,   0,   0,   0]],
[[242 ,129, 228,  12, 121, 129,  55,   8, 121, 152, 211,   4, 139,  25, 228,   4],[215 ,247,  65, 132,   5, 118,   4,  88,   7, 146, 146, 146, 229, 217,  44,  86]]]
def print_DCX(DC):
    for i in range(len(DC)):
        for lst in range(len(DC[i])):
            for j in DC[i][lst]:
                if(j<16):
                    print(("0"+str(hex(j))[2:]).upper(),end="")
                else:
                    print((str(hex(j))[2:]).upper(),end="")
            print()

if __name__=="__main__":
    gmat=np.load(file_pth+"GLOBAL_MAT.npy")
    CONS=CONS2
    cons_lst=CONS[0]
    cons_coe=CONS[1]
    for i in range(len(cons_lst)):
        print("Results for ",i," th constraint: ")
        gf_add(gmat,cons_lst[i],cons_coe[i])
    print_DCX(DC3)
    # print(len({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255}))