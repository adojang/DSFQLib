To use these, do an .include cells/abc_cell_name.cir

You may need to comment out include statements that are already present in certain cells like the 4bit adder, and AW_XOR gate.
Remember that .include simply includes the file and adds it as text to the netlist. Adding to identical libraries is a bad idea, and should be avoided.