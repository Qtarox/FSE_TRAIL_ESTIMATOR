import numpy as np
import config.config as config
np.set_printoptions(linewidth=400)
np.set_printoptions(threshold=np.inf)
round_num=config.round_num
file_path=config.file_path
# round_num=1
MC=[[2,3,1,1],
    [1,2,3,1],
    [1,1,2,3],
    [3,1,1,2]]

X_IND=[[0,5,10,15],
       [1,6,11,12],
       [2,7,8,13],
       [3,4,9,14]]

def gen_BL_MAT():
   Bmat=np.zeros((16,32+16),dtype=int)
   for i in range(4):
      for j in range(4):
         row=i*4+j
         Bmat[row][16+row]=1
         Bmat[row][32+row]=1
         for k in range(4):
            Bmat[row][X_IND[j][k]]=MC[i][k]
   # print(Bmat)
   return Bmat



def gen_lmat():
   tmp=gen_BL_MAT()
   #generate a matrix of size 16*round_num  * (32+16)*round_num
   L_mat=np.zeros((16*(round_num),48*(round_num+1)),dtype=int)
   for i in range(round_num):
      for j in range(16):
         row=i*16+j
         s_ind=32*i
         k_ind=32*(round_num+1)+16*i
         L_mat[row][s_ind+16:s_ind+32]=tmp[j][:16]
         L_mat[row][s_ind+32+j]=1
         L_mat[row][k_ind+j]=1
   return L_mat

def gen_nl_mat():
   NL_mat=np.zeros((16*(round_num),48*(round_num+1)),dtype=int)
   for i in range(round_num):
      for j in range(16):
         row=i*16+j
         s_ind=32*i
         # k_ind=32*round_num+16*i
         NL_mat[row][s_ind+j]=1
         NL_mat[row][s_ind+16+j]=1
         # NL_mat[row][k_ind+j]=1
   return NL_mat

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

def gen_GM():
   G_mat=assemble_2blk(gen_lmat(),gen_nl_mat())
   np.save(file_path+"GLOBAL_MAT.npy",G_mat)
   return G_mat
if __name__=="__main__":
   # print(gen_lmat())
   gen_GM()