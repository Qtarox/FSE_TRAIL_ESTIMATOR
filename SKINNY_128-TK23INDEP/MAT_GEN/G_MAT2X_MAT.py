import numpy as np
import config.config as config
round_num=config.round_num
from TOOLS.BASIC_OP import is_active
def GMat2Xmat(gmat,x_dic,y_dic,twk_n=1):
    # reform the gmat to x_only matrix
    # 1. delete all key variables
    # 2. nullify active position
    # 3. change y_r_i into x_r_i
    print("gmat shape: ",np.shape(gmat))
    res=np.zeros((np.shape(gmat)[0],(round_num+1)*32),dtype=int)
    for i in range(np.shape(res)[0]):
        for j in range(np.shape(res)[1]):
            if(gmat[i][j]==1 and (not is_active(j,x_dic,y_dic))):
                res[i][j]=1
    x_mat=np.zeros((np.shape(res)[0],16*(round_num+1)),dtype=int)
    for i in range(np.shape(res)[0]):
        for j in range(np.shape(res)[1]):
            if(res[i][j]==1):
                tmp_rn=j//32
                tmp_ind=j%32
                if(tmp_ind<16):
                    x_rn=tmp_rn
                    x_ind=tmp_ind
                    x_mat[i][x_rn*16+x_ind]=1
                else:
                    y_rn=tmp_rn
                    y_ind=tmp_ind-16
                    x_mat[i][y_rn*16+y_ind]=1
    #check linear constraints:
    linear_list=[]
    for i in range(np.shape(res)[0]):
        if(np.all(x_mat[i] == 0)):
            linear_list.append(i)
    linear_num=len(linear_list)
    non_linear_mat=np.zeros((np.shape(x_mat)[0]-linear_num,16*(round_num+1)),dtype=int)
    row_cnt=0
    nl_mat_row_ind=[]
    for i in range(np.shape(x_mat)[0]):
        if(i in linear_list):
            pass
        else:
            non_linear_mat[row_cnt]=x_mat[i]
            row_cnt=row_cnt+1
            nl_mat_row_ind.append(i)


    return non_linear_mat,linear_list,nl_mat_row_ind

def Prune_gmat(gmat,x_dic,y_dic,twk_n=1):
    # reform the gmat to x_only matrix
    # 1. delete all key variables
    # 2. nullify active position
    # 3. change y_r_i into x_r_i
    print("gmat shape: ",np.shape(gmat))
    res=np.zeros(np.shape(gmat),dtype=int)
    for i in range(np.shape(res)[0]):
        for j in range(np.shape(res)[1]):
            if(gmat[i][j]==1 and (not is_active(j,x_dic,y_dic))):
                res[i][j]=1

    return res