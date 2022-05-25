#!/usr/bin/env python
# Import relevant packages
import argparse
import numpy as np
from cgi import print_arguments
from collections import Counter
from lib2to3.pgen2.token import EQUAL

# Main function
def main():
  # Version info
  vers = "Sandle - A 2-input test pattern generator for JoSim v 1.0"

  # Initiate the parser
  parser = argparse.ArgumentParser(description=vers)

  # Add possible parser arguments
  parser.add_argument("-n", help="Number of Input Sources")
  parser.add_argument("-t", help="Time Between Inputs")
  parser.add_argument("-o", "--output", help="output file, should be .txt")
  parser.add_argument("-V", "--version", action='version', help="show script version", version=vers)

  # Read arguments from the command line
  args = parser.parse_args()
  numInputs = args.n
  restTime = int(args.t,base=10)


  name = 0
 

  binList = np.zeros((16))
  for a in range(0,16):
    binList[a] = a


  Matrixx = np.zeros((2,4))
  GEK = np.zeros((2,4,16))

  print(GEK)

  #Create Binary profiles for numbers
  for name in range(2):
    for ID in range(4):
      Matrixx[name,ID] = 0b0001<<ID

      for a in range(0,16):
        bi = int(binList[a])

        bi2 = int(Matrixx[name,ID])
        meep = (bi & bi2)

        if (meep > 0): meep = 1
        #print (meep)
        GEK[name,ID,a] = meep
       



 
  def generateText (Letter,name, bits, timestartinc, pattern):


   timeOUT = ""
    

    
   for ID in range(bits):
      #cycle through every GEK value, A and B side, starting with A

      
      timeblob = ""
      node = "I_" + Letter + str(ID)
      timeinc = timestartinc
      for a in range(0,16):
        if(pattern[name,ID,a] ==0):
          timeinc = timeinc + 1
        if(pattern[name,ID,a] ==1):
          #print("Pass")
          timeratio = int(restTime) / 100
          timeblock = int(timeratio * float(timeinc)*100)
          timeinc = timeinc + 1

          timeblob = timeblob + str(timeblock) + "p " +"0 " + str(timeblock + 3) + "p " + "cval " + str(timeblock + 5) + "p " + "0 "
            
      timeOUT = timeOUT + node + " 0 " + node + " pwl(0 0 " + timeblob + ")" + '\n'

   return timeOUT,timeinc



  OUTA1, startinco = generateText("A", 0 ,4, 0, GEK)
  OUTA2, startinc = generateText("A",  0, 4, startinco,GEK)
  OUTB2, startinc = generateText("B",  1, 4, startinco,GEK)

  print (OUTA1)
  print (OUTA2)
  print (OUTB2)








        





 
  #template = "I_a 0 1000 pwl(0 0 100p 0 103p cval 105p 0)"








if __name__ == '__main__':
  main()
