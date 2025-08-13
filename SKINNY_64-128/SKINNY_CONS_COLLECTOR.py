from TOOLS.BASIC_OP import *
import config.config as config
from MAT_GEN.G_MAT import create_GMat
from MAT_GEN.G_MAT2X_MAT import GMat2Xmat,Prune_gmat
from TOOLS.Visual import show_cons_set, show_L_equ_SKINNY
from CONS_COLLECTOR.CONS_FINDER import Extract_equ 
from CONS_COLLECTOR.MILP_COLLECTOR import get_LIST0
from CONS_SOLVE.CONS_SOLVER import final_solve
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

    RESDC5=[[9, 11, 27], [7]]
    RESDC4=[[0, 2, 17, 30, 44, 62, 128, 148, 155, 169]]#, [10, 11, 13, 31, 40, 135, 138, 152]]
    RESDC7=[ [12, 27], [12, 25]]
    RESDC71=[[4, 5, 29, 69]]
    RESDC2=[ [18, 41, 43], [1,28,39, 62], [10], [17], [20], [58]]
    # res=Extract_equ(x_mat,5)
    # res=get_LIST0(file_path+"/X_MAT.npy")
    # res= [[0, 2, 24, 26], [4, 15, 17]]
    # res=[[1, 25], [16, 38, 40], [36, 58]]
    # res=[[8, 10, 26], [9, 10, 12, 30, 38]]
    #  [[0, 2, 16, 29, 42, 60], [8, 9, 12, 26, 30, 38], [8, 10, 26], [9, 10, 12, 30, 38]] 7R


    # print("resluts: \n", RESDC5)
    cnt=1
    gmat_res=RESDC4
    FINAL_RES=[]
    for i in range(len(gmat_res)):
        tmp=[]
        print("the "+str(cnt)+" equation set is:")
        show_cons_set(gmat,gmat_res[i])
        cnt=cnt+1
        chosen_mat=gmat[gmat_res[i],:].copy()
        np.save(file_path+'/tst_mat'+str(i)+'.npy',chosen_mat)
        chosen_mat.tofile(file_path+'/tst_mat'+str(i)+'.bin')
        key_list,key_dic=final_solve(file_path=config.file_path,mat_name='/tst_mat'+str(i)+'.npy') 
        tmp.append(key_list)
        tmp.append(key_dic)
        FINAL_RES.append(tmp.copy())
    print("Final results:")
    print(FINAL_RES)