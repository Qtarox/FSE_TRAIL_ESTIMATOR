import re
from CP_SOLVER.auto_func import *
from CP_SOLVER.con_solve import cons_cp_solve
from cons0 import *
act_x = {'x_0_99': {8, 0, 10, 2},'x_1_99': {0, 1, 4, 5},'x_3_99': {0, 1, 4, 5},
         "x_0_2": [10, 11, 14, 15], "x_0_4": [10, 11, 14, 15], "x_0_5": [10, 11, 14, 15], "x_0_6": [10, 11, 14, 15], "x_0_7": [10, 11, 14, 15], "x_0_8": [10, 11, 14, 15], "x_0_9": [10, 11, 14, 15], "x_0_10": [10, 11, 14, 15], "x_0_12": [10, 11, 14, 15], "x_0_13": [10, 11, 14, 15], "x_1_6": [5, 7, 13, 15], "x_1_9": [5, 7, 13, 15], "x_1_12": [5, 7, 13, 15], "x_1_15": [5, 7, 13, 15], "x_2_2": [10, 11, 14, 15], "x_2_15": [10, 11, 14, 15], "x_3_6": [5, 7, 13, 15], "x_3_14": [5, 7, 13, 15], "x_4_1": [10, 11, 14, 15], "x_4_11": [10, 11, 14, 15], "x_5_5": [5, 7, 13, 15], "x_5_9": [5, 7, 13, 15], "x_6_3": [10, 11, 14, 15], "x_6_10": [10, 11, 14, 15], "x_6_11": [10, 11, 14, 15], "x_6_15": [10, 11, 14, 15], "y_0_2": [5, 13, 7, 15], "y_0_4": [5, 13, 7, 15], "y_0_5": [5, 13, 7, 15], "y_0_6": [5, 13, 7, 15], "y_0_7": [5, 13, 7, 15], "y_0_8": [5, 13, 7, 15], "y_0_9": [5, 13, 7, 15], "y_0_10": [5, 13, 7, 15], "y_0_12": [5, 13, 7, 15], "y_0_13": [5, 13, 7, 15], "y_1_6": [10, 11, 14, 15], "y_1_9": [10, 11, 14, 15], "y_1_12": [10, 11, 14, 15], "y_1_15": [10, 11, 14, 15], "y_2_2": [5, 13, 7, 15], "y_2_15": [5, 13, 7, 15], "y_3_6": [10, 11, 14, 15], "y_3_14": [10, 11, 14, 15], "y_4_1": [5, 13, 7, 15], "y_4_11": [5, 13, 7, 15], "y_5_5": [10, 11, 14, 15], "y_5_9": [10, 11, 14, 15], "y_6_3": [5, 13, 7, 15], "y_6_10": [5, 13, 7, 15], "y_6_11": [5, 13, 7, 15], "y_6_15": [5, 13, 7, 15]}



# Z={'x_0_99': {0, 8, 2, 10}, 'x_2_99': {8, 0, 10, 2}}
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
            
        # match = re.match(r'\+?\s*(x_\d+_\d+)\s*\+\s*(y_\d+_\d+)', line)
        match = re.match(r'\+?\s*(x_(\d+)_(\d+))\s*\+\s*(y_\2_\3)', line)
        # print(match)
        
        if match:
            x_var, y_var = match.group(1, 4)
            sbox_constraints.append(f"constraint table([{x_var}, {y_var}], sbox_table);")
        else:
            vars_in_eq = re.findall(r'[a-z]_\d+_\d+|k_\d+', line)
            if len(vars_in_eq) > 1:
                constraint_type = f"bit_xor{len(vars_in_eq)}"
                xor_constraints.append(f"constraint {constraint_type}({', '.join(vars_in_eq)});")
                type_lst.append(constraint_type)
    cnt=0
    for var in sorted(variables):
        if var in variable_constraints:
            values = ", ".join(map(str, variable_constraints[var])) 
            range_constraints.append(f"array[1..{ len(variable_constraints[var]) }] of int: possible_values{cnt} = [ {values} ]; \n var 1..{ len(variable_constraints[var]) }: i{cnt};\n constraint {var} = possible_values{cnt}[i{cnt}];")
            # range_constraints.append(f"set of int: possible_values{cnt} = {{ {values} }};\n var possible_values{cnt} : {var};")
            cnt+=1
    # range_constraints.append("constraint k_2 in { 8, 0, 10, 2 };")
    # range_constraints.append("constraint k_0 in { 8, 0, 10, 2 };")
    # range_constraints.append("constraint k_3 in { 8, 0, 10, 2 };")



    constraint_definitions = "\n".join(xor_constraints + sbox_constraints + range_constraints)


    minizinc_code = f"""include "table.mzn";

    % Define 4-bit integer variables (0..15)
    {variable_declarations}

    {constraint_definitions}

    array[0..15, 1..2] of int: sbox_table = 
        array2d(0..15, 1..2, [
        0, 12,  1, 0,  2,15, 3 ,10,
        4,2,  5,11, 6,9, 7,5, 
        8,8, 9,3, 10,13, 11,7, 
        12,1, 13,14, 14,6, 15,4

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
    fw.close()
def SOLVE_CP(cons_t,z,base_ind,f_pth):
    
    cons_name=f_pth+"./con_solve"+str(base_ind)+".mzn"
    solu_txt=f_pth+"./solve_results"+str(base_ind)+".txt"
    trans_equ(cons_t,cons_name,z)
    print(cons_cp_solve(solu_txt,cons_name))

if __name__=="__main__":
    cons_t=CONS3
    z=Z3
    cons_name="con_solve3.mzn"
    solu_txt="solve_results1.txt"
    
    trans_equ(cons_t,cons_name,z)
    print(cons_cp_solve(solu_txt,cons_name))