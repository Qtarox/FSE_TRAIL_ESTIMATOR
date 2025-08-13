include "table.mzn";

% Define 4-bit integer variables (0..15)
var 0..15: k_10;
var 0..15: k_12;
var 0..15: k_2;
var 0..15: k_9;
var 0..15: x_1_0;
var 0..15: x_1_12;
var 0..15: x_2_11;
var 0..15: x_2_4;
var 0..15: x_3_9;
var 0..15: x_4_11;
var 0..15: y_0_13;
var 0..15: y_1_0;
var 0..15: y_1_6;
var 0..15: y_1_9;
var 0..15: y_2_11;
var 0..15: y_2_4;
var 0..15: y_3_6;
var 0..15: y_3_9;

constraint bit_xor3(y_0_13, x_1_0, x_1_12);
constraint bit_xor3(y_1_0, x_2_4, k_9);
constraint bit_xor4(y_1_6, y_1_9, x_2_11, k_12);
constraint bit_xor4(y_2_4, y_2_11, x_3_9, k_2);
constraint bit_xor4(y_3_6, y_3_9, x_4_11, k_10);
constraint table([x_1_0, y_1_0], sbox_table);
constraint table([x_2_4, y_2_4], sbox_table);
constraint table([x_2_11, y_2_11], sbox_table);
constraint table([x_3_9, y_3_9], sbox_table);
constraint x_1_12 in { 5, 7, 13, 15 };
constraint x_4_11 in { 10, 11, 14, 15 };
constraint y_0_13 in { 5, 13, 7, 15 };
constraint y_1_6 in { 10, 11, 14, 15 };
constraint y_1_9 in { 10, 11, 14, 15 };
constraint y_3_6 in { 10, 11, 14, 15 };

array[0..15, 1..2] of int: sbox_table = 
    array2d(0..15, 1..2, [
        0, 12,  1, 6,  2, 9,  3, 0,
        4, 1,   5, 10, 6, 2,  7, 11,
        8, 3,   9, 8,  10, 5, 11, 13,
        12, 4,  13, 14, 14, 7, 15, 15
    ]);

% Predicate for bitwise XOR (n variables)
predicate bit_xor3(var 0..15: x0, var 0..15: x1, var 0..15: y) =
    let {
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits,
        array[0..3] of var bool: y_bits
    } in (
        int2bin(x0, x0_bits) /\
        int2bin(x1, x1_bits) /\
        int2bin(y, y_bits) /\
        forall(i in 0..3)(
            (x0_bits[i] + x1_bits[i]) mod 2 = y_bits[i]
        )
    );

predicate bit_xor4(var 0..15: x0, var 0..15: x1, var 0..15: x2, var 0..15: y) =
    let {
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits,
        array[0..3] of var bool: x2_bits,
        array[0..3] of var bool: y_bits
    } in (
        int2bin(x0, x0_bits) /\
        int2bin(x1, x1_bits) /\
        int2bin(x2, x2_bits) /\
        int2bin(y, y_bits) /\
        forall(i in 0..3)(
            (x0_bits[i] + x1_bits[i] + x2_bits[i]) mod 2 = y_bits[i]
        )
    );

predicate bit_xor5(var 0..15: x0, var 0..15: x1, var 0..15: x2, var 0..15: x3, var 0..15: y) =
    let {
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits,
        array[0..3] of var bool: x2_bits,
        array[0..3] of var bool: x3_bits,
        array[0..3] of var bool: y_bits
    } in (
        int2bin(x0, x0_bits) /\
        int2bin(x1, x1_bits) /\
        int2bin(x2, x2_bits) /\
        int2bin(x3, x3_bits) /\
        int2bin(y, y_bits) /\
        forall(i in 0..3)(
            (x0_bits[i] + x1_bits[i] + x2_bits[i] + x3_bits[i]) mod 2 = y_bits[i]
        )
    );

predicate int2bin(var 0..15: x, array[0..3] of var bool: bits) =
    (bits[0] = (x div 1) mod 2) /\
    (bits[1] = (x div 2) mod 2) /\
    (bits[2] = (x div 4) mod 2) /\
    (bits[3] = (x div 8) mod 2);
