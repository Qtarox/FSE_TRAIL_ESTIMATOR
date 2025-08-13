import numpy as np

np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=400)
def generate_solu_set(arr1,rhs_list):#return all possible combination of the variables in this list
    #arr1 stands for the 0,1 vector of the left hand side of equation
    #rhs_list stands for the possible result for the equation
    if(np.all(arr1) and rhs_list!=[]):
        return -1
    elif(np.all(arr1)==False and rhs_list==[]):
        return -1
    elif(np.all(arr1)==False and rhs_list!=[]):
        # solu_set is two dimension array the first row is the index of 
        ind_arr=extract(arr1)
        res=ind_arr
        for i in rhs_list:
            tmp=tranverse(res,[],i,ind_arr,0,0)
            res=tmp

        return res

def extract(arr):
    list_tmp=[]
    for i in range(len(arr)):
        if(arr[i]==1):
            list_tmp.append(i)
    ind_arr=np.array(list_tmp)
    return ind_arr

def tranverse(res,tmp_row,num,ind_arr,curr_ind,curr_sum):
    #1.extract the index of the first row
    #num corresponding to the number value of the rhs_list

    if(curr_ind==len(ind_arr)-1):
        rest_sum=curr_sum^num
        tmp_row.append(rest_sum)
        res = np.vstack([res, np.array(tmp_row.copy())])
        tmp_row.pop(-1)
        return res
    for i in range(16):
        tmp_sum=curr_sum^i
        tmp_row.append(i)
        
        res=tranverse(res,tmp_row,num,ind_arr,curr_ind+1,tmp_sum)
        tmp_row.pop(-1)
    return res


def intersec(i1,i2):
    res=[]
    for i in i1:
        if(i in i2):
            res.append(i)

    return np.array(res.copy())


def get_ind_inter(ind,common_ind):# given a mat and common ind, return the corresponding column numbers
    res=[]
    for i in common_ind:
        for j in range(np.shape(ind)[0]):
            if(i==ind[j]):
                res.append(j)
                break
    #res_ind=res.copy()           
    return res


def list_merge(i1,i2):
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

def array_less(a1,a2):

    len=np.shape(a1)[0]
    for i in  range(len):
        if(a1[i]<a2[i]):
            return True
        elif(a1[i]>a2[i]):
            return False
        else:
            continue
    print("equal")
    return False

def smerge_mat(m1,m2):
    len=np.shape(m1)[0]+np.shape(m2)[0]
    cnt1=0
    cnt2=0
    if(array_less(m1[0],m2[0])):
        res=m1[0]
        cnt1=cnt1+1
    else:
        res=m2[0]
        cnt2=cnt2+1
    for i in range(len-1):
        if(cnt1>np.shape(m1)[0]-1):
            res=np.vstack([res,m2[cnt2]])
            cnt2=cnt2+1

        elif(cnt2>np.shape(m2)[0]-1):
            res=np.vstack([res,m1[cnt1]])
            cnt1=cnt1+1
        else:
            if(array_less(m1[cnt1],m2[cnt2])):
                res=np.vstack([res,m1[cnt1]])
                cnt1=cnt1+1
            else:
                res=np.vstack([res,m2[cnt2]])
                cnt2=cnt2+1
    return res

def array_equal_prime(a1,a2,ind1,ind2):
    len=np.shape(ind1)[0]
    for i in range(len):
        if(a1[int(ind1[i])]<a2[int(ind2[i])]):
            return False
        elif(a1[int(ind1[i])]>a2[int(ind2[i])]):
            return False
        else:
            continue
    return True

def array_less_prime(a1,a2,ind1,ind2):#compare the element denoted by the ind_array
    len=np.shape(ind1)[0]
    #print("inter_ind",ind1)
    #print("common_ind",ind2)
    for i in range(len):
        if(a1[int(ind1[i])]<a2[int(ind2[i])]):
            return True
        elif(a1[int(ind1[i])]>a2[int(ind2[i])]):
            return False
        else:
            continue
    return False

def smerge_mat_prime(m1,m2,ind):
    len=np.shape(m1)[0]+np.shape(m2)[0]
    cnt1=0
    cnt2=0
    if(array_less_prime(m1[0],m2[0],ind,ind)):
        res=m1[0]
        cnt1=cnt1+1
    else:
        res=m2[0]
        cnt2=cnt2+1
    for i in range(len-1):
        if(cnt1>np.shape(m1)[0]-1):
            res=np.vstack([res,m2[cnt2]])
            cnt2=cnt2+1

        elif(cnt2>np.shape(m2)[0]-1):
            res=np.vstack([res,m1[cnt1]])
            cnt1=cnt1+1
        else:
            if(array_less_prime(m1[cnt1],m2[cnt2],ind,ind)):
                res=np.vstack([res,m1[cnt1]])
                cnt1=cnt1+1
            else:
                res=np.vstack([res,m2[cnt2]])
                cnt2=cnt2+1
    return res

def mat_sort_prime(mat,ind):
    if (np.shape(mat)[0] <= 1):
        return mat  

    mid = np.shape(mat)[0] // 2  
    left_half = mat[:mid]  
    right_half = mat[mid:]  

    left_half = mat_sort_prime(left_half,ind) 
    right_half = mat_sort_prime(right_half,ind)  

    return smerge_mat_prime(left_half, right_half,ind) 

def mat_sort(mat):
    if (np.shape(mat)[0] <= 1):
        return mat  

    mid = np.shape(mat)[0] // 2  
    left_half = mat[:mid]  
    right_half = mat[mid:]  

    left_half = mat_sort(left_half) 
    right_half = mat_sort(right_half)  

    return smerge_mat(left_half, right_half) 

def prune(mat):
    ind=mat[0]
    original_matrix=mat[1:]
    unique_matrix, indices = np.unique(original_matrix, axis=0, return_index=True)
    mat_res=np.vstack([ind,unique_matrix])
    return mat_res

def get_common_solu(pmat1,pmat2):#extract all common solution 
    mat_common=pmat1[0]
    tmp1=prune(pmat1)[1:]
    tmp1=mat_sort(tmp1)
    tmp2=prune(pmat2)[1:]
    tmp2=mat_sort(tmp2)

    cnt2=0
    i=0

    while(i <np.shape(tmp1)[0]):
        if(cnt2>np.shape(tmp2)[0]-1):
            break
        if((tmp1[i]==tmp2[cnt2]).all()):
            mat_common=np.vstack([mat_common,tmp1[i]])
            i=i+1
        else:
            if(array_less(tmp1[i],tmp2[cnt2])):
                i=i+1
            else:
                cnt2=cnt2+1
    #print("mat",mat_common)
    return mat_common

def get_ind_com(array_com):
    res=np.zeros_like(array_com)
    print(np.shape(res))
    for i in range(np.shape(res)[0]):
        res[i]=i
    return res



def get_premat(ind,mat):
    init=ind[0]
    res=mat[:,init]
    for i in ind:
        if(i==init):
            continue
        else:
            res=np.column_stack([res,mat[:,i]])
    return res

def simplify(mat,common_solu):#only preserve the valid soultion in mat
    ind=mat[0]
    res=ind
    print("ind: ",ind)
    if(common_solu.ndim==1):
        common_solu=common_solu.reshape(1,-1)

    com_ind=get_ind_com(common_solu[0])
    
    inter_ind=get_ind_inter(ind,common_solu[0])
    #print("inter_ind: ",inter_ind)
    mat_tmp=mat_sort_prime(mat[1:],inter_ind)
    com_tmp=common_solu[1:]

    cnt=0
    i=0
    while( i <np.shape(mat_tmp)[0]):
        if(cnt>=np.shape(com_tmp)[0]):
            break
        if(array_less_prime(mat_tmp[i],com_tmp[cnt],inter_ind,com_ind)):
            i=i+1
        elif(array_equal_prime(mat_tmp[i],com_tmp[cnt],inter_ind,com_ind)):
            res=np.vstack([res,mat_tmp[i]])
            i=i+1
        else:
            cnt=cnt+1
            

    #print(res)
    return res

def intersec_solu(mat1,mat2):#get the solution set for the common index array
    ind1=mat1[0]
    ind2=mat2[0]
    if(independent(ind1,ind2)):
        print("independent matrices, no need to take care")
        return 
    merge_mat=list_merge(ind1,ind2)# the index for merge list
    common_ind=list_common(ind1,ind2)

    inter_ind1=get_ind_inter(ind1,common_ind)#return the index in mat1 for these common_ind elements
    #print("interind1:", inter_ind1)
    inter_ind2=get_ind_inter(ind2,common_ind)
    #print("interind2:", inter_ind2)
    pre_mat1=get_premat(inter_ind1,mat1)#extract pre_mat for these  matrices
    pre_mat2=get_premat(inter_ind2,mat2)
    if (pre_mat1.ndim==1):
        pre_mat1=pre_mat1.reshape(-1,1)
    if (pre_mat2.ndim==1):
        pre_mat2=pre_mat2.reshape(-1,1)
    #print(np.shape(pre_mat1))

    common_solu=get_common_solu(pre_mat1,pre_mat2)
    #return mat1 part and mat2 part 
    mat1_simp=simplify(mat1, common_solu)
    #print("mat1_simp",mat1_simp)
    #print("simplified mat1 size:", np.shape(mat1_simp))
    mat2_simp=simplify(mat2, common_solu)
    #print("mat2_simp",mat2_simp)
    #print("simplified mat2 size:", np.shape(mat2_simp))
    merge_mat=MAT_MERGE(mat1_simp,mat2_simp,inter_ind1,inter_ind2)
    return merge_mat
    
    #return mat1_simp
def MAT_MERGE(mat1,mat2,ref_ind1,ref_ind2):
    if(mat1.ndim==1):
        mat1=mat1.reshape(1,-1)
    if(mat2.ndim==1):
        mat2=mat2.reshape(1,-1)
    ind_1=mat1[0]
    ind_2=mat2[0]
    m1=mat1[1:]
    m2=mat2[1:]
    m_ind=list_merge(ind_1,ind_2)
    list1=locate(ind_1,m_ind)
    list2=locate(ind_2,m_ind)
    merge_mat=m_ind
    for i in range(np.shape(m1)[0]):
        for j in range(np.shape(m2)[0]):
            if(array_equal_prime(m1[i],m2[j],ref_ind1,ref_ind2)):
                tmp_row=merge_row(m1[i],m2[j],list1,list2,m_ind)
                merge_mat=np.vstack([merge_mat,tmp_row])
    return merge_mat

def merge_row(row1,row2,list1,list2,m_ind):
    row=np.zeros_like(m_ind)
    for i in range(np.shape(row1)[0]):
        row[list1[i]]=row1[i]
    for j in range(np.shape(row2)[0]):
        if(row[list2[j]]!=0):
            continue
        row[list2[j]]=row2[j]

    return row

def locate(ind,merged):
    res=[]
    for i in ind:
        for j in range(np.shape(merged)[0]):
            if(i==merged[j]):
                res.append(j)
                break
    return np.array(res.copy())


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
    
def Set_xor(lhs_eq1,lhs_eq2,rhs_list1,rhs_list2):
    res1=generate_solu_set(lhs_eq1,rhs_list1)
    res2=generate_solu_set(lhs_eq2,rhs_list2)
    print("mat1 size:",np.shape(res1))
    print("mat2 size:",np.shape(res2))
    merge_mat=intersec_solu(res1,res2)
    return merge_mat
def MAT_XOR(mat1,mat2):
    print("begin merge")
    print("mat1 size:",np.shape(mat1))
    print("mat2 size:",np.shape(mat2))
    if(np.shape(mat1)[0]*np.shape(mat2)[0]>10000000):
        print("too large to calculate")
        return -1
    merge_mat=intersec_solu(mat1,mat2)
    print(np.shape(merge_mat))
    if (merge_mat.ndim==1):
        merge_mat=merge_mat.reshape(1,-1)
    return merge_mat

if __name__=="__main__":
    tst1=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    tst2=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rhs_list1=[0]
    rhs_list2=[0,1]  
    test1=[[1,2],[0,1]]
    test2=[[1,2],[1,0]]


    merge_mat=MAT_XOR(np.array(test1),np.array(test2))
    print(merge_mat)
    print("merged mat size",np.shape(merge_mat))
    
    #print(np.shape(res1))
    #print(np.shape(comm_sol))


 