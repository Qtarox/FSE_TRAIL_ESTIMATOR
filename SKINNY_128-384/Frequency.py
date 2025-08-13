import config.config as config
import numpy as np
S=config.Sbox
c1=[0,1,4,5]
c2=[0,8,2,10]
x1=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
x2=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
hash_l=list(0 for i in range(16))
for i in c1:
    # for j in c2:
        for x in x1:
            for y in x2:
                print(S[x]^S[x^y]^S[y],x,y,i)
                hash_l[S[x]^S[x^y]^S[y]]+=1
print(hash_l)