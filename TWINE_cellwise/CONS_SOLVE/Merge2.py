import numpy as np

np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=400)
N=16

def list_common(i1,i2):
    common=[]
    for i in i1:
        if(i in i2):
            common.append(i)
    return common

def independent(i1,i2):
    for i in i1:
        if(i in i2):
            return False
    return True
    
##ancient code
def get_com_ind(array1, array2):
    list=[]
    for i in array1:
        if(i in array2):
            list.append(i)
    list=np.array(list)
    return list

def create_common_table(list):
    t_num=N**len(list)
    res=[]
    tmp=[]
    for i in range(t_num):
        res.append(tmp.copy())
    return res

def locate(ind_row,com_ind):
    cnt=0
    ind_row=np.reshape(np.array(ind_row),(1,-1))
    com_ind=np.reshape(com_ind,(1,-1))
    res=[]

    for i in range(np.shape(ind_row)[1]):
        if(cnt>=np.shape(com_ind)[1]):
            break

        if(com_ind[0][cnt]==ind_row[0][i]):
            res.append(i)
            cnt=cnt+1
    return np.array(res)

def ind_merge(i1,i2):
    res=[]
    cnt1=0
    cnt2=0
    while(cnt1<np.shape(i1)[0] or cnt2<np.shape(i2)[0]):
        if(cnt1==np.shape(i1)[0]):
            res.append(i2[cnt2])
            cnt2=cnt2+1
        elif(cnt2==np.shape(i2)[0]):
            res.append(i1[cnt1])
            cnt1=cnt1+1
        else:
            if(i1[cnt1]<i2[cnt2]):
                res.append(i1[cnt1])
                cnt1=cnt1+1
            elif(i1[cnt1]>i2[cnt2]):
                res.append(i2[cnt2])
                cnt2=cnt2+1
            else:
                res.append(i1[cnt1])
                cnt1=cnt1+1
                cnt2=cnt2+1               

    return np.array(res.copy())

def check_row(arr,col_ind):
    res=0
    for i in col_ind:
        tmp=arr[i]
        res=res*N+tmp
    return res


def fill_in(com_ind,mat,com_table):
    ind_row=mat[0]
    col_ind=locate(ind_row,com_ind)
    for i in range(np.shape(mat)[0]):
        if(i==0):
            continue
        group_num=int(check_row(mat[i],col_ind))#determine the list_group the row belong
        com_table[group_num].append(i)
    return com_table

def common_solution(com_t1,com_t2):
    t_len=len(com_t1)
    res=[]
    solu_num=0
    for i in range(t_len):
        tmp=[]
        if(len(com_t1[i])!=0 and len(com_t2[i])!=0):
            tmp.append(i)
            tmp.append(com_t1[i])
            tmp.append(com_t2[i])
            res.append(tmp)
            solu_num=solu_num+len(com_t1[i])*len(com_t2[i])
    return solu_num,res

def final_solu(solu_num,com_solu,merge_ind,mat1,mat2):
    merge_ind=np.reshape(merge_ind,(1,-1))
    col_num=np.shape(merge_ind)[1]
    res=np.zeros((solu_num+1,col_num),dtype=int)
    res[0]=merge_ind
    ind_list1=locate(merge_ind,mat1[0])
    ind_list2=locate(merge_ind,mat2[0])
    #print(ind_list1)
    #print(ind_list2)
    cnt=1
    for i in com_solu:
        m1_sol=i[1]
        m2_sol=i[2]
        for j in range(len(m1_sol)):
            r1_ind=m1_sol[j]
            for k in range(len(m2_sol)):
                r2_ind=m2_sol[k]
                for c1 in range(len(ind_list1)):
                    res[cnt][ind_list1[c1]]=mat1[r1_ind][c1]
                for c2 in range(len(ind_list2)):
                    res[cnt][ind_list2[c2]]=mat2[r2_ind][c2]
                cnt=cnt+1


    return res
def simp_check(mat,MAT_B,activelist):
    ind1=mat[0]
    res=mat

    for i in ind1:
        i=int(i)
        if(i<160 and (i in activelist)):
            res=MAT_XOR(res,MAT_B[i])
    print("shape after cut off:", np.shape(res))
    return res

def MAT_XOR(mat1,mat2):
    mat1=mat1.astype(int)
    mat2=mat2.astype(int)
    if(independent(mat1[0],mat2[0])):
        print("independent matrices, no need to take care")
        return -1
    # print("begin merge")
    # print("mat1 size:",np.shape(mat1))
    # print("mat2 size:",np.shape(mat2))
    #if(np.shape(mat1)[0]*np.shape(mat2)[0]>4097*260000):
    #    print("too large to calculate")
    #    return -1
    common_ind=get_com_ind(mat1[0],mat2[0])
    merge_ind=ind_merge(mat1[0],mat2[0])

    com_t1=create_common_table(common_ind)
    com_t2=create_common_table(common_ind)
    com_t1=fill_in(common_ind,mat1,com_t1)
    com_t2=fill_in(common_ind,mat2,com_t2)
    solu_num,com_solu=common_solution(com_t1,com_t2)
    #print(com_solu)
    mat=final_solu(solu_num,com_solu,merge_ind,mat1,mat2)

    #print(mat)
    #if (merge_mat.ndim==1):
    #    merge_mat=merge_mat.reshape(1,-1)
    #return merge_mat
    return mat

def independent(i1,i2):
    for i in i1:
        if(i in i2):
            return False
    return True

if __name__=="__main__":
    mat=[[2,3,4,5],
         [1,1,1,1],
         [1,2,1,1],
         [1,2,0,1],
         [1,0,1,0], 
         [1,2,1,1]]
    mat1=[[4],
          [1],
          [2],
          [3]]
    mat3=[[5],
          [1]]
    mat2=[[1,2,4,10],
         [1,3,1,1],
         [1,4,3,1],
         [1,2,1,1],
         [1,1,6,1]]


    merge_mat=MAT_XOR(np.array(mat1),np.array(mat3))
    
    
    #print(np.shape(res1))
    #print(np.shape(comm_sol))


 