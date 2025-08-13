import numpy as np
import json
import sys
import os
import config.config as config
Sbox= config.Sbox
np.set_printoptions(linewidth=400)

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
    res=set(res)
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
    for x in range(16):
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
    for x in range(16):
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
    original_stdout = sys.stdout

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
    l1=list_xor([8,13],[10,11,14,15])
    l2=list_xor([10,11,14,15],[0,8])
    l3=list_xor(l2,[3,14])
    print(list_xor([1,9],[4,6,12,14]))
    print(l3)
    l4=list_xor([5, 13, 7, 15],[5, 7, 13, 15])
    print(l4)
    print(list_xor([10, 11, 14, 15],[10, 11, 14, 15]))
    y112=[0,8]
    x215=[8,13]
    x23=[3,14]
    print(list_xor(list_xor(y112,x215),x23))
    print(list_xor({8, 0, 10, 2},SBOX_MAP({2, 3, 6, 7, 10, 11, 14, 15})))