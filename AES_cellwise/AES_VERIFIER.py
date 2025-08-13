import numpy as np
from GAUSS.GAUSS_COLLECTOR import *
from GEN_L.GEN_LMAT import *
from TOOLS.BASIC_OP import *
from TOOLS.Visual import *
import config.config as config
np.set_printoptions(linewidth=400)
np.set_printoptions(threshold=np.inf)
round_num=config.round_num
file_path=config.file_path
DC=config.DC
Sbox=config.Sbox
def Prune_gmat(gmat,x_dic,y_dic):
    # reform the gmat to x_only matrix
    # 1. delete all key variables
    # 2. nullify active position
    # 3. change y_r_i into x_r_i
    print("gmat shape: ",np.shape(gmat))
    res=np.zeros(np.shape(gmat),dtype=int)
    for i in range(np.shape(res)[0]):
        for j in range(np.shape(res)[1]):
            if(gmat[i][j]>=1 and (not is_active(j,x_dic,y_dic)) and j<(round_num+1)*32):
                res[i][j]=gmat[i][j]

    return res

if __name__=="__main__":
    create_folder(file_path)
    creat_dic(file_path,DC)

    x_dic=load_dic(config.file_path+"act_x.json")
    y_dic=load_dic(config.file_path+"act_y.json")
    G_mat=gen_GM()
    # Lmat.astype(int)
    p_mat=Prune_gmat(G_mat,x_dic,y_dic)
    show_L_equ_AES(G_mat)
    
    print(gaussian_elimination_gf28(p_mat))
    