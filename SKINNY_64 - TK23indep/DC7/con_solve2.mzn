include "table.mzn";

    % Define 4-bit integer variables (0..15)
    var 0..15: k_28;
var 0..15: k_35;
var 0..15: x_4_9;
var 0..15: y_4_9;
var 0..15: z_0_99;
var 0..15: z_1_99;

    constraint bit_xor3(z_0_99, x_4_9, k_28);
constraint bit_xor3(z_1_99, y_4_9, k_35);
constraint table([x_4_9, y_4_9], sbox_table);
constraint z_0_99 in { 0, 8 };
constraint z_1_99 in { 2, 3, 6, 7 };

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


    
predicate bit_xor3(var 0..15: x0, var 0..15: x1, var 0..15: x2) =
    let { 
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits,
        array[0..3] of var bool: x2_bits
    } in (
        int2bin(x0, x0_bits) /\ 
        int2bin(x1, x1_bits) /\ 
        int2bin(x2, x2_bits) /\ 
        forall(i in 0..3)(
            ( x0_bits[i] + x1_bits[i] + x2_bits[i]) mod 2 = 0
        )
    );
