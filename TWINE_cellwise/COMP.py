#res for dhh11
c1={'32': 1, '16': 2, '24': 2, '8': 2}#128
c2={'23': 120320, '18': 68608, '27': 76539, '26': 91691, '25': 25856, '33': 26112, '28': 25050, '30': 99328, '31': 27136, '42': 39936, '22': 65280, '43': 7680, '48': 11264, '45': 26880, '44': 14592, '46': 16384, '34': 26648, '35': 12776, '47': 9728, '41': 4608, '21': 19984, '17': 4352, '24': 8704, '16': 14848, '20': 20582, '19': 12938, '15': 35072, '29': 4608, '8': 13568, '7': 51968, '5': 4864, '4': 31232, '3': 29440}
c3={'20': 1, '12': 1}

res={}
for k1 in c1:
    for k2 in c2:
        for k3 in c3:
            K=int(k1)*int(k2)*int(k3)
            num=c1[k1]*c2[k2]*c3[k3]
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