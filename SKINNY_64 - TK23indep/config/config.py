from config.DCs import DC_DIC
DC_name="DC7"
DC=DC_DIC[DC_name]
Sbox=[ 12 , 6 , 9 , 0 , 1 , 10 , 2 , 11 , 3 , 8 , 5 , 13 , 4 , 14 , 7 , 15 ]
Sbox_inv=[ 3 , 4 , 6 , 8 , 12 , 10 , 1 , 14 , 9 , 2 , 5 , 7 , 0 , 11 , 13 , 15 ]
full_list=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
cons_mod=1  
round_num=len(DC)
file_path=".\\"+DC_name+"\\"