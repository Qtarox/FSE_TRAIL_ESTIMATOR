import numpy as np
from TOOLS.BASIC_OP import *
import config.config as config
from TOOLS.Visual import show_cons_set, show_L_equ_SKINNY
import random
from RES_CONS import *
round_num=config.round_num
Sbox=config.Sbox
x_dic=load_dic(config.file_path+"act_x.json")
y_dic=load_dic(config.file_path+"act_y.json")
def is_useless(len_lin,i,var_lst):
    # print(var_lst)
    for j in (var_lst[i]):
        
        if(is_active(j)):
            continue#useful
        else:
            flg=True
            for ind in range(len_lin,len(var_lst)):
                # print("var:",var_lst[ind])
                if(j in var_lst[ind]):
                    flg=False
                    # print(str(j)+" is in")
                    break
            if(flg==False):
                continue
            else:
                return True
    return False
                    
def useless_lst(len_lin,var_lst):
    # print(var_lst)
    u_lst=[]
    for i in range(len(var_lst)):
        tmp=[]
        for j in (var_lst[i]):
            if(is_active(j)):
                continue#useful
            else:
                flg=True
                for ind in range(len_lin,len(var_lst)):
                    # print("var:",var_lst[ind])
                    if(j in var_lst[ind]):
                        flg=False
                        # print(str(j)+" is in")
                        break
                if(flg==False):
                    continue
                else:
                    tmp.append(j)
        u_lst.append(tmp.copy())
    return u_lst

def Prepross_eq(cmat,len_lin,equ_ind_lst):
    nl_mat=cmat[len_lin:][:]
    # 1. XOR all equation in same linear layer
    # 1.1 classify equations in the same linear layer
    linear_list=list([] for i in range(round_num))
    var_lst=[]
    for i in range(np.shape(cmat)[0]):
        tmp=[]
        for j in range(32*(round_num+1)):
            if(cmat[i][j]==1):
                tmp.append(j)
        var_lst.append(tmp.copy())
    # print(linear_list)
    for i in range(len_lin):
        linear_list[equ_ind_lst[i]//16].append(i)
    tmp_lst=[]
    for i in linear_list:
        if(len(i)>0):
            tmp_lst.append(i.copy())
    linear_list=tmp_lst
    useless=[]
    for i in range(len_lin):
        if(is_useless(len_lin,i,var_lst)):
            useless.append(i)
    u_lst=useless_lst(len_lin,var_lst)
    res=list([] for i in range((len_lin)))
    used=[0 for i in range((len_lin))]
    # print("useless:",u_lst)
    added=[]
    for i in range(len_lin):
        if(used[i]==0):
            res[i].append(i)
        for j in range(i+1,len_lin):
            if(set(u_lst[i])&set(u_lst[j]) and used[j]==0):
                res[i].append(j)
                u_lst[i]=list(set(u_lst[i]+(u_lst[j])))
                used[j]=1
    final_res=[]
    for i in res:
        if(i!=[]):
            final_res.append(i.copy())
    print(final_res)
    
    # 1.2 merge all the useless linear equations 
    new_len=len(final_res)
    new_mat=np.zeros((new_len,np.shape(cmat)[1]),dtype=int)
    for i in range(new_len):
        for j in final_res[i]:
            new_mat[i]^=cmat[j]
    # show_L_equ_SKINNY(new_mat)
    # show_L_equ_SKINNY(nl_mat)
    
    return new_mat ,nl_mat

    
#2^-4n
def show_constraint_set(nmat,equ_dic,nlmat):
    equ_LST=[]#used to save the linear and nonlinear equations
    for i in range(np.shape(nmat)[0]):
        str_tmp=""
        if("z_"+str(i)+"_"+str(99) in equ_dic):
            str_tmp+="z_"+str(i)+"_"+str(99)
        for j in range(32*(round_num+1)):
            if(nmat[i][j]==1):
                if(is_active(j)):
                    pass
                else:
                    rn=j//32
                    ind=j%32
                    if(ind<16):
                        str_tmp=str_tmp+" + x_"+str(int(rn))+"_"+str(ind)+""
                    else:
                        str_tmp=str_tmp+" + y_"+str(int(rn))+"_"+str((ind-16))+""
        for k in range(16*(round_num+1)):
            if(nmat[i][k+round_num*32+32]==1):
                # print(k+round_num*128)
                str_tmp+=' + k1_'+str(k%16)+" +  k2_"+str(k%16)+"_"+str((k//16)//2)
        str_tmp=str_tmp+'= 0 '
        print(str_tmp)
        equ_LST.append(str_tmp)
    for i in range(np.shape(nlmat)[0]):
        str_tmp=""
        # if("x_"+str(i)+"_"+str(99) in equ_dic):
        #     str_tmp+="x_"+str(i)+"_"+str(99)
        for j in range(32*(round_num+1)):
            if(nlmat[i][j]==1):
                if(is_active(j)):
                    pass
                else:
                    rn=j//32
                    ind=j%32
                    if(ind<16):
                        str_tmp=str_tmp+" + x_"+str(int(rn))+"_"+str(ind)+""
                    else:
                        str_tmp=str_tmp+" + y_"+str(int(rn))+"_"+str((ind-16))+""

        str_tmp+='= 0 '
        print(str_tmp)
        equ_LST.append(str_tmp)
    return equ_LST,equ_dic


def check_uniformity(new_mat):
    equ_dic={}
    uni_flg=False
    for i in range(np.shape(new_mat)[0]):
        free_cnt=0
        tmp=[0]
        for j in range(32*(round_num+1)):
            if(new_mat[i][j]==1):
                if(is_active(j)):
                    # print(active_list(j))
                    tmp=list_xor(tmp,active_list(j))
                else:
                    free_cnt+=1
        # print("equ "+str(i)+": ",tmp)
        if(tmp==[0]):
            pass
        else:
            if(len(tmp)==16):
                print("USELESS UNIFORM!")
                uni_flg=True
            equ_dic["z_"+str(i)+"_"+str(99)]=tmp.copy()
    return equ_dic,uni_flg



def get_key_var(equ_var):
    key_var=[]
    for i in equ_var:
        tmp=[]
        for j in i:
            if(j>32*(round_num+1)):
                tmp.append(j)
        key_var.append(tmp.copy())
    return key_var



def CONS_ES(file_path,mat_name,equ_ind_lst):
    #input the equation set 
    # 1. build the 2D array to store the possible values Z={(x0,y0),(x1,y1),(x2,y2)},initialize the data
    # 2. generate 2^20 random set of Z_i
    # 3. Save the count number of each key combination
    chosen_mat=np.load(file_path+mat_name)
    len_lin=0
    
    for i in range(np.shape(chosen_mat)[0]):
        cnt=np.sum(chosen_mat[i])
        if(cnt==2):
            len_lin=i
            break
    equ_var=[]
    new_mat=Prepross_eq(chosen_mat,len_lin,equ_ind_lst)
    for i in range(np.shape(new_mat)[0]):
        tmp=[]
        for j in range(np.shape(new_mat)[1]):
            if(new_mat[i][j]==1):
                tmp.append(j)
        equ_var.append(tmp.copy())
    Z_list,ARR_X=get_Z_set(new_mat)
    key_var=[]
    key_lst=[]
    for i in equ_var:
        tmp=[]
        for k in i:
            if(k>=32*(round_num+1)):
                tmp.append(k)
                if(k not in key_lst):
                    key_lst.append(k)
        key_var.append(tmp.copy())
    show_key(key_var)
                

def get_Z_set(c_mat):
    # 1. extract out the variable list
    Z_list=[]
    for i in range(np.shape(c_mat)[0]):
        for j in range((round_num+1)*32):
            if(c_mat[i][j]==1):
                rn=j//32
                ind=j%32
                if(ind>=16):#is y
                    y_ind=ind-16
                    Z_list.append(y_ind+rn*32)
                else:# is x
                    Z_list.append(ind+rn*32)
    Z_list=list(set(Z_list))    

    # 2. build the 2d array
    ARR_X=[]
    ARR_Y=[]
    name_lst=[]
    for i in Z_list:
        x_str='x_'+str(i//32)+'_'+str(i%32)
        name_lst.append(x_str)
        if(x_str in x_dic):
            ARR_X.append(x_dic[x_str])
        else:
            ARR_X.append(config.full_list.copy())
    for i in ARR_X:
        ARR_Y.append(SBOX_MAP(i))
    # print(name_lst)
    # print(ARR_X)
    # print(ARR_Y)
    return Z_list,ARR_X

def show_key(key_var):
    for i in range(len(key_var)):
        if(len(key_var[i])==0):
            print("no key invovled in equ "+str(i))
        else:
            print("keys in equ ")

def get_random_set(ARR_X):
    random_X=[]
    for i in ARR_X:
        random_X.append(i[random.randint(0,len(i))])
    return random_X

def get_linear_len(tstmat):
    len_cnt=0
    for i in range(np.shape(tstmat)[0]):
        if(np.sum(tstmat[i])==2):
            break
        len_cnt+=1
    return len_cnt


def get_var(c_mat):
    var_lst=[]
    start_ind=24*(round_num+1)
    for i in range(np.shape(c_mat)[0]):
        for j in range(start_ind,32*(round_num+1)):
            if(c_mat[i][j]==1):
                if(j-start_ind not in var_lst):
                    var_lst.append(j-start_ind)
    return var_lst

def lists_intersect(lst1, lst2):
    return bool(set(lst1) & set(lst2))
def Grouping(V):# group constraints
    GROUP_LST=[]
    used_lst=[0 for i in range(len(V))]
    for i in range(len(V)):
        tmp=[]
        if(used_lst[i]==1):
            continue
        else:
            tmp.append(i)
            used_lst[i]=1

        for j in range(i,len(V)):
            if(used_lst[j]==1):
                continue
            if(lists_intersect(V[i],V[j])):
                used_lst[j]=1
                tmp.append(j)
        GROUP_LST.append(tmp.copy())
    return GROUP_LST




def process_cons(RES_C):
    RES=[]
    RES_G=[]
    V=[]
    for ind in range(len(RES_C)):
        tmp=[]
        print()
        print("constraint set "+str(ind)+" under check: ")
        tstm=np.load(config.file_path+'/tst_mat'+str(ind)+'.npy')
        # show_Lblock_equ(tstm)
        len_lin=get_linear_len(tstm)
        print("len:",len_lin)
        nmat,nl_mat=Prepross_eq(tstm,len_lin,RES_C[ind])
        var_lst=get_var(nmat)
        V.append(var_lst)

        #give an pruned equation and a dic list
        equ_dic,uni_flg=check_uniformity(nmat)
        if(uni_flg==True):# if uniform then withdraw it
            continue
        print("=========================================")
        equ_list,equ_dic=show_constraint_set(nmat,equ_dic,nl_mat)   
        tmp.append(equ_list.copy())
        tmp.append(equ_dic.copy())
        print(equ_dic)   
        RES.append(tmp.copy())
    Group_LST=Grouping(V)
    print(RES) 
    return RES,Group_LST# a list for generate cp solver file     
        
if __name__=="__main__":
    RES=[]
    RES_C=[ [0] ,[1], [68], [135]]
    for ind in range(len(RES_C)):
        tmp=[]
        print()
        print("constraint set "+str(ind)+" under check: ")
        tstm=np.load(config.file_path+'/tst_mat'+str(ind)+'.npy')
        show_L_equ_SKINNY(tstm)
        len_lin=get_linear_len(tstm)
        # print(len_lin)
        nmat,nl_mat=Prepross_eq(tstm,len_lin,RES_C[ind])
        
        #give an pruned equation and a dic list
        equ_dic=check_uniformity(nmat)
        print("=========================================")
        equ_list,equ_dic=show_constraint_set(nmat,equ_dic,nl_mat)   
        tmp.append(equ_list.copy())
        tmp.append(equ_dic.copy())
        print(equ_dic)   
        RES.append(tmp.copy())
    # print(RES)



            



