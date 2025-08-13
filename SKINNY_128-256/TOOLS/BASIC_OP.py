import numpy as np
import json
import sys
import os
import config.config as config
Sbox= config.Sbox
s_inv=config.Sbox_inv
np.set_printoptions(linewidth=400)

def Inv_SBOX_MAP(list1):
    list2=[]
    for i in list1:
        list2.append(s_inv[i])
    return list2.copy()
def SBOX_MAP(list1):
    list2=[]
    for i in list1:
        list2.append(Sbox[i])
    return list2.copy()

def corr_ind(ind_num):
    rn=ind_num//32
    j=ind_num%32
    if(j<16): #is an ind of x
        x_rn=rn+1
        y_rn=x_rn
        y_ind=j+16
        y_num=y_rn*32+y_ind
        return y_num
    else: #ind of y
        y_rn=rn
        x_rn=y_rn
        x_ind=j-16
        x_num=(x_rn-1)*32+x_ind
        return x_num
       
def list_xor(l1,l2):#two possible set xor
    res=[]
    for i in l1:
        for j in l2:
            res.append(i^j)
    dic_tmp={}
    res=sorted(res)
    for i in res:
        if(i in dic_tmp):
            dic_tmp[i]+=1
        else:
            dic_tmp[i]=1
    flg=False
    gcd_t=256
    for i in range(256):
        if(i not in dic_tmp or dic_tmp[i]==0):
            continue
        elif(flg==False):
            gcd_t=dic_tmp[i]
            flg=True
        else:
            gcd_t=np.gcd(gcd_t,dic_tmp[i])
        if(gcd_t==1):
            break
    if(gcd_t==1):
        return res
    res=[]
    for i in range(256):
        if(i not in dic_tmp):
            continue
        t=(dic_tmp[i]//gcd_t)
        for j in range(t):
            res.append(i)
    
    return res
    

def X_DDT(xddt):
    for input in range(16):
        for output in range(16):
            cnt=0
            for x in range(16):
                x1=x
                x2=x^input
                y1=Sbox[x1]
                y2=Sbox[x2]
                if(y1^y2==output and input!=0):
                    xddt[input][output][cnt]=x
                    cnt=cnt+1
    return xddt

def xddt_list(input,output):
    res=[]
    for x in range(256):
        x1=x
        x2=x^input
        y1=Sbox[x1]
        y2=Sbox[x2]
        if(y1^y2==output and input!=0):
            res.append(x)
            #print("XDDT("+str(input)+", "+str(output)+")="+str(tmp))
    return res
    

def yddt_list(input,output):
    res=[]
    for x in range(256):
        x1=x
        x2=x^input
        y1=Sbox[x1]
        y2=Sbox[x2]
        if(y1^y2==output and input!=0):
            res.append(y1)
    return res


def corr_ind(ind_num):
    rn=ind_num//32
    j=ind_num%32
    if(j<16): #is an ind of x
        x_rn=rn
        y_rn=x_rn
        y_ind=j+16
        y_num=y_rn*32+y_ind
        return y_num
    else: #ind of y
        y_rn=rn
        x_rn=y_rn
        x_ind=j-16
        x_num=(x_rn)*32+x_ind
        return x_num

def create_folder(pth):
# Create the new folder if it doesn't already exist
    if not os.path.exists(pth):
        os.makedirs(pth)
    # Verify if the folder has been created
    os.path.exists(pth)
def creat_dic(file_path,round):
    x_dic={}
    y_dic={}
    for r in range(len(round)):
        for x_index in range(16):
            if(round[r][0][x_index]==0):
                continue
            k_tmp='x_'+str(r)+'_'+str(x_index)
            y_tmp='y_'+str(r)+'_'+str(x_index)
            l_x=xddt_list(round[r][0][x_index],round[r][1][x_index])
            l_y=yddt_list(round[r][0][x_index],round[r][1][x_index])
            x_dic[k_tmp]=l_x.copy()
            y_dic[y_tmp]=l_y.copy()
    # original_stdout = sys.stdout

    # Specify the file name where you want to save the output
    file_x= file_path+"act_x.json"

        # Open the file in write mode, this will create the file if it doesn't exist
    with open(file_x, 'w') as json_file1:
        # Redirect the standard output to the file
        json.dump(x_dic, json_file1)
    
    file_y= file_path+"act_y.json"

        # Open the file in write mode, this will create the file if it doesn't exist
    with open(file_y, 'w') as json_file2:
        # Redirect the standard output to the file
        json.dump(y_dic, json_file2)

def load_dic(file_path):
    if os.path.exists(file_path):
        f = open(file_path, encoding='utf-8')
        content = f.read()
        user_dic = json.loads(content)
        return user_dic
    
x_dic=load_dic(config.file_path+"act_x.json")
y_dic=load_dic(config.file_path+"act_y.json")

def is_active(num,x_dic=x_dic,y_dic=y_dic):
    rn=num//32
    ind=num%32
    if(ind<16):#is x
        x_rn=rn
        if(("x_"+str(x_rn)+"_"+str(ind)) in x_dic):
            # print("x_"+str(x_rn)+"_"+str(ind))
            return True
        else:
            return False
    else:
        y_rn=rn
        y_ind=ind-16
        if(("y_"+str(y_rn)+"_"+str(y_ind)) in y_dic):
            # print("y_"+str(y_rn)+"_"+str(y_ind))
            return True
        else:
            return False

def active_list(num,x_dic=x_dic,y_dic=y_dic):
    rn=num//32
    ind=num%32
    if(ind<16):#is x
        x_rn=rn
        if(("x_"+str(x_rn)+"_"+str(ind)) in x_dic):
            # print("x_"+str(x_rn)+"_"+str(ind))
            return x_dic["x_"+str(x_rn)+"_"+str(ind)]
        else:
            return False
    else:
        y_rn=rn
        y_ind=ind-16
        if(("y_"+str(y_rn)+"_"+str(y_ind)) in y_dic):
            # print("y_"+str(y_rn)+"_"+str(y_ind))
            return y_dic["y_"+str(y_rn)+"_"+str(y_ind)]
        else:
            return False      
if __name__=="__main__":
    Z= [0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23, 32, 33, 34, 35, 36, 37, 38, 39, 48, 49, 50, 51, 52, 53, 54, 55, 64, 65, 66, 67, 68, 69, 70, 71, 80, 81, 82, 83, 84, 85, 86, 87, 96, 97, 98, 99, 100, 101, 102, 103, 112, 113, 114, 115, 116, 117, 118, 119, 128, 129, 130, 131, 132, 133, 134, 135, 144, 145, 146, 147, 148, 149, 150, 151, 160, 161, 162, 163, 164, 165, 166, 167, 176, 177, 178, 179, 180, 181, 182, 183, 192, 193, 194, 195, 196, 197, 198, 199, 208, 209, 210, 211, 212, 213, 214, 215, 224, 225, 226, 227, 228, 229, 230, 231, 240, 241, 242, 243, 244, 245, 246, 247]
    Z2=[0, 0, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 35, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 64, 65, 66, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 97, 99, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]
    Z=  [0, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 25, 26, 27, 28, 29, 30, 31, 64, 66, 68, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 82, 84, 86, 88, 89, 90, 91, 92, 93, 94, 95, 128, 130, 132, 134, 136, 137, 138, 139, 140, 141, 142, 143, 144, 146, 148, 150, 152, 153, 154, 155, 156, 157, 158, 159, 192, 194, 196, 198, 200, 201, 202, 203, 204, 205, 206, 207, 208, 210, 212, 214, 216, 217, 218, 219, 220, 221, 222, 223] 
    Z3=(list_xor(SBOX_MAP(Z),Z2))
    count=0
    for x in Z3:
        if(x==0):
            count+=1
    print(count)
    # print(len(Z)*(len(Z2)))
    print(len(Z3))
    # print(len(Z2))
    Z2={'z_0_99': [8, 9, 10, 11, 12, 13, 14, 15, 40, 41, 42, 43, 44, 45, 46, 47, 88, 89, 90, 91, 92, 93, 94, 95, 120, 121, 122, 123, 124, 125, 126, 127, 152, 153, 154, 155, 156, 157, 158, 159, 184, 185, 186, 187, 188, 189, 190, 191, 216, 217, 218, 219, 220, 221, 222, 223, 248, 249, 250, 251, 252, 253, 254, 255], 
    'z_1_99': [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24, 25, 25, 25, 26, 26, 26, 27, 27, 27, 28, 28, 28, 29, 29, 29, 30, 30, 30, 31, 31, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 64, 64, 65, 65, 65, 66, 66, 66, 67, 67, 67, 68, 68, 68, 69, 69, 69, 70, 70, 70, 71, 71, 71, 72, 72, 72, 73, 73, 73, 74, 74, 74, 75, 75, 75, 76, 76, 76, 77, 77, 77, 78, 78, 78, 79, 79, 79, 80, 80, 80, 81, 81, 81, 82, 82, 82, 83, 83, 83, 84, 84, 84, 85, 85, 85, 86, 86, 86, 87, 87, 87, 88, 88, 88, 89, 89, 89, 90, 90, 90, 91, 91, 91, 92, 92, 92, 93, 93, 93, 94, 94, 94, 95, 95, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127],
    'k_4': [16, 17, 18, 19, 20, 21, 22, 23, 56, 57, 58, 59, 60, 61, 62, 63, 80, 81, 82, 83, 84, 85, 86, 87, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 144, 145, 146, 147, 148, 149, 150, 151, 168, 169, 170, 171, 172, 173, 174, 175, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 208, 209, 210, 211, 212, 213, 214, 215, 232, 233, 234, 235, 236, 237, 238, 239, 248, 249, 250, 251, 252, 253, 254, 255]}
    print(list_xor(SBOX_MAP(Z2["z_0_99"]),Z2["z_1_99"]))

