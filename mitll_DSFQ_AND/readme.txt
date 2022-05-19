DSFQ_AND Cell Notes

To run the file:
-Install JoSim (add it to PATH if on windows)
-Install python (must be added to PATH if on windows)
-Put a copy of josim-plot in the folder.

then copy and paste the following:

josim -o AW_mitll_AND_testbench.csv AW_mitll_AND_testbench.cir -V 1
josim-plot.py AW_mitll_AND_testbench.csv -t stacked

==========================================================================
==========================================================================


Version 1.5
The layout bias line was designed for an input voltage of 2.06mV instead of the standard 2.5mV due to an error.
This may be corrected in later versions