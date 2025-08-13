import numpy as np
import config.config as config
from TOOLS.BASIC_OP import load_dic, corr_ind
x_dic=load_dic(config.file_path+"act_x.json")
y_dic=load_dic(config.file_path+"act_y.json")
from TOOLS.Visual import show_L_equ_SKINNY
np.set_printoptions(linewidth=160,threshold=np.inf)
round_num=config.round_num

def mat_filter(rorder_mat,row_list):
    mat=np.zeros((len(row_list),np.shape(rorder_mat)[1]))
    cnt=0
    for i in row_list:
        mat[cnt]=rorder_mat[i]
        cnt=cnt+1
    return mat

def show_xpos(mat):
    print(np.shape(mat))
    for i in range(np.shape(mat)[0]):
        for j in range(32*round_num):
            if(mat[i][j]==1 and j%32<16):
                print(j//32*16+j%32)

def find_x_pos(array):
    for i in range(np.shape(array)[0]):
        if(array[i]==1 and i%32<16):# find the x_index
            r=i//32
            ind=i%32
            x_ind=r*16+ind
            return x_ind        

def reform_order(mat):
    list=[]
    res=np.zeros(np.shape(mat))
    print(np.shape(mat))
    for i in range(np.shape(mat)[0]):
        row_ind=find_x_pos(mat[i])
        res[row_ind]=mat[i]
        list.append(row_ind)
    print(list)
    return res.astype(int)

def find_active_list(x_dic,y_dic):#return the active x (from x_1 to x_4) and active y (from y_0 to y_3)
    list=[]
    for i in range(32*round_num):
        ind=i%32
        rn=i//32
        if(ind<16):# is a x
            x_rn=rn+1
            x_ind=ind
            k_tmp='x_'+str(x_rn)+'_'+str(x_ind)
            if(k_tmp in x_dic):
                list.append(i)

        else:
            y_rn=rn
            y_ind=ind-16
            k_tmp='y_'+str(y_rn)+'_'+str(y_ind)
            if(k_tmp in y_dic):
                list.append(i)
    return list
#TODO: 1st. Apply QQ's algorithm to activate the fake unconstrainted x and y (guarantee the new algo can find more constraints)
#TODO: 2nd. Find all constraints equations with only 2 unconstrainted variables (including the k variable, and number maybe increased to 3)
#TODO: 3rd. Try to select all the related equations
#TODO: 4th. Check if they satisfy the rule of "N component in N equations"
def find_n_uncons_equ(ro_mat,active_list,n):
    list_equ=[]
    for i in range(np.shape(ro_mat)[0]):
        cnt=0
        for j in range(32*round_num):
            if(ro_mat[i][j]==1 and not(j in active_list)):
                cnt=cnt+1
        if(cnt<=n):
            list_equ.append(i)

    return list_equ

def uncons_xy_equ(chosen_mat,active_list):
    mat=chosen_mat
    for i in range(np.shape(mat)[0]):
        for j in range(32*round_num):
            if(mat[i][j]==1 and j in active_list):
                mat[i][j]=0
    print("The unconstrained variable equations: ")
    show_L_equ_SKINNY(mat)
    return mat

def QQ_alg(ro_mat,active_list):
    row_list=[]
    new_added_x=[]
    semi_active=active_list.copy()
    for i in range(np.shape(ro_mat)[0]):
        flag=True
        for j in range(32*round_num):
            if(ro_mat[i][j]==1):
                if(j%32>15):#is a y element
                    if(j in semi_active):
                        pass
                    else:
                        flag=False
                        break
        if(flag):#put x and corresponding y into the active_list
            rn=i//16+1
            tmp_ind=i%16
            if(rn>=round_num):
                continue
            
            x_ind=(rn-1)*32+tmp_ind
            if(not(x_ind in active_list) and x_ind<32*round_num):
                print("equ "+str(i)+" is found")
                show_L_equ_SKINNY(ro_mat[i].reshape(1,-1))  
                semi_active.append(int(x_ind))
                new_added_x.append(int(x_ind))# new added includes the active x with 0 differential value
                y_ind=rn*32+16+tmp_ind
                if(y_ind<32*round_num):
                    semi_active.append(int(y_ind))     
    print("The new active element list in QQ Algo: \n", semi_active)  
    print("added active element:  \n",new_added_x)         
    return semi_active,new_added_x

def find_start(new_added_x):
    list=[]
    for i in new_added_x:
        rn=i//32
        ind=i%32
        tmp=rn*16+ind
        list.append(tmp)

    return list

def find_uncons_var(equ,active_list):
    equ=np.reshape(equ,(1,-1))
    print(np.shape(equ))
    res=[]
    for i in range(16*round_num):
        if(equ[0][i]==1 and not(i in active_list)):
            res.append(i)
    return res

def mat_reform(ro_mat):
    res=np.zeros((np.shape(ro_mat)[0],16*round_num),dtype=int)
    for i in range(np.shape(ro_mat)[0]):
        for j in range(32*round_num):
            if(ro_mat[i][j]==1):
                rn=j//32
                if(rn+1>=round_num):
                    continue
                if(j%32<16):#is x variable
                    res[i][(rn+1)*16+j%32]=1
                else:#is y variable·   
                    res[i][rn*16+(j%32-16)]=1

    return res

def show_xmat(x_mat):
    for i in range(np.shape(x_mat)[0]):
        l_tmp=""
        flag=False
        
        for j in range(16*round_num):
            rn=j//16
            ind=j%16
            if(flag==False and x_mat[i][j]==1):
                l_tmp=l_tmp+" x_"+str(int(rn))+"_"+str(ind)
                flag=True
            elif(flag==True and x_mat[i][j]==1):
                l_tmp=l_tmp+" + x_"+str(int(rn))+"_"+str(ind)
        if(l_tmp!=""):
            print(l_tmp+"= know constraint")
    
def is_eliminate(con_xmat,arr1):
    tmp=np.zeros((1,np.shape(con_xmat)[1]),dtype=int)
    for i in arr1:
        for j in range(np.shape(con_xmat)[1]):
            tmp[0][j]=tmp[0][j]^con_xmat[i][j]
    for k in range(np.shape(con_xmat)[1]):
        if(tmp[0][k]!=0):
            return False
    return True

def is_include(cur_list,row_uncons):
    #check if there is elements of row_uncons included in cur_list 
    for i in row_uncons:
        for pre_list in cur_list:
            if(i in pre_list):
                return True
    return False


def sorted_mat(x_mat):
    chosen_list=[]
    uc_num_list=[]
    for i in range(np.shape(x_mat)[0]):
        chosen_list.append(i)
        tmp=find_uncons(x_mat[i])
        var_num=len(tmp)
        uc_num_list.append(var_num)

    for i in range(1,len(uc_num_list)):
        for j in range(0,len(uc_num_list)-i):   
            if(uc_num_list[j]<uc_num_list[j+1]):
                uc_num_list[j], uc_num_list[j + 1] = uc_num_list[j + 1], uc_num_list[j]
                chosen_list[j],chosen_list[j+1]=chosen_list[j+1],chosen_list[j]
    y_mat=np.zeros(np.shape(x_mat),dtype=int)  
    for i in range(np.shape(y_mat)[0]):
        y_mat[i]=x_mat[chosen_list[i]]

    return y_mat,chosen_list          


def equ_table(x_mat):
    res=[]
    for j in range(np.shape(x_mat)[1]):
        tmp_list=[]
        for i in range(np.shape(x_mat)[0]):
            if(x_mat[i][j]==1):
                tmp_list.append(i)
        res.append(tmp_list.copy())
    return res #res[i] store the equ index where the element i shows up

def relate_equ_dic(x_mat):
    rows=np.shape(x_mat)[0]
    cols=np.shape(x_mat)[1]
    dic={}
    res=equ_table(x_mat)
    for i in range(rows):
        tmp_list=[]
        for j in range(cols):
            if(x_mat[i][j]==1):#then check the res[j]
                for row_ind in res[j]:
                    if(row_ind>i and not (row_ind in tmp_list)):
                        tmp_list.append(row_ind)
        tmp_list.sort()
        dic[i]=tmp_list.copy()

    return dic

def quick_gen_xmat():#generate a n*8 mat for test
    input_mat1=[[0,1,0,0,0,0,0,0],
               [0,1,1,1,1,0,0,0],
               [0,0,1,0,0,0,0,0],
               [0,0,0,0,1,0,0,0],
               [0,0,0,0,1,0,0,0],
               [0,0,0,0,0,0,0,1],
               [0,0,1,0,1,0,0,1]]
    input_mat=[[0,1,0,0,0,0,0,0],
               [0,1,1,0,0,0,0,0],
               [0,0,1,0,0,0,0,0],
               [0,0,0,1,0,0,0,1],
               [0,0,0,0,1,0,0,0],
               [0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,0,1],
               [0,0,0,1,1,0,0,0]]
    x_mat=np.array(input_mat1,dtype=int)
        
    return x_mat


def scan_equ(x_mat,used_list,tmp_equ_set,const_xMAT, start_ind,RES,equ_dic,limit,xor_val):#can only deal with n<3 suitation
    next_equ_list=[]
    for col_ind in range(np.shape(xor_val)[0]):
        if(xor_val[col_ind]==1):#then check the res[j]
                for row_ind in equ_dic[col_ind]:
                    if(not (row_ind in next_equ_list)):
                        next_equ_list.append(row_ind)
    # print("now tmp_equ_set ",tmp_equ_set," xor_val: ",xor_val)
    # print("next row comes from: ",next_equ_list)

    for i in next_equ_list:

        if(used_list[i]==0 and i>start_ind and len(tmp_equ_set)<=limit):
            tmp_equ_set.append(i)
            tmp=np.bitwise_xor(xor_val, x_mat[i])
            used_list[i]=1
            if(is_eliminate(const_xMAT,tmp_equ_set)):
                tmp_equ_set.sort()
                if(tmp_equ_set in RES):
                    pass
                else:
                    RES.append(tmp_equ_set.copy())
                tmp_equ_set.remove(i)
                used_list[i]= 0
                
            else:
                RES=scan_equ(x_mat,used_list,tmp_equ_set,const_xMAT, start_ind,RES,equ_dic,limit,tmp)  
                tmp_equ_set.remove(i)
                used_list[i]=0
        else:
            pass
    return RES

def find_uncons(row):
    row1=np.reshape(row,(1,-1))
    uc_list=[]
    for i in range(np.shape(row1)[1]): 
        if(row1[0][i]==1):
            uc_list.append(i)
    return uc_list

def FIND_EQU_SET4(x_mat,chosen_list,equ_dic,limit):
    const_xmat=np.copy(x_mat)
    used_list=np.zeros((np.shape(x_mat)[0],),dtype=int)
    tmp_equ_set=[]
    res=[]
    tmp=[]
    for i in range(np.shape(x_mat)[0]):
        # start_uc_list=find_uncons(x_mat[i])
        tmp_equ_set.append(i)
        used_list[i]=1
        xor_val=x_mat[i]
        # cur_list.append(start_uc_list)
        tmp=scan_equ(x_mat,used_list,tmp_equ_set,const_xmat,i,tmp,equ_dic,limit,xor_val)
        tmp_equ_set.remove(i)
        # cur_list.pop(-1)
        used_list[i]=0
    # print(tmp)
    for ele in tmp:
        for j in range(len(ele)):
            ele[j]=chosen_list[ele[j]]
        res.append(ele)
        
    return res    

def Extract_equ(x_mat,limit):
    len_x=np.shape(x_mat)[0]
    equ_dic=equ_table(x_mat)
    # print(equ_dic)
    chosen_list=list(range(0, len_x))
    res=FIND_EQU_SET4(x_mat,chosen_list,equ_dic,limit)
    return res


if __name__=="__main__":

    x_mat1=quick_gen_xmat()
    res=Extract_equ(x_mat1,10)
    print("res: \n", res)