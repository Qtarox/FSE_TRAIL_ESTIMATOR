import numpy as np
from GEN_L.GF28 import * 
import config.config as config
np.set_printoptions(linewidth=400)
np.set_printoptions(threshold=np.inf)
round_num=config.round_num

def XOR(MAT,r1,r2):
    for j in range(np.shape(MAT)[1]):
        MAT[r1][j]^=MAT[r2][j]

def row_mul(mat,row,b):
    for j in range(np.shape(mat)[1]):
        if(mat[row][j]!=0):
            mat[row][j]=gf_mul(mat[row][j],b)
    return mat

def unify_row(mat, row):
    b=-1
    for j in range(np.shape(mat)[1]):
        if(mat[row][j]!=0 ):
            b=gf_inv(mat[row][j]) 
            print(mat[row][j])
            break
    if(b==-1):
        return
    else:
        row_mul(mat,row,b) 
        return b
def is_all_zero(mat,r):
    for j in range(np.shape(mat)[1]):
        if(mat[r][j]>0):
            return False
    return True
def check(mat, row_rec):
    res=[]
    for i in range(np.shape(mat)[0]):
        if(is_all_zero(mat,i)):
            res.append(i)
    CONS=[]
    COF=[]
    for i in res:
        tmp=[]
        coe=[]
        for j in range(np.shape(row_rec)[1]):
            if(row_rec[i][j]>=1 and j<16*(round_num)):
                tmp.append(j)
                coe.append(row_rec[i][j])
        if(len(tmp)>0):
            CONS.append(tmp.copy())
            COF.append(coe.copy())


    return CONS,COF

def gaussian_elimination_gf28(mat):
    """
    Standard Gaussian elimination over GF(2^8) without index constraints.
    
    :param mat: Binary matrix without index column
    :return: Row reduced matrix
    """
    mat = mat.copy()
    rows, cols = mat.shape
    row_idx = 0  # Current row being processed
    row_rec=np.zeros((rows,rows),dtype=int)
    for i in range(rows):
        row_rec[i][i]=1

    for col in range(cols):
        # Find pivot (first row with 1 in current column)
        pivot_row = None
        for r in range(row_idx, rows):
            if mat[r, col] !=0:
                pivot_row = r
                break
        
        if pivot_row is None:  # No pivot found, move to next column
            continue

        # Swap pivot row to the top
        b=unify_row(mat,pivot_row)
        row_mul(row_rec,pivot_row,b)
        # print(b)
        mat[[row_idx, pivot_row]] = mat[[pivot_row, row_idx]]
        row_rec[[row_idx, pivot_row]] = row_rec[[pivot_row, row_idx]]


        # Eliminate below
        for r in range(row_idx + 1, rows):
            if mat[r, col] >=1:
                b=unify_row(mat,r)
                mat[r] ^= mat[row_idx]  # XOR elimination
                row_mul(row_rec,r,b)
                row_rec[r]^=row_rec[row_idx]

        row_idx += 1  # Move to the next row
    res,cof=check(mat,row_rec)

    return res,cof


# Example usage


# reduced_mat = modified_gaussian_elimination(mat)
if __name__=="__main__":
    pass


