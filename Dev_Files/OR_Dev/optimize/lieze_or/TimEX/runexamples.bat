@ECHO OFF

REM run example sequence for TimEx
REM Author:    Coenrad Fourie
REM Last mod:  2 February 2022 - L Schindler

REM You need in the path: jsim_n, iverilog and vvp

@ECHO ON

TimEx ORv1.cir -d definitions.txt -x

pause


