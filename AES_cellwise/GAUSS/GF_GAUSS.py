import numpy as np
from GEN_L.GF28 import * 

# import numpy as np
# from collections import defaultdict

# def modified_gaussian_elimination(mat):
#     """
#     Performs Gaussian elimination on a binary matrix while respecting index constraints.
    
#     :param mat: numpy array of shape (n, m+1), where the last column is the index
#     :return: Reduced row echelon form of the matrix with index constraints
#     """
#     mat = np.array(mat, dtype=np.uint8)  # Ensure binary field
#     rows, cols = mat.shape
#     data_cols = cols - 1  # Exclude index column
    
#     # Step 1: Group rows by index
#     index_groups = defaultdict(list)
#     for row in mat:
#         index_groups[row[-1]].append(row[:-1])  # Exclude index column
    
#     # Step 2: Perform Gaussian elimination within each group
#     reduced_groups = {}
#     for idx, group in index_groups.items():
#         group_matrix = np.array(group, dtype=np.uint8)
#         reduced_groups[idx] = gaussian_elimination_gf2(group_matrix)
    
#     # Step 3: Merge results into final matrix
#     final_rows = []
#     for idx, reduced_matrix in reduced_groups.items():
#         for row in reduced_matrix:
#             if np.any(row):  # Ignore zero rows
#                 final_rows.append(np.append(row, idx))  # Add back index column

#     return np.array(final_rows, dtype=np.uint8)
def row_mul(mat,row,b):
    for j in range(np.shape(mat)[1]):
        if(mat[row][j]!=0):
            mat[row][j]=gf_mul(mat[row][j],b)
    return mat

def unify_row(mat, row):
    flg=False
    b=-1
    for j in range(np.shape(mat)[1]):
        if(mat[row][j]!=0 and flg==False):
            b=gf_inv(mat[row][j]) 
            break
    if(b==-1):
        return
    else:
        row_mul(mat,row,b)   

def gaussian_elimination_gf28(mat):
    """
    Standard Gaussian elimination over GF(2) without index constraints.
    
    :param mat: Binary matrix without index column
    :return: Row reduced matrix
    """
    mat = mat.copy()
    rows, cols = mat.shape
    row_idx = 0  # Current row being processed

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
        mat[[row_idx, pivot_row]] = mat[[pivot_row, row_idx]]

        # Eliminate below
        for r in range(row_idx + 1, rows):
            if mat[r, col] >=1:
                unify_row(mat,r)
                mat[r] ^= mat[row_idx]  # XOR elimination

        row_idx += 1  # Move to the next row

    return mat

# Example usage


# reduced_mat = modified_gaussian_elimination(mat)
# if __name__=="__main__":


