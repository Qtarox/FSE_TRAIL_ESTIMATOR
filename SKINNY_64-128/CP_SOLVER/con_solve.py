import minizinc
from datetime import timedelta
import time

def cons_cp_solve(res_name,cons_name):
    with open(res_name, "w") as fw:
        fw.write("Count of combinations\n")
    KEY_HASH={}       
    for k1 in range(1):
        for k2 in range(1):
            time_start = time.time()
            model = minizinc.Model()
            model.add_file(cons_name)
            # model.add_string("""constraint k_9 = 0;""")
            # model.add_string(f"constraint k_12 = 0;")
            # model.add_string(f"constraint k_12 = 0;")


            solver = minizinc.Solver.lookup("gecode")
            instance = minizinc.Instance(solver, model)
            result = instance.solve(all_solutions=True, timeout=timedelta(seconds=2000), processes=8)
            print("result status", result.status)

            count_k = {}
            for i, solution in enumerate(result):
                # print(f"Solution {i + 1}:")
                # print(solution)

                k_values = {attr: getattr(solution, attr) for attr in dir(solution) if attr.startswith(r'k')}
                index = tuple(k_values[key] for key in sorted(k_values.keys()))

                if index in count_k:
                    count_k[index] += 1
                else:
                    count_k[index] = 1


            print("\nCount of combinations:")
            with open(res_name, "a") as fw:
                fw.write(f"% num: {i+1}\n")
                fw.write(f"{k_values.keys()}\n")

            for key, value in count_k.items():
                with open(res_name, "a") as fw:
                    fw.write(f"{key}: {value}\n")
                # print(f"{key}: {value}")
                if(str(value) in KEY_HASH):
                    KEY_HASH[str(value)]+=1
                else:
                    KEY_HASH[str(value)]=1



            time_end = time.time()
            print("time: ", time_end-time_start)
            with open(res_name, "a") as fw:
                fw.write(f"time: {time_end-time_start}\n")
    return KEY_HASH


if __name__=="__main__":
    print(cons_cp_solve("solve_results1.txt","con_solve3.mzn"))