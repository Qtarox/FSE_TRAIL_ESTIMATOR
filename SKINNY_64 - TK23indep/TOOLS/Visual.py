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
            for k in range(8*round_num):
                if(lmat[i][k+round_num*32+32]==1):
                    # print(k+round_num*128)
                    l_tmp=l_tmp+' + k^'+str(k//8)+"_"+str(k%8)

            l_tmp=l_tmp+'= 0 '
            print(l_tmp[2:])
def show_L_equ_SKINNY1(lmat):
    for i in range(np.shape(lmat)[0]):
        # print(i)
        l_tmp=""
        flag=False
        for j in range(32*(round_num+1)):
            rn=j//32
            ind=j%32
            if(lmat[i][j]==1 and is_active(j)):
                if(ind<16):
                    l_tmp=l_tmp+" + [ x_"+str(int(rn))+"_"+str(ind)+" ]"
                else:
                    l_tmp=l_tmp+" + [ y_"+str(int(rn))+"_"+str((ind-16))+ " ]"
            elif(lmat[i][j]==1):
                if(ind<16):
                    l_tmp=l_tmp+" + x_"+str(int(rn))+"_"+str(ind)+""
                else:
                    l_tmp=l_tmp+" + y_"+str(int(rn))+"_"+str((ind-16))+""
        for k in range(8*round_num):
            if(lmat[i][k+round_num*32+32]==1):
                # print(k+round_num*128)
                l_tmp=l_tmp+' + k_'+str(k)

        l_tmp=l_tmp+'= 0 '
        print(l_tmp)

    
def show_cons_set(gmat,list_i):
    for row_ind in list_i:
        tmp=gmat[row_ind]
        tmp=np.reshape(tmp,(1,-1))
        show_L_equ_SKINNY(tmp)