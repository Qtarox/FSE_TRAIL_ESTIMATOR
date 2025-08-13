import config.config as config
import numpy as np
from TOOLS.Visual import show_L_equ_SKINNY
file_pth=config.file_path

def XOR(MAT,r1,r2):
    for j in range(np.shape(MAT)[1]):
        MAT[r1][j]^=MAT[r2][j]

def swapRow(MAT,r1,r2):
    MAT[[r1, r2]] = MAT[[r2, r1]]

def up_triangle(MAT,N):
    for i in range(np.shape(MAT)[0]-1,-1,-1):
        ref(MAT,i,N)
        print(i)
def ref(MAT, cur_row,N):
    cur_ind=cur_row
    while(cur_ind<np.shape(MAT)[0]-1 and findPivot(MAT,cur_ind,N)>findPivot(MAT,cur_ind+1,N)):
        swapRow(MAT,cur_ind,cur_ind+1)
        cur_ind+=1
def findPivot1(MAT, curRow):
    for c in range(np.shape(MAT)[1]-128):       
        ind=c%256
        if(MAT[curRow][c]==1):
            if(ind>=192 or (ind<192 and (ind%12)<4)): 
                return c
    return -1 
def findPivot(MAT,curRow,N):
    for c in range(N):       
        if(MAT[curRow][c]==1):
            return c
    return 999999
# def up_triangle(mat):
#     list_ind=[[0,i] for i in range(np.shape(mat)[0])]
#     res=mat.copy()
#     for i in range(np.shape(mat)[0]):
#         for j in range(np.shape(mat)[1]):
#             if(mat[i][j]==1):
#                 list_ind[i][0]=j
#                 break
#     sorted_tuples = sorted(list_ind, key=lambda x: x[0])
#     for i in range(np.shape(mat)[0]):
#         res[i]=mat[sorted_tuples[i][1]]
#     return res
def Guass_Elimin(MAT,N=None):
    cur_row=1
    M=np.shape(MAT)[0]
    if(N):
        pass
    else:
        N=np.shape(MAT)[1]#-128
    up_triangle(MAT,N)
    # print(MAT)
    # show_L_equ_GIFT3(MAT)
    while(cur_row<M and findPivot(MAT,cur_row,N)<N):
        #check the cur_row
        while(findPivot(MAT,cur_row,N)<=findPivot(MAT,cur_row-1,N)):
            # print("stuck")
            XOR(MAT,cur_row,cur_row-1)
            ref(MAT,cur_row,N)
            # print(MAT)
        cur_row+=1

if __name__=="__main__":
    # MAT=[[1,0,0,0,1,1,0,0],
    #      [1,1,0,0,1,0,0,1],
    #      [0,1,1,1,0,1,1,0],
    #      [1,0,0,0,0,1,0,0],
    #      [0,0,1,1,0,0,0,1],
    #      [1,1,0,0,1,0,0,1]]
    # MAT=np.array(MAT)
    # Guass_Elimin(MAT,4)
    # print(MAT)
    
    # gmat=np.load(file_pth+"GIFT_LMAT.npy")
    gmat=np.load(file_pth+"pmat.npy")
    print(np.shape(gmat))
    # ok
    # show_L_equ_GIFT3(gmat)
    # ok
    Guass_Elimin(gmat,np.shape(gmat)[1]-16)
    show_L_equ_SKINNY(gmat)