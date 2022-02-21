// ---------------------------------------------------------------------------
// Verilog testbench file, created with TimEx v2.05
// Timing description and structural design for IARPA-BAA-14-03 via
// U.S. Air Force Research Laboratory contract FA8750-15-C-0203 and
// IARPA-BAA-16-03 via U.S. Army Research Office grant W911NF-17-1-0120.
// For questions about TimEx, contact CJ Fourie, coenrad@sun.ac.za
// (c) 2016-2018 Stellenbosch University
// ---------------------------------------------------------------------------
`timescale 1ps/100fs
module tb_DSFQ_AND;
   reg a = 0;
   reg b = 0;
   initial
      begin
         $dumpfile("tb_DSFQ_AND.vcd");
         $dumpvars;
         // Now in state 0
         #20 a = !a;
         // Now in state 0
         #10 b = !b;
         // Now in state 0
      end

   initial
      begin
         $display("\t\ttime,\ta,\tb,\tq");
         $monitor("%d,\t%b,\t%b,\t%b",$time,a,b,q);
      end

   DSFQ_AND DUT (a, b, q);

   initial
      #40 $finish;
endmodule
