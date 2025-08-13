import minizinc
from datetime import timedelta
import time


with open("solve_results.txt", "w") as fw:
    fw.write("Count of combinations\n")
        
for k1 in range(16):
    for k2 in range(1):
        time_start = time.time()
        model = minizinc.Model()
        model.add_file("con_solve2.mzn")
        model.add_string("""constraint k_10 = 0;""")
        model.add_string(f"constraint k_2 = {k1};")
        model.add_string(f"constraint k_9 = {k2};")


        solver = minizinc.Solver.lookup("gecode")
        instance = minizinc.Instance(solver, model)
        result = instance.solve(all_solutions=True, timeout=timedelta(seconds=2000), processes=8)
        print("result status", result.status)

        count_k = {}
        for i, solution in enumerate(result):
            # print(f"Solution {i + 1}:")
            # print(solution)

            k_values = {attr: getattr(solution, attr) for attr in dir(solution) if attr.startswith("k_")}
            index = tuple(k_values[key] for key in sorted(k_values.keys()))

            if index in count_k:
                count_k[index] += 1
            else:
                count_k[index] = 1


        print("\nCount of combinations:")
        with open("solve_results.txt", "a") as fw:
            fw.write(f"% num: {i+1}\n")
            fw.write(f"{k_values.keys()}\n")

        for key, value in count_k.items():
            with open("solve_results.txt", "a") as fw:
                fw.write(f"{key}: {value}\n")
            # print(f"{key}: {value}")


        time_end = time.time()
        print("time: ", time_end-time_start)
        with open("solve_results.txt", "a") as fw:
            fw.write(f"time: {time_end-time_start}\n")