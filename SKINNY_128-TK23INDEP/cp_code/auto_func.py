import re
def gen_func_n(n):
    func_str="\n"
    para="predicate bit_xor"+str(n)+"("
    tmp_para=""
    for i in range(n):
        if(i<n-1):
            tmp_para+="var 0..15: x"+str(i)+", "
        else:
            tmp_para+="var 0..15: x"+str(i)+") =\n"
    func_str+=para
    func_str+=tmp_para
    func_str+="    let { \n"
    for i in range(n-1):
        func_str+="        array[0..3] of var bool: x"+str(i)+"_bits,\n"
    func_str+="        array[0..3] of var bool: x"+str(n-1)+"_bits\n"
    func_str+='    } in (\n'
    for i in range(n):
        func_str+="        int2bin(x"+str(i)+", x"+str(i)+"_bits) /\\ \n"
    func_str+="        forall(i in 0..3)(\n"
    func_str+="            ("
    for i in range(n-1):
        func_str+=" x"+str(i)+"_bits[i] +"
    func_str+=" x"+str(n-1)+"_bits[i]) mod 2 = 0\n"
    func_str+="        )\n"
    func_str+="    );\n"
    return func_str


"""
  
predicate bit_xor3(var 0..15: x0, var 0..15: x1, var 0..15: y) =
    let {
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits,
        array[0..3] of var bool: y_bits
    } in (
        int2bin(x0, x0_bits) /\\
        int2bin(x1, x1_bits) /\\
        int2bin(y, y_bits) /\\
        forall(i in 0..3)(
            (x0_bits[i] + x1_bits[i]) mod 2 = y_bits[i]
        )
    );
"""  
if __name__=="__main__":
    gen_func_n(5)