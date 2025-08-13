include "table.mzn";

    % Define 4-bit integer variables (0..15)
    var 0..15: k_16;
var 0..15: z_0_99;

    constraint bit_xor2(z_0_99, k_16);
constraint z_0_99 in { 9, 15 };

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


    
predicate bit_xor2(var 0..15: x0, var 0..15: x1) =
    let { 
        array[0..3] of var bool: x0_bits,
        array[0..3] of var bool: x1_bits
    } in (
        int2bin(x0, x0_bits) /\ 
        int2bin(x1, x1_bits) /\ 
        forall(i in 0..3)(
            ( x0_bits[i] + x1_bits[i]) mod 2 = 0
        )
    );
