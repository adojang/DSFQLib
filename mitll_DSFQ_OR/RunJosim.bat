@ECHO ON

josim -o AW_OR_testbench.csv AW_OR_testbench.cir -V 1
josim-plot.py AW_OR_testbench.csv -t stacked

pause


