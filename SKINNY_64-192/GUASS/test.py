import numpy as np
import config.config as config
fp=config.file_path
from VTools.Visual import show_L_equ_GIFT3

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
def gaussian_elimination_gf2(matrix):
    """
    Perform Gaussian elimination on a binary matrix over GF(2).
    Returns the row echelon form and indices of dependent rows.
    """
    mat = matrix.copy()  # Work on a copy of the matrix
    mat,_=up_triangle(mat)
    m, n = mat.shape
    pivot_rows = []
    dependent_rows = []

    row = 0
    for col in range(n):
        if row >= m:
            break
        
        # Find pivot (first row with a 1 in the current column)
        pivot = None
        for i in range(row, m):
            if mat[i, col] == 1 and col<n-128:
                pivot = i
                break
        
        if pivot is None:
            continue  # No pivot in this column, move to the next column
        
        # Swap the current row with the pivot row
        if pivot != row:
            mat[[row, pivot]] = mat[[pivot, row]]
        
        # Eliminate rows below the pivot
        for i in range(row + 1, m):
            if mat[i, col] == 1:
                mat[i] ^= mat[row]  # XOR to eliminate

        pivot_rows.append(row)
        row += 1
    
    # Identify dependent rows
    for i in range(m):
        if i not in pivot_rows:
            dependent_rows.append(i)
    
    return mat, dependent_rows

# Example matrix over GF(2)
if __name__=="__main__":
    gmat=np.load(fp+"GIFT_GMAT.npy")
    row_echelon, dependent_rows = gaussian_elimination_gf2(gmat)
    show_L_equ_GIFT3(row_echelon)




    if dependent_rows:
        print("\nLinearly Dependent Rows:")
        print(dependent_rows)
    else:
        print("\nNo Linearly Dependent Rows Found.")
