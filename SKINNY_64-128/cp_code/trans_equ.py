import re
from auto_func import *

act_x = {"x_0_2": [10, 11, 14, 15], "x_0_4": [10, 11, 14, 15], "x_0_5": [10, 11, 14, 15], "x_0_6": [10, 11, 14, 15], "x_0_7": [10, 11, 14, 15], "x_0_8": [10, 11, 14, 15], "x_0_9": [10, 11, 14, 15], "x_0_10": [10, 11, 14, 15], "x_0_12": [10, 11, 14, 15], "x_0_13": [10, 11, 14, 15], "x_1_6": [5, 7, 13, 15], "x_1_9": [5, 7, 13, 15], "x_1_12": [5, 7, 13, 15], "x_1_15": [5, 7, 13, 15], "x_2_2": [10, 11, 14, 15], "x_2_15": [10, 11, 14, 15], "x_3_6": [5, 7, 13, 15], "x_3_14": [5, 7, 13, 15], "x_4_1": [10, 11, 14, 15], "x_4_11": [10, 11, 14, 15], "x_5_5": [5, 7, 13, 15], "x_5_9": [5, 7, 13, 15], "x_6_3": [10, 11, 14, 15], "x_6_10": [10, 11, 14, 15], "x_6_11": [10, 11, 14, 15], "x_6_15": [10, 11, 14, 15], "y_0_2": [5, 13, 7, 15], "y_0_4": [5, 13, 7, 15], "y_0_5": [5, 13, 7, 15], "y_0_6": [5, 13, 7, 15], "y_0_7": [5, 13, 7, 15], "y_0_8": [5, 13, 7, 15], "y_0_9": [5, 13, 7, 15], "y_0_10": [5, 13, 7, 15], "y_0_12": [5, 13, 7, 15], "y_0_13": [5, 13, 7, 15], "y_1_6": [10, 11, 14, 15], "y_1_9": [10, 11, 14, 15], "y_1_12": [10, 11, 14, 15], "y_1_15": [10, 11, 14, 15], "y_2_2": [5, 13, 7, 15], "y_2_15": [5, 13, 7, 15], "y_3_6": [10, 11, 14, 15], "y_3_14": [10, 11, 14, 15], "y_4_1": [5, 13, 7, 15], "y_4_11": [5, 13, 7, 15], "y_5_5": [10, 11, 14, 15], "y_5_9": [10, 11, 14, 15], "y_6_3": [5, 13, 7, 15], "y_6_10": [5, 13, 7, 15], "y_6_11": [5, 13, 7, 15], "y_6_15": [5, 13, 7, 15]}

# input_text = """
# + [ y_0_4 ] + [ y_0_11 ] + x_1_9 + k_4= 0 
#  + [ y_1_3 ] + y_1_9 + [ x_2_15 ] + k_13= 0 
#  + x_1_9 + y_1_9= 0 
#  + [ y_1_3 ] + y_1_9 + [ y_1_12 ] + [ x_2_3 ] + k_13= 0 
# """

# input_text = """
#  + y_0_1 + x_1_5 + k_1= 0 
#  + y_0_1 + [ y_0_11 ] + [ x_1_13 ] + k_1= 0
#  + y_1_5 + [ y_1_8 ] + [ x_2_10 ] + k_14= 0
#  + x_1_5 + y_1_5= 0
#  """


input_text = """
 + y_0_0 + x_1_4 + k_0= 0
 + y_0_0 + [ y_0_10 ] + [ x_1_12 ] + k_0= 0
 + y_0_1 + x_1_5 + k_1= 0
 + y_0_1 + y_0_11 + x_1_13 + k_1= 0
 + [ y_0_2 ] + [ y_0_8 ] + x_1_14 + k_2= 0
 + y_0_3 + x_1_7 + k_3= 0
 + y_0_3 + [ y_0_9 ] + [ x_1_15 ] + k_3= 0
 + [ y_0_4 ] + y_0_11 + [ x_1_9 ] + k_4= 0
 + [ y_0_6 ] + [ y_0_9 ] + x_1_11 + k_6= 0
 + y_1_0 + y_1_10 + y_1_13 + x_2_0 + k_9= 0
 + y_1_0 + x_2_4 + k_9= 0
 + y_1_1 + y_1_11 + y_1_14 + x_2_1 + k_15= 0
 + y_1_1 + y_1_11 + x_2_13 + k_15= 0
 + y_1_2 + x_2_6 + k_8= 0
 + y_1_2 + y_1_8 + x_2_14 + k_8= 0
 + y_1_4 + y_1_11 + x_2_9 + k_10= 0
 + y_1_5 + y_1_8 + x_2_10 + k_14= 0
 + y_1_7 + y_1_10 + x_2_8 + k_11= 0
 + y_2_0 + y_2_10 + y_2_13 + x_3_0 + k_1= 0
 + y_2_1 + y_2_11 + y_2_14 + x_3_1 + k_7= 0
 + [ y_2_2 ] + y_2_8 + [ x_3_14 ] + k_0= 0
 + y_2_4 + y_2_11 + x_3_9 + k_2= 0
 + y_2_6 + y_2_9 + x_3_11 + k_4= 0
 + y_3_0 + x_4_4 + k_15= 0
 + y_3_1 + y_3_11 + [ y_3_14 ] + [ x_4_1 ] + k_11= 0
 + [ y_3_6 ] + y_3_9 + [ x_4_11 ] + k_10= 0
 + y_4_4 + [ y_4_11 ] + [ x_5_9 ] + k_0= 0
 + x_1_4 + y_1_4= 0
 + x_1_5 + y_1_5= 0
 + x_1_7 + y_1_7= 0
 + x_1_11 + y_1_11= 0
 + x_1_13 + y_1_13= 0
 + x_1_14 + y_1_14= 0
 + x_2_0 + y_2_0= 0
 + x_2_1 + y_2_1= 0
 + x_2_4 + y_2_4= 0
 + x_2_6 + y_2_6= 0
 + x_2_8 + y_2_8= 0
 + x_2_9 + y_2_9= 0
 + x_2_10 + y_2_10= 0
 + x_2_13 + y_2_13= 0
 + x_2_14 + y_2_14= 0
 + x_3_0 + y_3_0= 0
 + x_3_1 + y_3_1= 0
 + x_3_9 + y_3_9= 0
 + x_3_11 + y_3_11= 0
 + x_4_4 + y_4_4= 0
 """


input_text = """
+ y_0_0 + [ y_0_10 ] + [ y_0_13 ] + x_1_0 + k_0= 0
 + y_0_0 + [ y_0_10 ] + [ x_1_12 ] + k_0= 0
 + y_1_0 + x_2_4 + k_9= 0
 + [ y_1_6 ] + [ y_1_9 ] + x_2_11 + k_12= 0
 + y_2_4 + y_2_11 + x_3_9 + k_2= 0
 + [ y_3_6 ] + y_3_9 + [ x_4_11 ] + k_10= 0
 + x_1_0 + y_1_0= 0
 + x_2_4 + y_2_4= 0
 + x_2_11 + y_2_11= 0
 + x_3_9 + y_3_9= 0 
 """


input_text = """
[ y_0_13 ] + x_1_0 + [x_1_12 ] = 0
 + y_1_0 + x_2_4 + k_9= 0
 + [ y_1_6 ] + [ y_1_9 ] + x_2_11 + k_12= 0
 + y_2_4 + y_2_11 + x_3_9 + k_2= 0
 + [ y_3_6 ] + y_3_9 + [ x_4_11 ] + k_10= 0
 + x_1_0 + y_1_0= 0
 + x_2_4 + y_2_4= 0
 + x_2_11 + y_2_11= 0
 + x_3_9 + y_3_9= 0
"""

input_text1="""
 + [ y_0_5 ] + [ y_0_8 ] + [ y_0_9 ] + x_1_7 + x_1_10 + [ x_1_15 ] + k_5= 0 
 + y_1_7 + y_1_10 + x_2_8 + k_11= 0
 + [ y_2_2 ] + y_2_8 + [ x_3_14 ] + k_0= 0
"""
def trans_equ(input_text,file_name,variable_constraints):
    variables = set(re.findall(r'[a-z]_\d+_\d+|k_\d+', input_text))

    variable_declarations = "\n".join(f"var 0..15: {var};" for var in sorted(variables))


    xor_constraints = []
    sbox_constraints = []
    range_constraints = []
    type_lst=[]
    for line in input_text.strip().split("\n"):
        line = re.sub(r'[\[\]]', '', line) 
        line = line.replace("= 0", "").strip()
        
    
        match = re.match(r'\+?\s*(x_\d+_\d+)\s*\+\s*(y_\d+_\d+)', line)
        
        if match:
            x_var, y_var = match.groups()
            sbox_constraints.append(f"constraint table([{x_var}, {y_var}], sbox_table);")
        else:
            vars_in_eq = re.findall(r'[a-z]_\d+_\d+|k_\d+', line)
            if len(vars_in_eq) > 1:
                constraint_type = f"bit_xor{len(vars_in_eq)}"
                xor_constraints.append(f"constraint {constraint_type}({', '.join(vars_in_eq)});")
                type_lst.append(constraint_type)
    for var in sorted(variables):
        if var in variable_constraints:
            values = ", ".join(map(str, variable_constraints[var])) 
            range_constraints.append(f"constraint {var} in {{ {values} }};")



    constraint_definitions = "\n".join(xor_constraints + sbox_constraints + range_constraints)


    minizinc_code = f"""include "table.mzn";

    % Define 4-bit integer variables (0..15)
    {variable_declarations}

    {constraint_definitions}

    array[0..15, 1..2] of int: sbox_table = 
        array2d(0..15, 1..2, [
            0, 12,  1, 6,  2, 9,  3, 0,
            4, 1,   5, 10, 6, 2,  7, 11,
            8, 3,   9, 8,  10, 5, 11, 13,
            12, 4,  13, 14, 14, 7, 15, 15
        ]);

    % Predicate for bitwise XOR (n variables)
    predicate int2bin(var 0..15: x, array[0..3] of var bool: bits) =
        (bits[0] = (x div 1) mod 2) /\\
        (bits[1] = (x div 2) mod 2) /\\
        (bits[2] = (x div 4) mod 2) /\\
        (bits[3] = (x div 8) mod 2);


    """
    ind_lst=[]
    for i in type_lst:
        num=int(i[7:])
        if(num not in ind_lst):
            ind_lst.append(num)
    print(ind_lst)
    for i in ind_lst:
        minizinc_code+= gen_func_n(i)

    print(minizinc_code)
    with open(file_name, "w") as fw:
        fw.write(minizinc_code)

if __name__=="__main__":
    trans_equ(input_text1,"con_solve3.mzn",act_x)