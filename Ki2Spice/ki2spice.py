#!/usr/bin/env python
# Import relevant packages
import argparse
from cgi import print_arguments
from collections import Counter
from lib2to3.pgen2.token import EQUAL

# Main function
def main():
  # Version info
  vers = "KiCad to JoSim's SPICE Syntax Translator, version 1.0"

  # Initiate the parser
  parser = argparse.ArgumentParser(description=vers)

  # Add possible parser arguments
  parser.add_argument("input", help="Typical Use-  Ki2Spice.py FILE.cir")
  #parser.add_argument("-o", "--output", help="the output file name with supported extensions: png, jpeg, webp, svg, eps, pdf")
  #parser.add_argument("-V", "--version", action='version', help="show script version", version=vers)

  # Read arguments from the command line
  args = parser.parse_args()

  # List of possible output formats
  outformats = [".cir"]
  f = open(args.input)
  netlist = f.read()
  f.close()

  text = netlist
    #cleaning
  text = text.lower()
  words = text.split()
  words = [word.strip('.,!;()[]') for word in words]
  words = [word.replace("'s", '') for word in words]

  #finding unique
  unique = []
  for word in words:
    if word not in unique:
         unique.append(word)
  unique.sort()
  #counting unique words
  num_unique =[len(unique)]
  cnt = Counter()
  for word in words:
    cnt[word] +=1

  #Doing some manual tidyup before we begin

  netlist = netlist.replace("GND", "0")
  netlist = netlist.replace("Inductor", "")
  netlist = netlist.replace("Resistor", "")
  netlistlow = str.lower(netlist)
  node = 0


  #If anything appears more than once (exception of jjmit) then assign a number for a node
  for wordx in unique:
    if cnt[wordx] > 1 and ((wordx != 'jjmit') and (wordx != 'ref') and (wordx != 'pwl(0')):
        search_text   = wordx
        replace_text = str(node)

        node+=1
        netlistlow = netlistlow.replace(search_text, replace_text)
        #print(f"Replaced {wordx} with {replace_text}")
  netlistout = netlistlow.replace(".title kicad schematic", "* Back Annotated .cir file from KiCad")

  #Split each line 
  splot = netlistout.splitlines( )
  splot.sort()
  lines = len(splot)
  paramlist = ""
  currentcount = 1

  for x in range (lines):
    if splot[x].split()[0] != "*" and splot[x].split()[0] != ".end":
      
      #Setup list of parameters, and add nice tabs and spacing
      paramlist = paramlist + ".param \t" + splot[x].split()[0] + "  \t= \n"
      splot[x] = splot[x].replace(" ", "   \t")
      splot[x] = splot[x] + " " + splot[x].split()[0]
    
      #add area for JJ's
      if 'jjmit' in splot[x]:
        splot[x] = splot[x].replace("jjmit ", " jjmit area=")

      #prevent odd behavior from current sources
      if ("ref) "+ 'i'+ str(currentcount)) in splot[x]:

        splot[x] = splot[x].replace(("ref) "+ 'i'+ str(currentcount)), 'i' + str(currentcount) + ')') 
        currentcount+=1



  #Move '.end' to the end
  splot.append(splot.pop(splot.index(".end")))

  #Join '.param' and the rest
  netlistout = "\n".join(splot)
  netlistout = paramlist + "\n\n" + netlistout
  





  file = open('translated_' + args.input, 'w')
  file.write(netlistout)
  file.close()

  print("File Written Sucessfully!")

  #print(netlistout)

if __name__ == '__main__':
  main()
