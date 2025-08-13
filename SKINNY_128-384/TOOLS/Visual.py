import config.config as config
import numpy as np
round_num=config.round_num
from TOOLS.BASIC_OP import is_active

def show_L_equ_SKINNY(lmat):
    for i in range(np.shape(lmat)[0]):
        if((lmat[i].sum())==2):# is nonlinear
            l_tmp=""
            for j in range(32*(round_num+1)):
                rn=j//32
                ind=j%32
                if(lmat[i][j]==1 and is_active(j)):
                    if(ind<16):
                        l_tmp=l_tmp+" + S([x^"+str(int(rn))+"_"+str(ind)+"])"
                    else:
                        l_tmp=l_tmp+" + [y^"+str(int(rn))+"_"+str((ind-16))+ "]"
                elif(lmat[i][j]==1):
                    if(ind<16):
                        l_tmp=l_tmp+" + S(x^"+str(int(rn))+"_"+str(ind)+")"
                    else:
                        l_tmp=l_tmp+" + y^"+str(int(rn))+"_"+str((ind-16))+""
            l_tmp=l_tmp+'= 0 '
            print(l_tmp[2:])
        else:
            l_tmp=""
            for j in range(32*(round_num+1)):
                rn=j//32
                ind=j%32
                if(lmat[i][j]==1 and is_active(j)):
                    if(ind<16):
                        l_tmp=l_tmp+" + [x^"+str(int(rn))+"_"+str(ind)+"]"
                    else:
                        l_tmp=l_tmp+" + [y^"+str(int(rn))+"_"+str((ind-16))+ "]"
                elif(lmat[i][j]==1):
                    if(ind<16):
                        l_tmp=l_tmp+" + x^"+str(int(rn))+"_"+str(ind)+""
                    else:
                        l_tmp=l_tmp+" + y^"+str(int(rn))+"_"+str((ind-16))+""
            for k in range(16*(round_num+1)):
                if(lmat[i][k+round_num*32+32]==1):
                    # print(k+round_num*128)
                    l_tmp=l_tmp+' + k1_'+str(k%16)+" +  k2_"+str(k%16)+"_"+str((k//16)//2)+" +  k3_"+str(k%16)+"_"+str((k//16)//2)
            l_tmp=l_tmp+'= 0 '
            print(l_tmp[2:])

    
def show_cons_set(gmat,list_i):
    for row_ind in list_i:
        tmp=gmat[row_ind]
        tmp=np.reshape(tmp,(1,-1))
        show_L_equ_SKINNY(tmp)