def binary_array_to_hex(binary_array):
    grouped_bits = [binary_array[i:i+4] for i in range(0, len(binary_array), 4)]
    hex_string = ''.join(hex(int(''.join(map(str, group)), 2))[2:].upper() for group in grouped_bits)
    return hex_string


r = 9
filename = f"optimal_solution_of_Model_twine64_{r}_round_searchForBestDifferentialCharacteristic_BranchBound_model.lp.txt"
# filename = f"optimal_solution_of_Model_twine64_{r}_round_calculateMinNumOfDifferentiallyActiveSbox_BranchBound_model.lp.txt"
for i in range(r):
    print(f"the {i}-th round")
    variables_x_left = ['x'+str(i) for i in range(64*i, 32+64*i)]
    value_x_left = []
    variables_x_right = ['x'+str(i) for i in range(32+64*i, 64+64*i)]
    value_x_right = []
    variables_sbox_in = ['sboxIn'+str(i) for i in range(32*i, 32+32*i)]
    value_sbox_in = []
    variables_sbox_out = ['sboxOut'+str(i) for i in range(32*i, 32+32*i)]
    value_sbox_out = []
    variables = {}
    with open(filename, 'r') as file:
        for line in file:
            if ' = ' in line:
                var, value = line.strip().split(' = ')
                if var in variables_x_left:
                    variables[var] = int(value)  
                if var in variables_x_right:
                    variables[var] = int(value)
                if var in variables_sbox_in:
                    variables[var] = int(value)  
                if var in variables_sbox_out:
                    variables[var] = int(value)  
    for i in range(len(variables_x_left)):
        # print(variables_x_left[i], variables[variables_x_left[i]])
        value_x_left.append(variables[variables_x_left[i]])
    for i in range(len(variables_x_right)):
        # print(variables_x_right[i], variables[variables_x_right[i]])
        value_x_right.append(variables[variables_x_right[i]])
    for i in range(len(variables_sbox_in)):
        # print(variables_sbox_in[i], variables[variables_sbox_in[i]])
        value_sbox_in.append(variables[variables_sbox_in[i]])
    for i in range(len(variables_sbox_out)):
        # print(variables_sbox_out[i], variables[variables_sbox_out[i]])
        value_sbox_out.append(variables[variables_sbox_out[i]])
    print("left: ", binary_array_to_hex(value_x_left))
    # print("binary:", value_x_left)
    print("right: ", binary_array_to_hex(value_x_right))
    # print("binary:", value_x_right)
    print("sbox_in: ", binary_array_to_hex(value_sbox_in))
    # print("binary:", value_sbox_in)
    print("sbox_out: ", binary_array_to_hex(value_sbox_out))
    # print("binary:", value_sbox_out)
    