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

I_b 0 4000 pulse(cval 0 200p 1p 1p 3p 200p)

.tran 0.25p 1000p 0 0.01p

XSOURCEINa SOURCECELL 1000 2000
XLOADINa LOADINCELL 2000 A

XSOURCEINb SOURCECELL 4000 5000
XLOADINb LOADINCELL 5000 B
XLOADOUTq LOADOUTCELL q 8000
XSINKOUTq SINKCELL 8000

*XDUT dsfq_and A B q

*$Ports 		 A B q
*.subckt DSFQ_OR A B q

.model jjmit jj(rtype=1, vg=2.8mV, cap=0.07pF, r0=160, rn=16, icrit=0.1mA)

.param Bps=0.5
.param Bp=0.7
.param Bia=1.2
.param Bib=1.2
.param Bua=1
.param Bub=1
.param Bla=1.3
.param Blb=1.3
.param Blim=1.8

.param LBias =350p
.param Lpoff = 16p
.param Rs=1
.param RH=4
.param IB1=270u



.param pinduct = 1p
Bia A 1 jjmit area=Bia
Ria A 10 1.97
Lia 10 1 pinduct

Bib B 3 jjmit area=Bib
Rib B 11 1.97
Lib 11 3 pinduct

Bua 1 2 jjmit area=Bua
Rua 1 13 2.16
Lua 13 2 pinduct

Bub 3 2 jjmit area=Bub
Rub 3 14 2.16
Lub 14 2 pinduct

Bla 1 0 jjmit area=Bla
Rla 1 15 1.90
Lla 15 0 pinduct

Blb 3 0 jjmit area=Blb
Rlb 3 16 1.90
Llb 16 0 pinduct

Lpoff 2 4 Lpoff
Rs 4 5 Rs
RH 4 0 RH

Bp 4 0 jjmit area=Bp
Rp 4 17 2.59
Lp 17 0 pinduct

Bps 5 0 jjmit area=Bps
Rps 5 18 2.79
Lps 18 0 pinduct
Lbias q VDD Lbias

IB1 0 VDD pwl(0 0 5p IB1 )

Blim q 2 jjmit area=Blim
Rlim 19 2 1.6
Llim 19 q pinduct
*.ends



*.PRINT NODEV A 0
*.PRINT NODEV B 0
*.PRINT NODEV q 0
.print i(L6.XSOURCEINa) i(L6.XSOURCEINb) p(BLIM)
*.print p(B3)
.end
