import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser(description='Expand all subcircuits in a Spice file')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input Spice file name')
    return parser.parse_args()

def parse_spice_file(filename):
    # Open the input Spice file
    with open(filename, 'r') as f:
        spice_text = f.read()

    # Find all subcircuits in the Spice file
    subckt_pattern = r'^\.subckt\s+(\S+)([\s\S]+?)^\.ends\s+(\S+)'
    subckt_matches = re.finditer(subckt_pattern, spice_text, re.MULTILINE)

    # For each subcircuit, replace the subcircuit call with the expanded subcircuit text
    for match in subckt_matches:
        subckt_name = match.group(1)
        subckt_text = match.group(2)
        expanded_text = expand_subckt(subckt_text, subckt_name)
        spice_text = spice_text.replace(match.group(0), expanded_text)

    # Write the output Spice file with all subcircuits expanded
    with open('expanded_' + filename, 'w') as f:
        f.write(spice_text)

def expand_subckt(subckt_text, subckt_name):
    # Find all subcircuit calls in the subcircuit text
    call_pattern = r'(\w+)\s+(\S+)(\s+\S+)*'
    call_matches = re.finditer(call_pattern, subckt_text)

    # For each subcircuit call, replace the call with the expanded subcircuit text
    for match in call_matches:
        call_name = match.group(1)
        call_params = match.group(2)
        call_params = re.sub(r'0(?=\s|\Z)', 'GND', call_params)
        subckt_instance = subckt_name + '_' + call_name
        expanded_text = expand_subckt(get_subckt_text(call_name), subckt_instance)
        subckt_text = subckt_text.replace(match.group(0), subckt_instance + ' ' + call_params + expanded_text)

    # Rename all components and nodes in the subcircuit text
    subckt_text = re.sub(r'(?<!\w)(\d+)(?!\w)', r'n\g<1>', subckt_text)
    subckt_text = re.sub(r'(?<!\w)([A-Za-z]+)(?!\w)', r'c_\g<1>', subckt_text)

    return subckt_text

def get_subckt_text(subckt_name):
    # Find the subcircuit definition with the given subcircuit name
    subckt_pattern = r'^\.subckt\s+' + subckt_name + r'([\s\S]+?)^\.ends'
    subckt_match = re.search(subckt_pattern, spice_text, re.MULTILINE)
    if subckt_match is None:
        raise ValueError('Subcircuit {} not found'.format(subckt_name))
    return subckt_match.group(1)

def main():
    args = parse_args()
    parse_spice_file(args.input)

if __name__ == '__main__':
    main()
