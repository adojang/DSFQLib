* JSIM deck file generated with TimEx
* === DEVICE-UNDER-TEST ===
* A Generic DSFQ AND Gate for use in simulating Logic Gates
* Copyright (q) 2022-2024 Adriaan van Wijk, Stellenbosch University
* Based on the design by Rylov [2019]
* This gate is not meant to be directly attached to PTLs as it does not support integrated PTL ports.
* Version 1.0
*$Ports    A B q
.subckt DSFQ_AND A B q
.param main=0.84
.param secondary=0.60
.param third=1.68
.param pInduc = 1p
.param retentionResistor=4
.model jjmit jj(rtype=1, vg=2.8mV, cap=0.07pF, r0=160, rn=16, icrit=100uA)
L1 A 1 12p
L2 B 4 12p
RD1 1 2 0.67
RD2 4 5 0.67
BD1 2 q jjmit area=secondary
RDp1 2 14 2.8
Ld1 14 q pInduc
BD2 5 q jjmit area=secondary
RDp2 5 15 2.8
Ld2 15 q pInduc
Rh1 1 q retentionResistor
B1 1 q jjmit area=main
Rb1 1 10 2.37
Lb1 10 q pInduc
Rh2 4 q retentionResistor
B2 4 q jjmit area=main
Rb2 4 11 2.37
Lb2 11 q pInduc
B3 0 q jjmit area=third
Rb3 q 13 1.67
Lb3 13 0 pInduc
Ibias 0 q dc 70u
.ends
* === SOURCE DEFINITION ===
.SUBCKT SOURCECELL  8 11
b1   1  2  jjmitll100 area=2.25
b2   3  4  jjmitll100 area=2.25
b3   5  6  jjmitll100 area=2.5
ib1  0  2  pwl(0 0 5p 275ua)
ib2  0  5  pwl(0 0 5p 175ua)
l1   8  7  1p
l2   7  0  3.9p
l3   7  1  0.6p
l4   2  3  1.1p
l5   3  5  4.5p
l6   5  11 2p
lp2  4  0  0.2p
lp3  6  0  0.2p
lrb1 9  2  1p
lrb2 10 4  1p
lrb3 12 6  1p
rb1  1  9  4.31
rb2  3  10 4.31
rb3  5  12 3.88
.model jjmitll100 jj(rtype=1, vg=2.8mv, cap=0.07pf, r0=160, rn=16, icrit=0.1ma)
.ENDS SOURCECELL
* === INPUT LOAD DEFINITION ===
.SUBCKT LOADINCELL  2 5
b1 1 6 jjmitll100 area=2.5
b2 4 8 jjmitll100 area=2.5
ib1 0 3 pwl(0 0 5p 350ua)
l1 2 1 2p
l2 1 3 2p
l3 3 4 2p
l4 4 5 2p
lb1 7 6 1p
lb2 9 8 1p
lp1 6 0 0.2p
lp2 8 0 0.2p
rb1 1 7 3.88
rb2 4 9 3.88
.model jjmitll100 jj(rtype=1, vg=2.8mv, cap=0.07pf, r0=160, rn=16, icrit=0.1ma)
.ENDS LOADINCELL
* === OUTPUT LOAD DEFINITION ===
.SUBCKT LOADOUTCELL  2 5
b1 1 6 jjmitll100 area=2.5
b2 4 8 jjmitll100 area=2.5
ib1 0 3 pwl(0 0 5p 350ua)
l1 2 1 2p
l2 1 3 2p
l3 3 4 2p
l4 4 5 2p
lb1 7 6 1p
lb2 9 8 1p
lp1 6 0 0.2p
lp2 8 0 0.2p
rb1 1 7 3.88
rb2 4 9 3.88
.model jjmitll100 jj(rtype=1, vg=2.8mv, cap=0.07pf, r0=160, rn=16, icrit=0.1ma)
.ENDS LOADOUTCELL
* === SINK DEFINITION ===
.SUBCKT SINKCELL  1
r1 1 0 2
.ENDS SINKCELL
* ===== MAIN =====
I_a 0 1 pwl(0 0 5p 0 1.25E-11 0 1.35E-11 0.001 1.45E-11 0)
XSOURCEINa SOURCECELL 1 2
XLOADINa LOADINCELL 2 3
I_b 0 4 pwl(0 0 5p 0 2.25E-11 0 2.35E-11 0.001 2.45E-11 0)
XSOURCEINb SOURCECELL 4 5
XLOADINb LOADINCELL 5 6
XLOADOUTq LOADOUTCELL 7 8
XSINKOUTq SINKCELL 8
XDUT dsfq_and 3 6 7
.tran 2.5E-13 4E-11 0 2.5E-13
.PRINT NODEV 3 0
.PRINT NODEV 6 0
.PRINT NODEV 7 0
.end
