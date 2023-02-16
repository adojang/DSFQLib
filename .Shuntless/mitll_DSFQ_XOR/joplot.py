import os
os.system('cmd /k "josim -o testbench.csv testbench.cir -V 1"')
os.system('cmd /k "python josim-plot.py testbench.csv"')