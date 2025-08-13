include "table.mzn";

    % Define 4-bit integer variables (0..15)
    var 0..15: z_0_99;

    array[1..8] of int: possible_values0 = [ 2, 3, 6, 7, 10, 11, 14, 15 ]; 
 var 1..8: i0;
 constraint z_0_99 = possible_values0[i0];

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


    