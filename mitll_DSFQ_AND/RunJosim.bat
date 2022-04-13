@ECHO ON

josim -o AW_AND_testbench.csv AW_AND_testbench.cir -V 1
josim-plot.py AW_AND_testbench.csv -t stacked








pause


