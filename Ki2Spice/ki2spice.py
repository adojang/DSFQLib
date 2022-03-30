#!/usr/bin/env python
# Import relevant packages
import argparse
from collections import Counter

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
  node = 1
  #If anything appears more than once (exception of jjmit) then assign a number for a node
  for wordx in unique:
    if cnt[wordx] > 1 and (wordx != 'jjmit'):
        search_text   = wordx
        replace_text = str(node)
        node+=1
        netlistlow = netlistlow.replace(search_text, replace_text)
        #print(f"Replaced {wordx} with {replace_text}")
  netlistout = netlistlow.replace(".title kicad schematic", "* Back Annotated .cir file from KiCad")
  file = open('translated_' + 'args.input', 'w')
  file.write(netlistout)
  file.close()

  print("File Written Sucessfully!")

  #print(netnew)

if __name__ == '__main__':
  main()
