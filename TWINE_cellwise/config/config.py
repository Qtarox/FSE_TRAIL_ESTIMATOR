import config.DCs as DCs
Sbox=[12, 0 ,15 ,10, 2 ,11, 9, 5, 8, 3, 13, 7, 1, 14 ,6, 4]
Sbox_inv=[1,12,4,9,15,7,14,11,8,6,3,5,0,10,13,2]
DC_name="DC15"
full_list=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
DC=DCs.DC_lst[DC_name]
round_num=len(DC)
file_path=".\\"+DC_name+"\\"