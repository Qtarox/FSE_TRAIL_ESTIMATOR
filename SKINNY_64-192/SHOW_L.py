"""    array[0..15, 1..2] of int: sbox_table = 
        array2d(0..15, 1..2, [
            0, 12,  1, 6,  2, 9,  3, 0,
            4, 1,   5, 10, 6, 2,  7, 11,
            8, 3,   9, 8,  10, 5, 11, 13,
            12, 4,  13, 14, 14, 7, 15, 15
        ]);"""

import config.config as config
L=config.F
str1=""
for i in range(15):
    str1+="    array[0..15, 1..2] of int: fbox_table"+str(i)+" =\n"
    str1+="       array2d(0..15, 1..2, [ \n     "
    for j in range(15):
        str1+=str(j)+", "+str(L[i][j])+" ,"
    str1+=str(15)+", "+str(L[i][15])+" \n"
    str1+=" ]);\n"

print(str1)