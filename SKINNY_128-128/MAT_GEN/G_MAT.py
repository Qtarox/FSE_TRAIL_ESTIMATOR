import numpy as np
M_EQ=np.load("MAT_GEN\M_EQ.npy")
import config.config as config
np.set_printoptions(linewidth=400)
round_num=config.round_num
file_path=config.file_path
# size should be (16 round_num) * (32* (round_num+1))
def Global_mat(res,M_EQ,round_num):
    for i in range(np.shape(res)[0]):
        equ_num=i%16
        rn=i//16 #the equ_num th equation in rn round
        for k in range(40):
            if(M_EQ[equ_num][k]==1):
                if(k<16):#x_r+1_k
                    res[i][(rn+1)*32+k]=1
                elif(k<32):#y_r_k
                    res[i][rn*32+k]=1
                else:# is key index
                    rn_k_ind=k-32
                    break
        k_ind=key_schedule(rn,rn_k_ind)
        res[i][(32)*(round_num+1)+k_ind]=1
    return res


# def gener_GEQU(mat,key_ind):
    
#     row_num=np.shape(mat)[0]
#     print(row_num)
#     res=np.zeros((row_num,round_num*32+16))
#     for i in range(row_num):
#         res[i][0:32*round_num]=mat[i][0:32*round_num]
#         res[i][32*round_num+key_ind]=1
#     return res
def key_schedule(round=0,key_index=0):
    key_permu=[9 , 15 , 8 , 13 , 10 , 14 , 12 , 11 , 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7]
    tmp=key_index
    for i in range(round):
        tmp=key_permu[tmp]
    return tmp    
def creat_NLmat():
    res=np.zeros((16*round_num,(round_num+1)*32+16),dtype=int)
    for i in range(np.shape(res)[0]):
        rn=i//16
        x_ind=i%16
        res[i][rn*32+x_ind]=1
        res[i][rn*32+x_ind+16]=1

    return res
def assemble_2blk(blk1,blk2):
    len1=np.shape(blk1)[0]
    len2=np.shape(blk2)[0]
    res=np.zeros((len1+len2,np.shape(blk1)[1]),dtype=int)
    for i in range(np.shape(res)[0]):
        if(i<len1):
            res[i]=blk1[i]
        elif(i<len2+len1):
            res[i]=blk2[i-len1]
    return res
def create_GMat(file_path):
    res=np.zeros((16*round_num,(round_num+1)*32+16),dtype=int)
    # print((M_EQ))
    blk1=Global_mat(res,M_EQ,round_num)
    blk2=creat_NLmat()
    gmat=assemble_2blk(blk1,blk2)  
    np.save(file_path+"GLOBAL_MAT.npy",gmat)
    return gmat
if __name__=="__main__":
    create_GMat(file_path)

