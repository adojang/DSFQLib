# Adriaan van Wijk 2022
#
#
#
# This file does some simple text manipulation


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
  vers = "Toothrbush - Output Test pattern manipulation for JoSim v 1.1"

  # Initiate the parser
  parser = argparse.ArgumentParser(description=vers)

  # Add possible parser arguments
  parser.add_argument("-V", "--version", action='version', help="show script version", version=vers)
  parser.add_argument("-sp", dest='spout', help="Typical Use-  Sandle.py ATALANTA_VECTOR.cir")
  parser.add_argument("-p", dest='pattern', help="Typical Use-  Sandle.py ATALANTA_VECTOR.cir")


  # Read arguments from the command line
  args = parser.parse_args()

  # List of possible output formats
  #outformats = [".cir"]
  f1 = open(args.spout)
  sp_lines = f1.read()
  f1.close()
  f2 = open(args.pattern)
  p_lines = f2.read()
  f2.close()



  p_lines = p_lines.lower()
  p_lines = p_lines.splitlines()

  deleteflag = 0
  for x in range(len(p_lines)):
    if " 1:" in p_lines[x]:
      deleteflag = x

  print("Pattern Data:\n")
  for x in range(deleteflag-1):
    p_lines.pop(0)

  #p_lines.pop(0) #get rid of the two starting lines
  #p_lines.pop(0) #get rid of the two starting line
  #p_words = p_lines.split() #split into words

  p_string = ""
  for x in range(1,len(p_lines)): #number of lines
    
    print(p_lines[x])
    p_words = p_lines[x].split()
    #print(p_words)
    #print("WORDS", p_words)
    #print("LENGTH:", len(p_words))
    p_words.pop(0)
    p_words.pop(0)
    #print(p_words)
    p_string = p_string.join(p_words)
    #print(p_string)

    p_lines[x] = p_string
  
  p_lines.pop(0)
#  print(p_lines)
  p_output = p_lines

















  #SP Processing: ======================================================================

  print("SP Data:\n")
  sp_lines = sp_lines.lower()
  sp_lines = sp_lines.splitlines()
  sp_lines.pop(0) #get rid of the two starting lines
  sp_lines.pop(0) #get rid of the two starting lines
  
  #Initialize
  sp_backup = sp_lines
  sp_2 = sp_lines
  transport = ""


  for x in range(len(sp_lines)):
    words = ""
    newwords = ""
    sp_words = sp_lines[x].split() #Words in line X
    sp_words.pop(0) #pop the first word which is a time thing with e-12 in it typically. Now we only have usefull stuff left.
    
    
    words = words.join(sp_words) #convert list to STRING

   #Compare if an element in the string is equal to the last time it was called
    if(x > 0):
      w = words
      wprev = sp_backup[x-1].split()
      wprev.pop(0)


      w = list(w)
      wprev = list(wprev)
      print("Index: ", x)
      print(wprev)
      print(w)
      
      for a in range(len(w)):
        num_w = int(w[a], base=10)
        num_wprev = int(wprev[a], base=10)
        if(num_w == num_wprev):
            w[a] = "0"
        else:
            w[a] = "1"
      

      newwords = newwords.join(w)
      #sp_lines[x] = newwords
      transport = transport + newwords + "\n"

    else:
      #For the first time when x == 0 only
      #sp_lines[x] = words
      transport = transport + words + "\n"


    #sp_backup[x] = words
    #transport = transport + newwords + "\n"


  #remove random thing
  cake = ""
  print(cake.join(transport))
  sp_2 = transport.splitlines()
  #sp_2 = sp_lines

  # OUTPUT: sp_2
  sp_output = sp_2


# END SP PROCESSING ============================================













  print(sp_output)
  print(p_output)


  passrate = ""
  for x in range(len(sp_output)):
    if(sp_output[x] == p_output[x]):
      passrate = passrate + "PASS " + str(x) + "\n"
    else:
      passrate = passrate + "FAIL " + str(x) + "\n"

  print(passrate)



  #file = open('sandle_output', 'w')
  #file.write(output)
  #file.close()









if __name__ == '__main__':
  main()
