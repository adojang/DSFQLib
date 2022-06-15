# Adriaan van Wijk 2022
#
#
#
# This file expects the output of .vec from atalanta's auto test pattern generator.
#The inputs are expected to be organized into this pattern:

#Input A0
#Input A1 ...
#Input B0
#Input B1 ...
#Output C0 [This MUST be here or the script will fail.]
#...
#...
#END


#!/usr/bin/env python
# Import relevant packages
import argparse
import numpy as np
from cgi import print_arguments
from collections import Counter
from lib2to3.pgen2.token import EQUAL
import array as arr
# Main function
def main():
  # Version info
  vers = "Sandle - Input test pattern generator for JoSim v 1.1"

  # Initiate the parser
  parser = argparse.ArgumentParser(description=vers)

  # Add possible parser arguments
  parser.add_argument("-s", help="Time Offset in ps")
  parser.add_argument("-t", help="Time Between Inputs, in ps")
  parser.add_argument("-o", "--output", help="output file, should be .txt")
  parser.add_argument("-V", "--version", action='version', help="show script version", version=vers)
  parser.add_argument("-i", dest='inputfile', help="Typical Use-  Sandle.py ATALANTA_VECTOR.cir")



  # Read arguments from the command line
  args = parser.parse_args()

  # List of possible output formats
  #outformats = [".cir"]
  f = open(args.inputfile)
  netlist = f.read()
  f.close()

  time_offset = int(args.s,base=10)/100
  restTime = int(args.t,base=10)


  text = netlist
  #cleaning
  text = text.lower()
  words = text.split()
  #words = [word.strip('.,!;()[]') for word in words]
  #words = [word.replace("'s", '') for word in words]


  #counting the number of inputs
  num_inputs = (int)(len(words[0])) #-1 because Cout is one of the outputs
  num_gates = (num_inputs-1)/2

  #counting the number of lines
  num_lines = len(words) - 1 #-1 because the last line is END
 




  #Matrixx = np.zeros((num_gates,num_inputs))
  GEK = np.zeros((num_inputs,num_lines))


  for a in range(0,num_lines):
    st = words[a]
    #Create Binary profiles for numbers
    #for name in range(num_gates): #Grouping per logic gate, equivalent to 'how many variables until A changes into B'
    for ID in range(num_inputs): #The total number of actual input ports
      if (int(st[ID],base=10) == 1):
        GEK[ID,a] = 1
        
 

  #For GEK
  #Values is COLUMN | - ie, I1, I2, I3
  #Timeset is ROW ___ - ie, t1, t2, t3
 
  def generateText (start_time_offset, pattern):

   string_store = [""]
   master_string = ""
   timeOUT = ""
  
   #Initialize All as Empty
   for x in range(num_inputs-1): #-1 because element 0 already initialized.
     string_store.append("")
   #for ID in range(bits):
    #cycle through every GEK value, A and B side, starting with A

    
   
   timeblock = 0
   timeinc = start_time_offset
   for a in range(0,num_lines): #a is sort of like the TIMESTEP
    
    # Add an element to the array juice train



    timeinc = timeinc + 1
    for ID in range(num_inputs): #The total number of actual input ports
  # after namechange, change  to the other name.
  
      timeblob = ""

      if(pattern[ID,a] ==0):
        
        timeratio = int(restTime) / 100
        timeblock = int(timeratio * float(timeinc)*100)
        timeblob = timeblob + str(timeblock) + "p " +"0 " + str(timeblock + 3) + "p " + "0 " + str(timeblock + 5) + "p " + "0 "
      if(pattern[ID,a] ==1):
        #print("Pass TIME:", a)
        #print("ID: ", ID)
        timeratio = int(restTime) / 100
        timeblock = int(timeratio * float(timeinc)*100)

        timeblob = timeblob + str(timeblock) + "p " +"0 " + str(timeblock + 3) + "p " + "cval " + str(timeblock + 5) + "p " + "0 "
      string_store[ID] = string_store[ID] + timeblob
    
   cnt = 0

   #Naming Convention
   for ID in range(num_inputs):
   
    if (ID >= num_gates):
      Letter = "B"
    else:
      Letter = "A"

    if(ID == num_inputs-1):
      Letter = "Cin"

    node = "I_" + Letter + str(cnt)
    cnt = cnt + 1
    if (cnt == num_gates):
      cnt = 0


    #Include Cin








    master_string = master_string + node + " 0 " + node + " pwl(0 0 " + string_store[ID] + ")" + "\n"

   return master_string


#Here we assume that the input list is order such that the first half of 1234 - ie 1 and 2 are A inputs while 3 and 4 are B inputs. This logic is then applied to the long 00010000 input pattern. In the case of 00010000, B has no 1's.
#Take the number (8) divide by 2 = 4, therefore for 00010000 the '1' marks the end of the A segment. The num_gates can be used for the 8/2, although I'm not sure if this is robust for the future...

  output = generateText(time_offset,GEK)



  print (output)


  file = open('sandle_output', 'w')
  file.write(output)
  file.close()









if __name__ == '__main__':
  main()
