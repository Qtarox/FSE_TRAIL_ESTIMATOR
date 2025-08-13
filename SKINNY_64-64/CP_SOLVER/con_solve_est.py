import minizinc
from datetime import timedelta
import time
import random
N=50
def gen_rand_sequence(n):
    #given n elements generate 1000 random tuples
    res=[]
    for i in range(N):
        tmp=[]
        for j in range(n):
            tmp.append(random.randint(0, 15))
        res.append(tmp.copy())
    return res

def cons_cp_solve(res_name,cons_name,key_var):
    with open(res_name, "w") as fw:
        fw.write("Count of combinations\n")
    KEY_HASH={}       
    key=list(key_var)
    print("invovlved keys: ", key)
    num=len(key)
    key_set=gen_rand_sequence(num)
    count_k = []
    ######################
    for K in key_set:
        time_start = time.time()
        model = minizinc.Model()
        model.add_file(cons_name)
        for key_ind in range(num):
            model.add_string("constraint "+key[key_ind]+" = "+str(K[key_ind])+";")



        solver = minizinc.Solver.lookup("gecode")
        instance = minizinc.Instance(solver, model)
        result = instance.solve(all_solutions=True, timeout=timedelta(seconds=2000), processes=8)
        # print("result status", result.status)
        # TODO: get the count for this single key, and save this count
        # after this, we just need to get a list of 1000 elements
        
        count=0
        for i, solution in enumerate(result):
            # print(f"Solution {i + 1}:")
            # print(solution)

            count+=1
        count_k.append(count)
    




    time_end = time.time()
    print("time: ", time_end-time_start)
    with open(res_name, "a") as fw:
        fw.write(f"time: {time_end-time_start}\n")


    return count_k


if __name__=="__main__":
    print(cons_cp_solve("solve_results1.txt","con_solve3.mzn"))