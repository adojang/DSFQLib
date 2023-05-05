INPUT:

.subckt one Am Bm Q1m
L1 Am Bm 5
L2 AA Bm 5
R1 BB 0 5
xtest3 three AA BB
.subckt three A1 B7
L1 A1 B7 55
L2 A1 0 55
R1 B7 0 5
R2 B7 cake 50
R3 cake 0 54
.ends
.ends

END INPUT


DESIRED OUTPUT:

.subckt one Am Bm Q1m
L1 Am Bm 5
L2 AA_three Bm 5
R1 BB_three 0 5
L1_three AA_three BB_three 55
L2_three AA_three 0 55
R1_three BB_three 0 5
R2_three BB_three cake 50
R3_three cake 0 54
*.ends
.ends

END DESIRED OUTPUT