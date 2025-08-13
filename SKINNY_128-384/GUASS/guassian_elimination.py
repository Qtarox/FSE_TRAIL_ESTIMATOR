import config.config as config
from TOOLS.Visual import show_L_equ_SKINNY
import numpy as np
file_pth=config.file_path

def XOR(MAT,r1,r2):
    for j in range(np.shape(MAT)[1]):
        MAT[r1][j]^=MAT[r2][j]

# void swapRow(uint8_t **M, int r1, int r2){
# 	uint8_t *t = M[r1];
# 	M[r1] = M[r2];
# 	M[r2] = t;
# }
list_0=[4,5,6,10]
list_1=[4,7,8,11]
list_2=[5,7,9,10,11]
list_3=[6,8,9,10,11]
map_L=[list_0,list_1,list_2,list_3]
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

def equation_absorb(arr1,arr2):
    # print(np.shape(arr1))
    # print("arr1: ",arr1)
    # print("arr2: ",np.array(arr2,dtype=int))
    res=np.zeros(np.shape(arr1),dtype=int)
    for i in range(np.shape(arr1)[0]):
        ind=i%256
        if(ind<192 and (ind%12)>=4):# x nonlinear variables
            res[i]=int(arr1[i]) ^ int(arr2[i])
        elif(ind>=192):# y linear
            res[i]=int(arr1[i]) ^ int(arr2[i])
    for i in range(np.shape(arr1)[0]):
        ind=i%256
        if(ind<192 and (ind%12)<4):#i is x linear index
            ind_base=i-ind%12
            flg=True

            for chk_var in map_L[ind%12]:
                if(res[ind_base+chk_var]==1):
                    res[i]=0
                    flg=False
                    break
            if(flg):
                res[i]=int(arr1[i]) ^ int(arr2[i])
    return res
def swapRow(MAT,r1,r2):
    tmp=MAT[r1]
    MAT[r1]=MAT[r2]
    MAT[r2]=tmp

def findPivotRow(MAT, curRow, curCol):
    for c in range(curCol,np.shape(MAT)[1]-128):
        for r in range(curRow,np.shape(MAT)[0]):
            ind=c%256
            if(MAT[r][c]==1):
                if(ind>=192 or (ind<192 and (ind%12)<4)): 
                    return r,c
    return -1,-1        

def GuassianElimination(MAT1):
    MAT,_=up_triangle(MAT1)
    curRow=0
    curCol=0
    while(True):
        pivotRow,pivotCol=findPivotRow(MAT,curRow,curCol)
        if(pivotRow==-1):
            break
        swapRow(MAT,curRow,pivotRow)
        for r in range(curRow+1,np.shape(MAT)[0]):
            if(MAT[r][pivotCol]==1):
                XOR(MAT,r,curRow)
        curRow+=1
        curCol=pivotCol+1
    return MAT
        
if __name__=="__main__":
    gmat=np.load(file_pth+"pmat.npy")
    gmat=GuassianElimination(gmat)
    show_L_equ_SKINNY(gmat)