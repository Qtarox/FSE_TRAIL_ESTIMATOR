import numpy as np
import json
import sys
import os

Sbox=[ 12 , 6 , 9 , 0 , 1 , 10 , 2 , 11 , 3 , 8 , 5 , 13 , 4 , 14 , 7 , 15 ]
np.set_printoptions(linewidth=400)
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