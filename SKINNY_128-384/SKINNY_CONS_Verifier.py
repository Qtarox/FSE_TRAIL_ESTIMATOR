from TOOLS.BASIC_OP import *
import config.config as config
from MAT_GEN.G_MAT import create_GMat
from MAT_GEN.G_MAT2X_MAT import GMat2Xmat,Prune_gmat
from TOOLS.Visual import show_cons_set, show_L_equ_SKINNY
from CP_SOLVER.trans_equ import *
from GUASS.GUASS_COLLECTOR import *
from CONS_ESTMATOR.CONS_ES import *
from RES_CONS import *
file_path=config.file_path
DC=config.DC
Sbox=config.Sbox

def x_ind2g_ind(res,nl_ind_list):
    for i in range(len(res)):
        for j in range(len(res[i])):
            tmp=nl_ind_list[res[i][j]]
            res[i][j]=tmp
    return res

def mat_filter(rorder_mat,row_list):
    mat=np.zeros((len(row_list),np.shape(rorder_mat)[1]))
    cnt=0
    for i in row_list:
        mat[cnt]=rorder_mat[i]
        cnt=cnt+1
    return mat
def save_res(gmat_res):
    cnt=1
    for i in range(len(gmat_res)):
        print("the "+str(cnt)+" equation set is:")
        show_cons_set(gmat,gmat_res[i])
        cnt=cnt+1
        chosen_mat=gmat[gmat_res[i],:].copy()
        np.save(file_path+'/tst_mat'+str(i)+'.npy',chosen_mat)
        chosen_mat.tofile(file_path+'/tst_mat'+str(i)+'.bin')
        # CONS_ES(config.file_path,'/tst_mat'+str(i)+'.npy',gmat_res[i]) 

if __name__=="__main__":
    create_folder(file_path)
    creat_dic(file_path,DC)

    x_dic=load_dic(config.file_path+"act_x.json")
    y_dic=load_dic(config.file_path+"act_y.json")
    gmat=create_GMat(file_path)
    show_L_equ_SKINNY(gmat)

    gmat=gmat.astype(int)
    x_mat,linear_cons,nl_r_ind=GMat2Xmat(gmat,x_dic,y_dic,)
    p_mat=Prune_gmat(gmat,x_dic,y_dic)
    print("trail is: ",config.DC_name)
    print("x_mat shape:",np.shape(x_mat))
    np.save(file_path+"/X_MAT.npy",x_mat)
    print("linear constraints: ")
    print(linear_cons)
    # print(gmat[0])
    # show_cons_set(gmat,linear_cons)
    np.save(file_path+'pmat.npy',p_mat)

    res=Guass_Elimin(p_mat.copy(),32*(round_num+1))# res is the list of all linear and nonlinear constraints
    
    with open(file_path+"constraints.txt", "w") as f:
        json.dump(res, f)
    #constraints is saved in txt, which is the corresponding index of the equtaion in our matrix representation
    N=5
    ok
    show_L_equ_SKINNY(gmat)
    RES_NEW=[]
    for i in res:
        print(len(i))
        if(len(i)<=N):# only choose the size lower than N equations make the equation more solvable
            RES_NEW.append(i)

    save_res(RES_NEW)# generate new simplified shorter constraints which are solvable
    print(RES_NEW)

    RES_CNS,Group_LST=process_cons(RES_NEW)# Group_LST point out the grouping of constraints
    # we provide the original constraint sets here for user to decide if merge these constraints or not, 
    # as some constraints only have one common variable, so grouping them would make the constraints become infeasible
    cnt=0
    
    
    for cons in RES_CNS:# HERE WE SOLVE THE original short constraints
        con_str=cons[0]
        str_f=""
        for str_c in con_str:
            str_f+=str_c
            str_f+="\n"
        cons_dic=cons[1]
        print(str_f)
        SOLVE_CP(str_f,cons_dic,cnt,file_path)
        cnt+=1