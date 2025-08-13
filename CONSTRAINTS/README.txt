These are the complete linear and nonlinear constraints detected by our tool. 
Notation:
1. x^r_i (y^r_i) refers to input (output) of the i-th Sbox/nonlinear bijection in round r.
2. k^r_j refers to the j-th subkey in round r
3. S( ) refers to S-box in SKINNY, LBLOCK and TWINE
4. '+' operator represents the XOR summation
5. for skinny cipher with TK schedule, k1_i means the i-th TK1, 
k2_i_n means the i-th cell TK2 after n times application of LFSR function, 
k3_i_n means the i-th cell TK3 after n times application of LFSR function;
And we have k2_i_n=L^n(k2_i_0), k3_i_n=L^n(k3_i_0),  where L stands for LFSR function

6. For other trails tested in the paper, constraints are either listed in appendix or either same as prior works
