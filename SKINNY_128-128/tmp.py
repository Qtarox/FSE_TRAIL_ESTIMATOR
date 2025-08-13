import config.config as config
S=config.Sbox
for i in range(256):
    if(i%16==0):
        print()
    print(str(i)+" ,"+str(S[i])+" ,",end=" ")
    