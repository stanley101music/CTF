import sys
import string
from z3 import *

banner = "Usage:\npython solve.py brute-force\npython solve.py z3-solver\n"

if len(sys.argv) != 2:
    print(banner)

if sys.argv[1] == "brute-force":
    Serial = "76876-77776"
    ch = string.ascii_lowercase
    Name_01 = []
    Name_23 = []
    for i in ch:
        for j in ch:
            v6, v8 = ord(i), ord(j)
            v7 = (v6 & 1) + 5
            v48 = ((v6 >> 4) & 1) + 5
            v42 = ((v6 >> 1) & 1) + 5
            v44 = ((v6 >> 2) & 1) + 5
            v46 = ((v6 >> 3) & 1) + 5
            v34 = (v8 & 1) + 1
            v40 = ((v8 >> 4) & 1) + 1
            v36 = ((v8 >> 1) & 1) + 1
            v9 = ((v8 >> 2) & 1) + 1
            v38 = ((v8 >> 3) & 1) + 1

            if (v7+v9 == int(Serial[0])) and (v46 + v38 == int(Serial[1])) and (v42 + v40 == int(Serial[2])) and (v44 + v34 == int(Serial[3])) and (v48 + v36 == int(Serial[4])):
                Name_01.append(i+j)
    for i in ch:
        for j in "p":
            v20, v22 = ord(i), ord(j)
            v21 = (v20 & 1) + 5
            v49 = ((v20 >> 4) & 1) + 5
            v43 = ((v20 >> 1) & 1) + 5
            v45 = ((v20 >> 2) & 1) + 5
            v47 = ((v20 >> 3) & 1) + 5
            v35 = (v22 & 1) + 1
            v41 = ((v22 >> 4) & 1) + 1
            v37 = ((v22 >> 1) & 1) + 1
            v23 = ((v22 >> 2) & 1) + 1
            v39 = ((v22 >> 3) & 1) + 1

            if (v21+v23 == int(Serial[6])) and (v47 + v39 == int(Serial[7])) and (v43 + v41 == int(Serial[8])) and (v45 + v35 == int(Serial[9])) and (v49 + v37 == int(Serial[10])):
                Name_23.append(i+j)
    for i in Name_01:
        for j in Name_23:
            print(i+j)

elif sys.argv[1] == "z3-solver":
    Serial = [7,6,8,7,6,7,7,7,7,6]
    # Size of char = 1 byte = 8 bits
    a,b,c,d = BitVec('a', 8), BitVec('b', 8), BitVec('c', 8), ord('p')
    
    # Add constraints to solver
    solver = Solver()
    solver.add(a>=0x61, a<=0x7A, b>=0x61, b<=0x7A, c>=0x61, c<=0x7A)

    v7 = (a & 1) + 5
    v48 = ((a >> 4) & 1) + 5
    v42 = ((a >> 1) & 1) + 5
    v44 = ((a >> 2) & 1) + 5
    v46 = ((a >> 3) & 1) + 5

    v34 = (b & 1) + 1
    v40 = ((b >> 4) & 1) + 1
    v36 = ((b >> 1) & 1) + 1
    v9 = ((b >> 2) & 1) + 1
    v38 = ((b >> 3) & 1) + 1  

    v21 = (c & 1) + 5
    v49 = ((c >> 4) & 1) + 5
    v43 = ((c >> 1) & 1) + 5
    v45 = ((c >> 2) & 1) + 5
    v47 = ((c >> 3) & 1) + 5

    v35 = (d & 1) + 1
    v41 = ((d >> 4) & 1) + 1
    v37 = ((d >> 1) & 1) + 1
    v23 = ((d >> 2) & 1) + 1
    v39 = ((d >> 3) & 1) + 1

    # Add constraints to solver
    solver.add(
        v7 + v9 == Serial[0],
        v46 + v38 == Serial[1],
        v42 + v40 == Serial[2],
        v44 + v34 == Serial[3],
        v48 + v36 == Serial[4],
        v21 + v23 == Serial[5],
        v47 + v39 == Serial[6],
        v43 + v41 == Serial[7],
        v45 + v35 == Serial[8],
        v49 + v37 == Serial[9]
    )

    # Iterate through all possible answers
    flag = []
    while solver.check() == sat:
        m = solver.model()
        sa,sb,sc = chr(m[a].as_long()),chr(m[b].as_long()),chr(m[c].as_long())
        flag.append(sa + sb + sc + 'p')
        solver.add(Or(a!=m[a], b!=m[b], c!=m[c]))
    print(flag)