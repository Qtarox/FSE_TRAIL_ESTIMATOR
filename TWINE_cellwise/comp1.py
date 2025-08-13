#res for dhh11
c1={'8': 3072, '12': 512, '4': 512}#128
c2={'20': 1024, '12': 1024, '24': 512, '8': 512, '16': 1024}
c3={'20': 1024, '12': 1024, '24': 512, '16': 1024, '8': 512}
c4= {'2': 96, '1': 64}
res={}
for k1 in c1:
    for k2 in c2:
        for k3 in c3:
            for k4 in c4:
                K=int(k1)*int(k2)*int(k3)*int(k4)
                num=c1[k1]*c2[k2]*c3[k3]*c4[k4]
                if(str(K) in res):
                    res[str(K)]+=num
                else:
                    res[str(K)]=num

# print(res)
sum=0
for k in res:
    sum+=res[k]
# print(sum)
R={}
for k in res:
    R[(int(int(k)))]=res[k]/sum*100
sorted_dict = {key: R[key] for key in sorted(R)}
print(sorted_dict)

# s=0
# c=8**5
# for key in sorted_dict:
#     if(key<7*c*8 and key>=7*c):
#         s+=sorted_dict[key]

# print(s)

# print(R)