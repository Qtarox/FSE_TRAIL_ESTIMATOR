include "table.mzn";

    % Define 4-bit integer variables (0..15)
    var 0..15: k_0;
var 0..15: k_11;
var 0..15: k_5;
var 0..15: x_1_10;
var 0..15: x_1_15;
var 0..15: x_1_7;
var 0..15: x_2_8;
var 0..15: x_3_14;
var 0..15: y_0_5;
var 0..15: y_0_8;
var 0..15: y_0_9;
var 0..15: y_1_10;
var 0..15: y_1_7;
var 0..15: y_2_2;
var 0..15: y_2_8;

    constraint bit_xor7(y_0_5, y_0_8, y_0_9, x_1_7, x_1_10, x_1_15, k_5);
constraint bit_xor4(y_1_7, y_1_10, x_2_8, k_11);
constraint bit_xor4(y_2_2, y_2_8, x_3_14, k_0);
constraint x_1_15 in { 5, 7, 13, 15 };
constraint x_3_14 in { 5, 7, 13, 15 };
constraint y_0_5 in { 5, 13, 7, 15 };
constraint y_0_8 in { 5, 13, 7, 15 };
constraint y_0_9 in { 5, 13, 7, 15 };
constraint y_2_2 in { 5, 13, 7, 15 };

    array[0..15, 1..2] of int: sbox_table = 
        array2d(0..15, 1..2, [
            0, 12,  1, 6,  2, 9,  3, 0,
            4, 1,   5, 10, 6, 2,  7, 11,
            8, 3,   9, 8,  10, 5, 11, 13,
            12, 4,  13, 14, 14, 7, 15, 15
        ]);

    % Predicate for bitwise XOR (n variables)
    predicate int2bin(var 0..15: x, array[0..3] of var bool: bits) =
        (bits[0] = (x div 1) mod 2) /\
        (bits[1] = (x div 2) mod 2) /\
        (bits[2] = (x div 4) mod 2) /\
        (bits[3] = (x div 8) mod 2);


    
predicate bit_xor7(var 0..15: x0, var 0..15: x1, var 0..15: x2, var 0..15: x3, var 0..15: x4, var 0..15: x5, var 0..15: x6) =
    let { 
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits,
        array[0..3] of var bool: x2_bits,
        array[0..3] of var bool: x3_bits,
        array[0..3] of var bool: x4_bits,
        array[0..3] of var bool: x5_bits,
        array[0..3] of var bool: x6_bits
    } in (
        int2bin(x0, x0_bits) /\ 
        int2bin(x1, x1_bits) /\ 
        int2bin(x2, x2_bits) /\ 
        int2bin(x3, x3_bits) /\ 
        int2bin(x4, x4_bits) /\ 
        int2bin(x5, x5_bits) /\ 
        int2bin(x6, x6_bits) /\ 
        forall(i in 0..3)(
            ( x0_bits[i] + x1_bits[i] + x2_bits[i] + x3_bits[i] + x4_bits[i] + x5_bits[i] + x6_bits[i]) mod 2 = 0
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
