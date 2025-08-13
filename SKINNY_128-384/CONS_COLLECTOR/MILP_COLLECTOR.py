import numpy as np
file_name="X_MAT.npy"
def generate_lp(file_name1):

    # 生成随机二进制向量
    # np.random.seed(42)
    # vectors = np.random.randint(0, 2, size=(num_vectors, dimension))
    # print(vectors)
    vectors=np.load(file_name1)
    num_vectors = np.shape(vectors)[0]  # 使用的向量数量
    dimension = np.shape(vectors)[1]  # 向量的维度
    s = ''
    for i in range(num_vectors):
        s += ('x' + str(i) + ' + ')
    constraint1 = s[0:-3] + " - obj = 0\n"
    # constraint1 += "obj = 4\n"
    constraint1 += s[0:-3] + " >= 1\n"
    integer_var = ''
    # 准备写入 .lp 文件
    filename = 'xor_problem.lp'
    with open(filename, 'w') as file:
        file.write("Minimize\n")  # 目标函数为空，只关心可行性
        file.write("obj\n")
        file.write("Subject To\n")
        file.write(constraint1)
        for j in range(dimension):
            # 为每个维度生成约束
            terms = [f" + {vectors[i][j]} x{i}" for i in range(num_vectors) if vectors[i][j] == 1]
            constraint = ''
            if terms:
                constraint += ''.join(terms)
                # 在模2条件下，应使用等式约束，目标值为2k（k是整数）
                # 由于这里我们只考虑binary变量，需要确保和为偶数
                constraint += f" - 2 y{j} = 0\n"
                file.write(constraint)
                integer_var += f'y{j} '
            # else:
            #     # 如果一个维度所有向量都为0，直接指定该维度的约束
            #     file.write(f"0 = 0\n")

        file.write("Binary\n")
        for i in range(num_vectors):
            file.write(f" x{i}\n")
        
        file.write("INTEGER\n")
        # 定义额外的辅助整数变量y，以确保约束可以被整除
        file.write(integer_var + '\n')
        file.write("End\n")
    print(f"File {filename} has been written.")


from gurobipy import  read, GRB

# 载入模型
def solve_lp():
    model = read('xor_problem.lp')
    """
    # 输出一个结果
    # 运行优化
    model.optimize()
    if model.status == 2:
        print('Optimal solution found.')
        for v in model.getVars():
            if int(v.x) >0:
                print(f'{v.varName} = {v.x}')
    """
    # 输出多个结果
    model.Params.PoolSearchMode = 2
    model.Params.PoolSolutions = 20000000
    model.optimize()
    num_solution = model.SolCount
    print("******number of retained solutions: ", num_solution)

    Final_list=[]

    for j in range(num_solution):
        model.Params.SolutionNumber = j
        model.setParam(GRB.Param.SolutionNumber, j)
        # print("PoolObjVal", model.PoolObjVal)
        # model.setParam(GRB.Param.SolutionNumber, j)
        tmp_list=[]
        for v in model.getVars():
            if (int(v.xn) >0 and v.varName[0]=='x'):
                # print(f'{v.varName} = {v.xn}')
                tmp_list.append(int(v.varName[1:]))
        # print(tmp_list)
        Final_list.append(tmp_list)
    return Final_list

def is_included(l1,l2):
    for i in l1:
        if(i in l2):
            pass
        else:
            return False
    return True

def reduce(list0):
    res=[]
    tmp0=[]
    for i in list0:
        tmp0.append(i.copy())
    for i in range(len(list0)):
        sub_i=list0[i]
        if(sub_i in res):
            pass
        else:
            if(sub_i==[]):
                continue
            res.append(sub_i.copy())
            for j in range(len(list0)):
                if(j<=i):
                    pass
                else:
                    list0[j] = [x for x in list0[j] if x not in sub_i]
    return res

def get_LIST0(file_name1):
    generate_lp(file_name1)
    List0=solve_lp()
    list_final=reduce(List0)
    return list_final

if __name__=="__main__":
    final_list=(get_LIST0(file_name1=file_name))
    print("solution number: ",len(final_list),"\n solutions:", final_list)