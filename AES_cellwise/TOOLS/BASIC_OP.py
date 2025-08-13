import numpy as np
import json
import sys
import os
import config.config as config
from GEN_L.GEN_LMAT import *
Sbox= config.Sbox
file_path=config.file_path
DC=config.DC
Sbox=config.Sbox
L=len(Sbox)
np.set_printoptions(linewidth=400)


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
    for input in range():
        for output in range(L):
            cnt=0
            for x in range(L):
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
    for x in range(L):
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
    for x in range(L):
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

def Wilson_Score(z,n,p):
    w1=1/(1+z**2/n)*(p+(z**2)/(2*n)- (z/(2*n))*np.sqrt(4*n*p*(1-p)+z**2) )
    w2=1/(1+z**2/n)*(p+(z**2)/(2*n)+ (z/(2*n))*np.sqrt(4*n*p*(1-p)+z**2) )
    print("the interval is: [ ",w1, " , ",w2, " ] ")
def pure_lstxor(l1,l2):
    res=[]
    for i in l1:
        for j in l2:
            res.append(i^j)
    return res
if __name__=="__main__":

    # l1=[117, 207]
    # l2=[55, 244]
    # l3=pure_lstxor(l1,l2)
    # l1=[83, 116]
    # l2=[238, 194]
    # l4=pure_lstxor(l1,l2)
    # print(pure_lstxor(l3,l4))
    # l5=pure_lstxor(l3,l4)
    # print(pure_lstxor(l5,[7,117]))
    # Wilson_Score(1.96,10000,0.22)
    Wilson_Score(1.96,1000,1)#[-7.86,-7.1]
    # lst=[0 for i in range(256)]
    # for i in range(256):
    #     for j in range(256):
    #         if(len(xddt_list(i,j))==4):
    #             print("in: ",i,"; out: ",j)
    #             lst[i]=j
    # print(lst)