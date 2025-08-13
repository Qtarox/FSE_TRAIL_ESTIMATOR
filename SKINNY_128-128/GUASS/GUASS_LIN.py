import config.config as config
import numpy as np
from VTools.Visual import show_L_equ_GIFT3, show_linear_mat
file_pth=config.file_path

def XOR(MAT,r1,r2):
    for j in range(np.shape(MAT)[1]):
        MAT[r1][j]^=MAT[r2][j]

def swapRow(MAT,r1,r2):
    tmp=MAT[r1]
    MAT[r1]=MAT[r2]
    MAT[r2]=tmp
# int findPivotRow(uint8_t **M, int currentRow, int currentCol, int &pivotCol, int ROWSIZE, int COLSIZE){
# 	for (int c = currentCol; c < COLSIZE; c++){
# 		for (int r = currentRow; r < ROWSIZE; r++){
# 			if (M[r][c] == 1){
# 				pivotCol = c;
# 				return r;
# 			}
# 		}
# 	}
# 	return -1; // return -1 when there is nothing else to find
# }

def findPivotRow(MAT, curRow, curCol):
    for c in range(curCol,np.shape(MAT)[1]-128):
        for r in range(curRow,np.shape(MAT)[0]):
            ind=c%256
            if(MAT[r][c]==1):
                if(ind>=192 or (ind<192 and (ind%12)<4)): 
                    return r,c
    return -1,-1        
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
def GuassianElimination(MAT):
    MAT,_=up_triangle(MAT)
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
    gmat=np.load(file_pth+"GIFT_GMAT.npy")
    gmat=GuassianElimination(gmat)
    show_L_equ_GIFT3(gmat)
