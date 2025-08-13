include "table.mzn";

    % Define 4-bit integer variables (0..15)
    var 0..15: k_54;
var 0..15: k_75;
var 0..15: k_77;
var 0..15: k_81;
var 0..15: k_90;
var 0..15: k_91;
var 0..15: x_10_2;
var 0..15: x_9_10;
var 0..15: y_10_2;
var 0..15: y_9_10;
var 0..15: z_0_99;
var 0..15: z_1_99;
var 0..15: z_2_99;

    constraint bit_xor5(z_0_99, y_9_10, x_10_2, k_54, k_81);
constraint bit_xor4(z_1_99, y_10_2, k_75, k_90);
constraint bit_xor4(z_2_99, x_9_10, k_77, k_91);
constraint table([x_9_10, y_9_10], sbox_table);
constraint table([x_10_2, y_10_2], sbox_table);
array[1..8] of int: possible_values0 = [ 0, 1, 6, 7, 8, 9, 14, 15 ]; 
 var 1..8: i0;
 constraint z_0_99 = possible_values0[i0];
array[1..4] of int: possible_values1 = [ 0, 5, 8, 13 ]; 
 var 1..4: i1;
 constraint z_1_99 = possible_values1[i1];
array[1..8] of int: possible_values2 = [ 1, 2, 5, 6, 8, 11, 12, 15 ]; 
 var 1..8: i2;
 constraint z_2_99 = possible_values2[i2];

    array[0..15, 1..2] of int: sbox_table = 
        array2d(0..15, 1..2, [
        0, 12,  1, 0,  2,15, 3 ,10,
        4,2,  5,11, 6,9, 7,5, 
        8,8, 9,3, 10,13, 11,7, 
        12,1, 13,14, 14,6, 15,4

        ]);

    % Predicate for bitwise XOR (n variables)
    predicate int2bin(var 0..15: x, array[0..3] of var bool: bits) =
        (bits[0] = (x div 1) mod 2) /\
        (bits[1] = (x div 2) mod 2) /\
        (bits[2] = (x div 4) mod 2) /\
        (bits[3] = (x div 8) mod 2);


    
predicate bit_xor5(var 0..15: x0, var 0..15: x1, var 0..15: x2, var 0..15: x3, var 0..15: x4) =
    let { 
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits,
        array[0..3] of var bool: x2_bits,
        array[0..3] of var bool: x3_bits,
        array[0..3] of var bool: x4_bits
    } in (
        int2bin(x0, x0_bits) /\ 
        int2bin(x1, x1_bits) /\ 
        int2bin(x2, x2_bits) /\ 
        int2bin(x3, x3_bits) /\ 
        int2bin(x4, x4_bits) /\ 
        forall(i in 0..3)(
            ( x0_bits[i] + x1_bits[i] + x2_bits[i] + x3_bits[i] + x4_bits[i]) mod 2 = 0
        )
    );

predicate bit_xor4(var 0..15: x0, var 0..15: x1, var 0..15: x2, var 0..15: x3) =
    let { 
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits,
        array[0..3] of var bool: x2_bits,
        array[0..3] of var bool: x3_bits
    } in (
        int2bin(x0, x0_bits) /\ 
        int2bin(x1, x1_bits) /\ 
        int2bin(x2, x2_bits) /\ 
        int2bin(x3, x3_bits) /\ 
        forall(i in 0..3)(
            ( x0_bits[i] + x1_bits[i] + x2_bits[i] + x3_bits[i]) mod 2 = 0
        )
    );
