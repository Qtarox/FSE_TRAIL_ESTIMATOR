from TOOLS.BASIC_OP import *
import config.config as config
from TOOLS.Visual import show_cons_set, show_L_equ_TWINE
from CONS_SOLVE.CONS_SOLVER import final_solve
from GEN_L import *
from RES_CONS import *
from CP_SOLVER.CONS_ES import *
from CP_SOLVER.trans_equ import *
from GUASS.GUASS_COLLECTOR import *
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
            if(gmat[i][j]==1 and (not is_active(j,x_dic,y_dic))):
                res[i][j]=1

    return res

def FEIS_CMP(DC):
    res=[]
    for i in range(len(DC)):
        tmp_in=[]
        tmp_out=[]
        for j in range(8):
            tmp_in.append(DC[i][0][j])
            tmp_in.append(0)
            tmp_out.append(DC[i][1][j])
            tmp_out.append(0)
        res.append([tmp_in.copy(),tmp_out.copy()])
    return res
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
    DC_CMP=FEIS_CMP(DC)
    print(DC_CMP)
    create_folder(file_path)
    creat_dic(file_path,DC_CMP)

    x_dic=load_dic(config.file_path+"act_x.json")
    y_dic=load_dic(config.file_path+"act_y.json")
    gmat=create_GMat(file_path)
    show_L_equ_TWINE(gmat)

    pmat=Prune_gmat(gmat,x_dic,y_dic)
    # show_L_equ_TWINE(pmat)
    np.save(file_path+"P_MAT.npy",pmat)
    res=Guass_Elimin(pmat.copy(),32*(round_num+1))# res is the list of all linear and nonlinear constraints
    with open(file_path+"constraints.txt", "w") as f:
        json.dump(res, f)
    N=10
    # show_L_equ_SKINNY(gmat)
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
