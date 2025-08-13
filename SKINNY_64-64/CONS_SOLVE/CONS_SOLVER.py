import numpy as np
# from constant import *
import config.config as config
from TOOLS.BASIC_OP import load_dic,list_xor,corr_ind
x_dic=load_dic(config.file_path+"act_x.json")
y_dic=load_dic(config.file_path+"act_y.json")
from TOOLS.Visual import show_L_equ_SKINNY
from CONS_SOLVE.Merge import  generate_solu_set
from CONS_SOLVE.Merge2 import MAT_XOR, simp_check,independent
np.set_printoptions(linewidth=np.inf,threshold=np.inf)
round_number=config.round_num
Sbox_inv=config.Sbox_inv
Sbox=config.Sbox
full_list=config.full_list
#this solver solve the chosen constraints

def vec_or(v1,v2):
    res=np.zeros(32*(round_number+1)+16)

    res=v1+v2
    #print(res)
    for i in range(32*(round_number+1)+16):
        if(res[0][i]>=1):
            res[0][i]=1
    return res

def MAT_filter(MAT_AB,var_list):
    MAT2=np.zeros((len(var_list),np.shape(MAT_AB)[1]),dtype=int)
    cnt=0
#======================== visualization ============================



def show_MAT_SIZE(MAT_AB,print_flg=1):
    for i in MAT_AB:
        print(np.shape(i))
        if(print_flg==1):
            if(np.shape(i)[0]>200):
                continue
            print(i)
    print()

def show_equ_set(list_equ,linear_equ,list_rhs,linear_rhs,key_ind,rn):
    print("equation set of key "+str(key_ind))
    for i in range(np.shape(linear_equ)[0]):
        print(linear_equ[i],end="  = ")
        print(linear_rhs[i])
    for i in range(np.shape(list_equ)[0]):
        print(list_equ[i],end="  = ")
        if(i>len(list_rhs)-1):
            break
        print(list_rhs[i])

def show_list(list_equ,list_rhs):
    print("List equation corresponding to Linear equ set:  ")
    for i in range(np.shape(list_equ)[0]):
        l_tmp=""
        flag=False
        
        for j in range(32*(round_number+1)):
            rn=j//32
            ind=j%32
            
            if(flag==False and list_equ[i][j]==1):
                if(ind<16):
                    l_tmp=l_tmp+" x_"+str(int(rn))+"_"+str(ind)
                else:
                    l_tmp=l_tmp+" y_"+str(int(rn))+"_"+str(ind-16)
                flag=True
            elif(flag==True and list_equ[i][j]==1):
                if(ind<16):
                    l_tmp=l_tmp+" + x_"+str(int(rn))+"_"+str(ind)
                else:
                    l_tmp=l_tmp+" + y_"+str(int(rn))+"_"+str(ind-16)
        for k in range(16):
            if(list_equ[i][32*(round_number+1)+k]==1):
                l_tmp=l_tmp+" + k_"+str(k)
        l_tmp=l_tmp+'  =  '+str(list_rhs[i])
        print(l_tmp)
#===================================================================
        
def check_active(tmp):# check the active S-box related varibles
    list=[]
    for i in range(32*(round_number+1)):
        if(tmp[0][i]==1):
            
            rn=i//32#IN EACH ROUND, WE SAVE X,Y IN A 32-BITS UNIT
            ind=i%32
            #print("active : "+str(i)+" round "+str(rn)+", index "+str(ind))
            if(ind<16):
                if('x_'+str(rn)+'_'+str(ind) in x_dic):
                    print('x_'+str(rn)+'_'+str(ind),end=" ,  ")
                    list.append(i)
            else:
                
                if('y_'+str(rn)+'_'+str(ind-16) in y_dic):
                    print('y_'+str(rn)+'_'+str(ind-16),end=" ,  ")
                    list.append(i)
    for i in range(16):
        if(tmp[0][i+32*(round_number+1)]==1):
            print("k_"+str(i))

    return list
def equ_to_matA(lhs_eq,rhs_list):
    mat=generate_solu_set(lhs_eq,rhs_list)
    return mat
def equ_to_matB(ACTIVE_NUM,rhs_list,inactive_flag=0):
    ind=ACTIVE_NUM%32
    l=len(rhs_list)
    if(ind<16): #x
        y_num=corr_ind(ACTIVE_NUM)
        if(y_num>32*(round_number+1)):
            res=np.zeros((1,1),dtype=int)
            res[0][0]=ACTIVE_NUM
            for i in range(l):
                tmp=np.zeros((1,1),dtype=int)
                tmp[0][0]=rhs_list[i]
                res=np.vstack([res,tmp])
        else:
            res=np.zeros((1,2),dtype=int)
            res[0][0]=ACTIVE_NUM
            res[0][1]=y_num
            for i in range(l):
                tmp=np.zeros((1,2),dtype=int)
                tmp[0][0]=rhs_list[i]
                tmp[0][1]=Sbox[rhs_list[i]]
                res=np.vstack([res,tmp])        
    else: # y
        x_num=corr_ind(ACTIVE_NUM)
        if(x_num<0):# because x_0_i never appears in linear equations, so we just give it up
            res=np.zeros((1,1),dtype=int)
            res[0][0]=ACTIVE_NUM
            for i in range(l):
                tmp=np.zeros((1,1),dtype=int)
                tmp[0][0]=rhs_list[i]
                res=np.vstack([res,tmp])
        else:
            res=np.zeros((1,2),dtype=int)
            res[0][1]=ACTIVE_NUM
            res[0][0]=x_num
            for i in range(l):
                tmp=np.zeros((1,2),dtype=int)
                tmp[0][1]=rhs_list[i]
                tmp[0][0]=Sbox_inv[rhs_list[i]]
                res=np.vstack([res,tmp])  
    return res
def generate_mat_list(ind_list,linear_equ,list_rhs,linear_rhs):
    mat_list=[]
    len_linear=np.shape(linear_equ)[0]
    for i in range(len_linear):
        tmp_matA=equ_to_matA(linear_equ[i],linear_rhs[i])
        mat_list.append(tmp_matA.astype(int))

    for i in range(len(list_rhs)):
        tmp_matB=equ_to_matB(ind_list[i],list_rhs[i])
        mat_list.append(tmp_matB.astype(int))

    return mat_list

def generate_list_equ(L_mat,var_list):#L_mat size(n,32*round_number+16)
    tmp=np.zeros((1,32*(round_number+1)+16),dtype=int)
    for i in range(np.shape(L_mat)[0]):
        tmp=vec_or(tmp,L_mat[i])
    print("variables: ")
    ind_list=check_active(tmp)# the index number of active elements in linear equation
    list_equ=np.zeros((1,32*(round_number+1)+16),dtype=int)
    rhs=[]
    flag=True
    print(ind_list)
    for i in var_list:
        line=np.zeros((1,32*(round_number+1)+16),dtype=int)
        
        line[0][i]=1
        if(i in ind_list):
            ind=i%32
            rn=i//32
            if(ind<16):#x_r_i
                list_tmp=x_dic['x_'+str(rn)+'_'+str(ind)]
            else:    
                list_tmp=y_dic['y_'+str(rn)+'_'+str(ind-16)]
            rhs.append(list_tmp.copy())
            if(flag==True):
                list_equ=line
                flag=False
            else:
                list_equ=np.vstack((list_equ,line))
        else:
            list_tmp=full_list.copy()
            rhs.append(list_tmp.copy())
            if(flag==True):
                list_equ=line
                flag=False
            else:
                list_equ=np.vstack((list_equ,line))
    
    print("active list",ind_list)
    
    return ind_list,list_equ,rhs

def reform_Linear(mat):#prepare the linear mat for solution
    rhs=[]
    for i in range(np.shape(mat)[0]):
        tmp1=[0]
        rhs.append(tmp1.copy())
    return mat,rhs

def empty_MAT(mat):
    if(np.shape(mat)[0]<=1):
        return True
    return False

def get_var(mat):#find element in the equation set
    tmp=np.zeros((1,np.shape(mat)[1]),dtype=int)
    for i in range(np.shape(mat)[0]):
        tmp=tmp+mat[i]
    var=[]
    for j in range(32*(round_number+1)):
        if(tmp[0][j]>0):
            var.append(j)
    return var

def swap(mat,list,ind,j):# swap list
    tmp=mat[ind].copy()
    mat[ind]=mat[j].copy()
    mat[j]=tmp.copy()
    lt=list[ind].copy()
    list[ind]=list[j].copy()
    list[j]=lt.copy()
    return mat,list

def MAT_SWAP(MAT_AB,ind,j):
    #print("MAT swap row "+str(ind)+" and row "+str(j))
    tmp=MAT_AB[ind]
    MAT_AB[ind]=MAT_AB[j]
    MAT_AB[j]=tmp
    return MAT_AB

def up_tri(mat,list,k,MAT_AB,len_linear):
    ind=k #just need to take care of the rows below k-th row
    changed=False
    for j in range(k+1,np.shape(mat)[0]):
        cur_ind=find_one(mat[ind])
        next=find_one(mat[j])
        if(cur_ind>next):
            changed=True
            print("now swap row "+str(ind)+" and row "+str(j))
            mat,list=swap(mat,list,ind,j)
            MAT_AB=MAT_SWAP(MAT_AB,ind+len_linear,j+len_linear)
            ind=j
        else:
            break
    return mat,list,MAT_AB,changed

def find_one(vec):#find the first none-zero element in the equation
    for i in range(np.shape(vec)[0]):
        if(vec[i]==1):
            return i
    return -1
def row_overlap(r1,r2):
    for i in range(np.shape(r1)[0]):
        if(r1[i]>0 and r2[i]>0):
            return True
    return False

def vec_xor(v1,v2):
    v1=v1.astype(int)
    v2=v2.astype(int)
    res=np.zeros(np.shape(v1),dtype=int)
    for i in range(np.shape(v1)[0]):
        res[i]=v1[i]^v2[i]
    return res
def intersect(l1,l2):
    res=[]
    for i in l1:
        if(i in l2):
            res.append(i)
    return res

def list_ind(linear_mat,list_mat):#return list of indexs of first nonzero elements
    one_ind=[]
    for i in range(np.shape(linear_mat)[0]):
        one_ind.append(find_one(linear_mat[i]))
    for i in range(np.shape(list_mat)[0]):
        one_ind.append(find_one(list_mat[i]))
    return one_ind
def get_B_IND(list_equ):
    list=[]
    for i in range(np.shape(list_equ)[0]):
        tmp=find_one(list_equ[i])
        list.append(tmp)
    
    return list
def extract_col(mat,ind_list):
    res=np.zeros((np.shape(mat)[0],len(ind_list)),dtype=int)
    mat_ind=[]
    for j in range(np.shape(mat)[1]):
        for i in ind_list:
            if(i==mat[0][j]):
                mat_ind.append(j)
                break
    for cnt in range(len(mat_ind)):
        for i in range(np.shape(mat)[0]):
            res[i][cnt]=mat[i][mat_ind[cnt]]
    res=simplify(res)
    return res

def get_constraint_key_prob(mat, ind_list):
    list_cnt=[0 for _ in range(16**(len(ind_list)))]
    for i in range(1,np.shape(mat)[0]):
        tmp_ind=0
        for j in range(len(ind_list)):
            tmp_ind=tmp_ind*16+mat[i][ind_list[j]]
            # print(tmp_ind)
        list_cnt[tmp_ind]=list_cnt[tmp_ind]+1
    return list_cnt

def simplify(mat):
    ind=np.zeros((1,np.shape(mat)[1]))
    ind=mat[0]
    tmp=np.unique(mat[1:][:],axis=0)
    res=np.vstack([ind,tmp])

    return res

def equ_relation(list_mat,linear_mat):
    relate_list=[]
    ind_list=[]
    ind_linear=[]
    for i in range(np.shape(linear_mat)[0]):
        tmp_list1=[]
        for j in range((round_number+1)*32):
            if(linear_mat[i][j]==1):
                tmp_list1.append(j)
        ind_linear.append(tmp_list1.copy())
    for i in range(np.shape(list_mat)[0]):
        tmp_list2=[]
        for j in range((round_number+1)*32):
            if(list_mat[i][j]==1):
                tmp_list2.append(j)
                tmp_list2.append(corr_ind(j))
        ind_list.append(tmp_list2.copy())
    for i in range(np.shape(linear_mat)[0]):
        tmp=[]
        for j in ind_linear[i]:
            for k in range(len(ind_list)):
                if(j in ind_list[k]):
                    tmp.append(k)
                    break
                
        relate_list.append(tmp.copy())
    return relate_list

def get_new_mat(LEQU_MAT):
    NEW_MAT=[np.copy(LEQU_MAT[0])]
    cnt=1
    equ_ind=0
    final_order=[]
    remain_list=list(range(len(LEQU_MAT)))
    final_order.append(0)
    
    while(cnt<len(LEQU_MAT)):
        for ind in remain_list:
            # print(equ_ind,ind)
            if(ind in final_order):
                continue
            if(independent(NEW_MAT[equ_ind][0],LEQU_MAT[ind][0])):
                pass
            else:
                NEW_MAT.append(np.copy(LEQU_MAT[ind]))
                cnt=cnt+1
                
                final_order.append(ind)
        equ_ind=equ_ind+1
    return NEW_MAT

def evaluate_prob(key_dis_lst):#this list record the times of appearence for the key combination
    dic_prob={}
    freq_list=[]
    for i in key_dis_lst:
        if(i in dic_prob):
            dic_prob[i]=dic_prob[i]+1
        else:
            freq_list.append(i)
            dic_prob[i]=1
    total_num=0
    for i in range(len(freq_list)):
        total_num=total_num+freq_list[i]*dic_prob[freq_list[i]]
    

    return dic_prob


def solve_cluster2(MAT_AB,list_mat,linear_mat,list_rhs,linear_rhs,list_active,linear=False):
    #1 merge all linear and nonlinear constraints

    len_linear=np.shape(linear_mat)[0]
    relate_list=equ_relation(list_mat,linear_mat)
    print(relate_list)
    LEQU_MAT=[]
    for equ_ind in range(len_linear):
        MAT_tmp=MAT_AB[equ_ind]
        for j in relate_list[equ_ind]:
            MAT_tmp=MAT_XOR(MAT_tmp,MAT_AB[len_linear+j])
        LEQU_MAT.append(np.copy(MAT_tmp))
    
    #2 merge all the equations
    # print("final solving:")
    
    NEW_MAT=get_new_mat(LEQU_MAT)
    Final_mat=NEW_MAT[0]
    # NEW_MAT=[LEQU_MAT[0],LEQU_MAT[1],LEQU_MAT[3],LEQU_MAT[4],LEQU_MAT[2]]
    for i in range(len_linear):
        if(i==0):
            pass
        else:
            Final_mat=MAT_XOR(Final_mat,NEW_MAT[i])
    key_list=[]
    key_ind_lst=[]
    print("Final mat shape: ",np.shape(Final_mat))
    for i in range(np.shape(Final_mat)[1]):
        if(Final_mat[0][i]>=32*(round_number+1)):
            key_list.append(Final_mat[0][i])
            key_ind_lst.append(i)
    print("key involved: ", key_list)
    key_distri_lst=get_constraint_key_prob(Final_mat,key_ind_lst)
    key_rows=extract_col(Final_mat,key_list)
    print(np.shape(key_rows))
    print("keys: ")
    print(key_rows)
            
    return key_list,key_distri_lst

   

def final_solve(file_path,mat_name,flg_linear=False):
    
    #active_equ=[4, 7, 20, 21, 24, 25, 28, 29, 38, 42, 46, 55, 59, 63, 70]
    print("==================================================================================================================")
    print("========================================== START SOLVING ========================================================= ")
    print("==================================================================================================================")
    chosen_mat=np.load(file_path+mat_name)
    #print(np.shape(mat))
    #print("l_mat")
    var_list=get_var(chosen_mat)
    print("VARIABLES INDEX in the equ set:/n",var_list)
    print()
    list_active,list_equ,list_rhs=generate_list_equ(chosen_mat,var_list)

    linear_equ,linear_rhs=reform_Linear(chosen_mat)
    #TO DO: GENERATE MATS FROM list_active.list_equ,list_rhs . linear_equ,linear_rhs
    #linear_equ,linear_rhs=reduce_equ(linear_mat=linear_equ,linear_list=linear_rhs,list_active=list_active)
    MAT_AB=generate_mat_list(var_list,linear_equ,list_rhs,linear_rhs)#TODO: this part need to be checked, especially the SBOX related x,y 
    #MAT_AB=MAT_filter(MAT_AB,var_list)
    show_L_equ_SKINNY(linear_equ)
    show_list(list_equ,list_rhs)
    show_MAT_SIZE(MAT_AB)
    

    key_list,key_distri_lst=solve_cluster2(MAT_AB,list_equ,linear_equ,list_rhs,linear_rhs,list_active,linear=flg_linear)
    key_dic=evaluate_prob(key_distri_lst)
    return key_list,key_dic
    #return MAT_res,key_mat

def final_solve_mat(mat,flg_linear=False):
    
    #active_equ=[4, 7, 20, 21, 24, 25, 28, 29, 38, 42, 46, 55, 59, 63, 70]
    print("==================================================================================================================")
    print("========================================== START SOLVING ========================================================= ")
    print("==================================================================================================================")
    chosen_mat=mat.copy()
    #print(np.shape(mat))
    #print("l_mat")
    var_list=get_var(chosen_mat)
    print("VARIABLES INDEX in the equ set:/n",var_list)
    print()
    list_active,list_equ,list_rhs=generate_list_equ(chosen_mat,var_list)

    linear_equ,linear_rhs=reform_Linear(chosen_mat)
    #TO DO: GENERATE MATS FROM list_active.list_equ,list_rhs . linear_equ,linear_rhs
    #linear_equ,linear_rhs=reduce_equ(linear_mat=linear_equ,linear_list=linear_rhs,list_active=list_active)
    MAT_AB=generate_mat_list(var_list,linear_equ,list_rhs,linear_rhs)#TODO: this part need to be checked, especially the SBOX related x,y 
    #MAT_AB=MAT_filter(MAT_AB,var_list)
    show_L_equ_SKINNY(linear_equ)
    show_list(list_equ,list_rhs)
    show_MAT_SIZE(MAT_AB)

    key_list,key_distri_lst=solve_cluster2(MAT_AB,list_equ,linear_equ,list_rhs,linear_rhs,list_active,linear=flg_linear)
    key_dic=evaluate_prob(key_distri_lst)
    return key_list,key_dic
    #return MAT_res,key_mat
if __name__=="__main__":
    final_solve(file_path=config.file_path,mat_name="tst_mat.npy")

      
   
