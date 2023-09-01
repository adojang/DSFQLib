#!/usr/bin/env python
import sys, getopt, csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from subprocess import call
import scipy.constants as cnst
import time
import shutil
import matplotlib.ticker as tick
from itertools import count
from itertools import takewhile
import itertools
marker = itertools.cycle((',', '+', '.', 'o', '*')) 



def any_range(start, stop, step):
    start = type(start + step)(start)
    return takewhile(lambda n: n < stop, count(start, step))


#Usage: python ivcurve.py josim yourfile.cir linenumber min max steps
#Example: python ivcurve.py josim t2.cir 28 4 20 4

# python ivcurve.py josim t2.cir 19 2 20 10

#    python ivcurve.py josim t4.cir 20 2 8 0.5

sim = sys.argv[1];
infile = sys.argv[2];
linetochange = int(sys.argv[3]) -1;
rangemin = float(sys.argv[4]);
rangemax = float(sys.argv[5]) + 1;
steps = float(sys.argv[6]);
outfile = infile.replace(".cir",".csv");

shutil.copyfile(infile, 'tempfile.cir')
# infile = 'tempfile.';
Phizero = 2*cnst.e / cnst.hbar;
k = Phizero / (2 * cnst.pi);
avgV = list()
avgVolt = list()
resistor = list()
fig = plt.figure()
ax = fig.add_subplot(111)


#SETUP, INITIAL RUN AND FILE POPULATION



for x in any_range(rangemin, rangemax, steps):

  
    netlist = open(infile, "r");
    netlistdata = netlist.readlines();
    netlist.close();
    tokens = netlistdata[linetochange].split();
    tokens2 = netlistdata[linetochange+1].split();

    # Change and Save and Run for all numbers in the range
    #This changes something like L1 and L2. The numbers must be above one another in the spice file.

    tokens[3] = str(x) + 'e-12';
    tokens2[3] = str(x) + 'e-12';

    netlistdata[linetochange] = ' '.join(tokens) + "\n"
    netlistdata[linetochange+1] = ' '.join(tokens2) + "\n"
    # infile = 'temp.cir'
    netlist = open('tempfile.cir', "w"); #OPEN TEMP FILE
    netlist.writelines(netlistdata); #WRITE NEW R VALUE TO FILE
    netlist.close();

    call([sim, "-o", outfile, 'tempfile.cir'])
    filename = outfile
    data = np.genfromtxt(filename, delimiter=',', skip_header=1, dtype=None)
    t = data[:,0] #time
    i = data[:,1] #current

   
    print(x);
    plt.plot(t, i, label='L = %f.2'%x);



plt.title("JoSIM DSFQ Loop Inductance Variation Curve")
plt.xlabel("Time")
plt.ylabel("Current")
plt.legend(loc='best')

y_fmt = tick.FormatStrFormatter('%2.2e')
ax.yaxis.set_major_formatter(y_fmt)
plt.grid(True)
plt.show()