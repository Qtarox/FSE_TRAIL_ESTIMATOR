import numpy as np
import config.config as config
from TOOLS.Visual import show_L_equ_TWINE
round_num=config.round_num
file_path=config.file_path
Pt=[5, 0, 1, 4, 7, 12, 3, 8, 13, 6, 9, 2, 15, 10, 11, 14]
def gen_lmat():
# for each round we have 16 x variables, 16 y variables(only 8 used) and 8round key k^r_i    
    L_MAT=np.zeros((16*round_num,40*(round_num+1)))
    for r in range(round_num):
        for i in range(8):
            g_equ_ind1=r*16+i*2
            g_equ_ind2=r*16+i*2+1
            #first write 2i equ_ind1
            k_r_i=32*(round_num+1)+8*r+i
            x_r_2i=32*r+2*i
            x_r1=32*(r+1)+Pt[2*i]
            L_MAT[g_equ_ind1][k_r_i]=1
            L_MAT[g_equ_ind1][x_r_2i]=1
            L_MAT[g_equ_ind1][x_r1]=1

            x_r_2i1=32*r+2*i+1
            y_r_2i=32*r+16+2*i
            x_r1_2i=32*(r+1)+Pt[2*i+1]
            k_r_i1=32*(round_num+1)+8*(r+1)+Pt[2*i+1]//2
            L_MAT[g_equ_ind2][x_r_2i1]=1
            L_MAT[g_equ_ind2][y_r_2i]=1
            L_MAT[g_equ_ind2][x_r1_2i]=1

            L_MAT[g_equ_ind2][k_r_i1]=1
    
    return L_MAT

def gen_nlmat():
    NL_MAT=np.zeros((8*round_num,40*(round_num+1)))
    for i in range(np.shape(NL_MAT)[0]):
        rn=i//8
        ind=i%8
        y_r_2i=32*rn+16+2*ind
        x_r_2i=32*rn+2*ind
        NL_MAT[i][x_r_2i]=1
        NL_MAT[i][y_r_2i]=1
    return NL_MAT

def assemble_2blk(blk1,blk2):
    len1=np.shape(blk1)[0]
    len2=np.shape(blk2)[0]
    res=np.zeros((len1+len2,np.shape(blk1)[1]),dtype=int)
    for i in range(np.shape(res)[0]):
        if(i<len1):
            res[i]=blk1[i]
        elif(i<len2+len1):
            res[i]=blk2[i-len1]
    return res
def create_GMat(file_path):

    blk1=gen_lmat()
    blk2=gen_nlmat()
    gmat=assemble_2blk(blk1,blk2)  
    np.save(file_path+"GLOBAL_MAT.npy",gmat)
    return gmat

if __name__=="__main__":
    gmat=create_GMat(file_path)
