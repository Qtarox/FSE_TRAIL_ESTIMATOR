import numpy as np

def MatPrepro(pmat):
    dic_var_row={}
    for j in range(np.shape(pmat)[1]):
        tmp_list=[]
        for i in range(np.shape(pmat)[0]):
            if(pmat[i][j]==1):
                tmp_list.append(i)
        dic_var_row[j]=tmp_list.copy()
    
    return dic_var_row.copy()
#     [x0,x1,x2,x3,x0x1,x0x2,x0x3,x1x2,x1x3,x2x3,x0x2x3,x1x2x3]
list_0=[4,5,6,10]
list_1=[4,7,8,11]
list_2=[5,7,9,10,11]
list_3=[6,8,9,10,11]
map_L=[list_0,list_1,list_2,list_3]

def CC_dic(dic_var_row):
    CC_DIC=dic_var_row.copy()
    for ind_i in dic_var_row:
        ind=ind_i%256
        if((ind%12)<4 and ind<192):# x linear variable
            new_var_list=[]
            for added in map_L[ind%12]:
                new_var_list.append(added+ind_i-ind%12)
            new_row_list=[]
            for var in new_var_list:
                new_row_list=list(set(new_row_list + dic_var_row[var]))
            CC_DIC[ind_i]=list(set(CC_DIC[ind_i]+new_row_list))
        elif(ind>=192):
            pass
        else:#x nonlinear variables
            CC_DIC[ind_i]=[]
    return CC_DIC

def swap_rows(mat, row1, row2):
    mat[row1], mat[row2] = mat[row2], mat[row1]

def up_triangle(mat):
    list_ind=[[0,i] for i in range(np.shape(mat)[0])]
    res=mat.copy()
    for i in range(np.shape(mat)[0]):
        for j in range(np.shape(mat)[1]):
            if(mat[i][j]==1):
                list_ind[i][0]=j
                break
    sorted_tuples = sorted(list_ind, key=lambda x: x[0])
    print(sorted_tuples)
    for i in range(np.shape(mat)[0]):
        res[i]=mat[sorted_tuples[i][1]]
    return res,sorted_tuples
    
def Guassian_ELM(mat):
    mat,piv_ind_lst=up_triangle(mat)
    row=np.shape(mat)[0]
    col=np.shape(mat)[1]
    for i in range(row):
        pass#for each element in each row, we try to eliminate them one by one
        


if __name__=="__main__":
    mat = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 1, 0, 0]]
    res=up_triangle(mat)
    print(res)