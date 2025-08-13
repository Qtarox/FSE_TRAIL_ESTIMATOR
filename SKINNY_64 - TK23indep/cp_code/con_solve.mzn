include "table.mzn";

% Define 4-bit integer variables (0..15)
var 0..15: y_0_1;
var 0..15: x_1_5;
var 0..15: k_1;
var 0..15: y_0_11;
var 0..15: x_1_13;
var 0..15: y_1_5;
var 0..15: y_1_8;
var 0..15: x_2_10;
var 0..15: k_14;

% XOR constraints
constraint bit_xor3(y_0_1, x_1_5, k_1);
constraint bit_xor4(y_0_1, y_0_11, x_1_13, k_1);
constraint bit_xor4(y_1_5, y_1_8, x_2_10, k_14);

% S-box lookup table
array[0..15, 1..2] of int: sbox_table = 
    array2d(0..15, 1..2, [
        0, 12,  1, 6,  2, 9,  3, 0,
        4, 1,   5, 10, 6, 2,  7, 11,
        8, 3,   9, 8,  10, 5, 11, 13,
        12, 4,  13, 14, 14, 7, 15, 15
    ]);

% Enforce S-box constraints
constraint table([x_1_5, y_1_5], sbox_table);

% Domain constraints for specific variables
constraint y_0_11 in {1, 9};
constraint x_1_13 in {4, 6, 12, 14};
constraint y_1_8 in {5, 10};
constraint x_2_10 in {4, 11};

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


% Predicate for bitwise XOR (4 variables)
predicate bit_xor4(var 0..15: x0, var 0..15: x1, var 0..15: x2, var 0..15: y) =
    let {
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits,
        array[0..3] of var bool: x2_bits,
        array[0..3] of var bool: y_bits,
        array[0..3] of var bool: temp_bits
    } in (
        int2bin(x0, x0_bits) /\
        int2bin(x1, x1_bits) /\
        int2bin(x2, x2_bits) /\
        int2bin(y, y_bits) /\
        
        forall(i in 0..3)(
            (x0_bits[i] + x1_bits[i] + x2_bits[i]) mod 2 = y_bits[i]
        )
    );


predicate int2bin(var 0..15: x, array[0..3] of var bool: bits) =
    (bits[0] = (x div 1) mod 2) /\
    (bits[1] = (x div 2) mod 2) /\
    (bits[2] = (x div 4) mod 2) /\
    (bits[3] = (x div 8) mod 2);

