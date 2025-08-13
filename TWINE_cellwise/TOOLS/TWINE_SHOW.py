import numpy as np
import config.config as config
from TOOLS.Visual import show_L_equ_TWINE
from RES_CONS import *
file_pth=config.file_path
round_num=config.round_num
res=[ [34, 49, 64, 84, 85, 102, 103, 106, 108, 115, 121, 127, 186, 195, 204], [18, 22, 32, 33, 35, 53, 76, 92, 94, 95, 107, 111, 160, 170, 191, 199], [4, 6, 14, 19, 23, 26, 27, 36, 41, 55, 72, 93, 157, 164, 171]]
RESD7=[[4, 6, 14, 19, 23, 26, 27, 36, 41, 55, 72, 93, 125, 132, 139]]
def show_cons_set(gmat,lst):
    mat=gmat[lst,:]
    show_L_equ_TWINE(mat)
if __name__=="__main__":
    gmat=np.load(file_pth+"GLOBAL_MAT.npy")
    print(np.shape(gmat))
    print("round_num: ",round_num)
    cnt=0
    for i in RES_DC15_SOL:
        lst=[] 
               
        for r in i:
            if(r>64*round_num):
                pass
            else:
                lst.append(r)
        print("the "+str(cnt)+" equation set is:")
        show_cons_set(gmat,lst)
        cnt=cnt+1
