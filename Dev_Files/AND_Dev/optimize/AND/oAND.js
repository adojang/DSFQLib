* JSIM deck file generated with TimEx
* === DEVICE-UNDER-TEST ===

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
.param cval=600u

I_a 0 1000 pwl(0 0 
+100p 0 103p cval 105p 0 
+120p 0 123p cval 125p 0
+300p 0 303p cval 305p 0
+400p 0 403p cval 405p 0
+720p 0 723p cval 725p 0
+820p 0 823p cval 825p 0
+850p 0 853p cval 855p 0)

I_b 0 4000 pulse(cval 0 100p 1p 1p 3p 200p)


XSOURCEINa SOURCECELL 1000 2000
XLOADINa LOADINCELL 2000 A

XSOURCEINb SOURCECELL 4000 5000
XLOADINb LOADINCELL 5000 B
XLOADOUTq LOADOUTCELL q 8000
XSINKOUTq SINKCELL 8000

*XDUT dsfq_and A B q

.tran 0.25p 1000p 0 0.01p
.model jjmit jj(rtype=1, vg=2.8mV, cap=0.07pF, r0=160, rn=16, icrit=100uA)

*$Ports    A B q
*.subckt DSFQ_AND A B q
.param pInduc = 1p


.param main=8.13825665e-01 
.param secondary=5.17677402e-01 
.param third=1.13196361e+00 


.param Ibiasz=4.62813248e-05
.param L1=8.11392791e-12
.param L2=8.85286944e-12  
.param Lout=1.47191818e-12 
.param retentionResistor=3.47741865e+00


L1 A 1 L1
L2 B 4 L2
RD1 1 2 0.67
RD2 4 5 0.67
BD1 2 C jjmit area=secondary
RDp1 2 14 2.8
Ld1 14 C pInduc
BD2 5 C jjmit area=secondary
RDp2 5 15 2.8
Ld2 15 C pInduc
Rh1 1 C retentionResistor
Rh2 4 C retentionResistor
B1 1 C jjmit area=main
Rb1 1 10 2.37
Lb1 10 C pInduc
B2 4 C jjmit area=main
Rb2 4 11 2.37
Lb2 11 C pInduc
B3 C 0 jjmit area=third
Rb3 C 13 1.67
Lb3 13 0 pInduc
Ibias 0 C dc Ibiasz
Lout C q Lout
*.ends



*.PRINT NODEV A 0
*.PRINT NODEV B 0
*.PRINT NODEV q 0
.print i(L6.XSOURCEINa) i(L6.XSOURCEINb) p(B3)
*.print p(B3)
.end
