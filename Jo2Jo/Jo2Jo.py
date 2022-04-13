#!/usr/bin/env python
# Import relevant packages
import argparse
from cgi import print_arguments
from collections import Counter
from lib2to3.pgen2.token import EQUAL

# Main function
def main():
  # Version info
  vers = "Jo2Jo Syntax Translator, version 1.0\nAdriaan van Wijk"

  # Initiate the parser
  parser = argparse.ArgumentParser(description=vers)

  # Add possible parser arguments
  parser.add_argument("-i", "--input", help="The .cir file for your deck")
  parser.add_argument("-m", "--mess",  help="The formatted mess output from Josim-tools")
  #parser.add_argument("-o", "--output", help="the output file name with supported extensions: png, jpeg, webp, svg, eps, pdf")
  #parser.add_argument("-V", "--version", action='version', help="show script version", version=vers)

  # Read arguments from the command line
  args = parser.parse_args()

  # List of possible output formats
  outformats = [".cir"]
  f = open(args.input)
  netlist = f.read()
  f.close()

  f = open(args.mess)
  mess = f.read()
  f.close()


  
  #cleaning netlist
  netlist = netlist.lower()
  #Split netlist into lines 
  netlist = netlist.splitlines()


#cleaning mess
  mess = mess.lower()
  words = mess.split()
  words = [word.strip('.,!;()[]') for word in words]
  words = [word.replace("'s", '') for word in words]

  #print (len(netlist))
  outlist = ""
  for x in range (len(netlist)):
    netlist[x] = netlist[x].replace(".param ", "")

    netlist[x] = netlist[x].replace("=", "={nominal=")

    #remove annoying last word
    netlist_words = netlist[x].split()
    
    rep = netlist_words[len(netlist_words)-1]
    netlist[x] = netlist[x].replace(rep," ")

    netlist[x] = netlist[x].replace("={nominal=", "=\t {nominal =")
    netlist[x] = netlist[x] + str(words[x]) + "}"

    outlist = outlist +'\n' + netlist[x]
    print(netlist[x])

  file = open('jo2jo_out.txt', 'w')
  file.write(outlist)
  file.close()

  print("File Written Sucessfully!")

 

if __name__ == '__main__':
  main()
