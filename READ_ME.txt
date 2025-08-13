#this is the read me for Trail-Estimator Source Code#
1. The XXXX_Verifier.py file  in each folder is the Trail-Estimator implementation, running it will simply calculate the solution for constraints of corresponding trails
2. In config/config.py file, user can adjust the target differential characterstic by setting DC_name variable;
3. The detailed differential trail is post in DCs.py in config/  under each folder
4. Here we have code for LBLOCK, TWINE, SKINNY-64 and SKINNY-128
5. indep in the filename means we treat subkey as independent
6. for skinny-64-128&192 file we provide the automatic solver based on CP, which considers the key scheduling of TK2&3

7. for skinny-128-256&384 file we provide the automatic solver based on CP, which considers the key scheduling of TK2&3

8. SKINNY_64-TK23INDEP， SKINNY_128-TK23INDEP are the simplified version of detector and solver which do not consider TK  key scheduling to reduce the complexity of solving. However, the result is just for reference and not included in paper.

9. The estimation method solver is stored in CP_Solver con_solve_est.py

