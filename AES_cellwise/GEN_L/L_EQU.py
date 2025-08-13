import sympy as sp

# Define variables for AES input
x = sp.symbols('x0:16')

# ShiftRows permutation
sr_indices = [ 0,  1,  2,  3,
               5,  6,  7,  4,
              10, 11,  8,  9,
              15, 12, 13, 14]
x_sr = [x[i] for i in sr_indices]

# MixColumns matrix in GF(2^8) notation (symbolic)
def gf_mul(a, b):
    # GF(2^8) multiplication (simplified for symbolic ops)
    return sp.Symbol(f'{a}*{b}')

# Fixed MixColumns matrix
MC = [
    ['02', '03', '01', '01'],
    ['01', '02', '03', '01'],
    ['01', '01', '02', '03'],
    ['03', '01', '01', '02']
]

# Compute MixColumns on each column
y = [0]*16
for col in range(4):
    col_inputs = [x_sr[row*4 + col] for row in range(4)]
    for row in range(4):
        val = 0
        terms = []
        for k in range(4):
            terms.append(gf_mul(MC[row][k], col_inputs[k]))
        y[row*4 + col] = ' + '.join(terms)

# Display results
for i in range(16):
    print(f'y{i} = {y[i]}')
