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
+200p 0 203p cval 205p 0
+300p 0 303p cval 305p 0
+400p 0 403p cval 405p 0
+500p 0 503p cval 505p 0
+600p 0 603p cval 605p 0
+850p 0 853p cval 855p 0)

I_b 0 4000 pwl(0 0 
+100p 0 103p cval 105p 0
+210p 0 213p cval 215p 0
+315p 0 318p cval 320p 0
+420p 0 423p cval 425p 0
+530p 0 533p cval 535p 0
+640p 0 643p cval 645p 0
+850p 0 853p cval 855p 0)


XSOURCEINa SOURCECELL 1000 2000
XLOADINa LOADINCELL 2000 A

XSOURCEINb SOURCECELL 4000 5000
XLOADINb LOADINCELL 5000 B
XLOADOUTq LOADOUTCELL C 8000
*X0SINKOUTq SINKCELL 8000
rsink 8000 0 2
*XDUT DSFQ_AND A B q

.tran 0.25p 1000p 0 0.01p
.model jjmit jj(rtype=1, vg=2.8mV, cap=0.07pF, r0=160, rn=16, icrit=100uA)

*$Ports    A B q
*.subckt DSFQ_AND A B q

.param Ibias=70u
.param main=0.84
.param secondary=0.60
.param third=1.68

* The circuit has a hold time of approximately 10ps. This can be increased by increasing the input inductors
* Either RH or RL must be chosen, and the other recalculated using the formula:
* Choose L and RL.
* RH = L/(((HoldTime/1.34) - T1)/4.5)
* This comes from the relationship HoldTime = 1.34*(Tau1 + 4.5*Tau2) 
* where Tau = L/R

.param L1=8p
.param L2=8p 
.param retentionResistor=9.8248
.param RL = 0.667

.param Lout=2p

*The precalculated values for the parasitic inductances and resistances
.param RBA=11.4332
.param LBA=6.4597p
.param RBB=8.1666
.param LBB=4.6141p
.param RBC=4.0833
.param LBC=2.3071p

L1 A 1 L1
L2 B 4 L2

RD1 1 2 RL
RD2 4 5 RL
BD1 2 C jjmit area=secondary
RDp1 2 14 RBA
Ld1 14 C LBA
BD2 5 C jjmit area=secondary
RDp2 5 15 RBA
Ld2 15 C LBA
Rh1 1 C retentionResistor
Rh2 4 C retentionResistor
B1 1 C jjmit area=main
Rb1 1 10 RBB
Lb1 10 C LBB
B2 4 C jjmit area=main
Rb2 4 11 RBB
Lb2 11 C LBB
B3 C 0 jjmit area=third
Rb3 C 13 RBC
Lb3 13 0 LBC
Ibias 0 C dc Ibias
Lout q C Lout
*.ends
.print p(rsink)
.end
