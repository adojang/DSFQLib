import re

def import_circuits(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    include_pattern = re.compile(r'\.include\s+(.+)')
    included_files = include_pattern.findall(content)
    #STAGE 1, Edit subckts
    names_list = []
    with open(output_file, 'w') as f:
        
        f.write(content)
        f.write('\n\n******* INCLUDED FILES *******\n')
        print("\nValid Subcircuits Found:\n")
        for include_file in included_files:
            #THIS LOOP IMPORTS EACH INCLUDED FILED.
            
            with open(include_file.strip(), 'r') as inc_f:
                f.write('\n')
                subckt_file = inc_f.read()
                #NOW WE HAVE A .SUBCKT FILE THAT IS READ
                #STEP 1, remove .model line.
                subckt_file = re.sub(r'^\.model\s+.*\n', '', subckt_file, flags=re.MULTILINE)
                #STEP 2 rename all parameters
                # print(subckt_file)
                edited_subckt, subcktname = rename_parameters(subckt_file)
                names_list.append(subcktname)

                #STEP 3 Write to file  
                f.write(edited_subckt)
    #remove .include lines

    #STAGE 2, Edit main file
    with open(output_file, 'r') as f:
        updated_content = f.read()
        #remove .include statements
        updated_content = re.sub(r'^\.include.*$', '', updated_content, flags=re.MULTILINE)

        updated_content = rename_nodes(updated_content,names_list)


    with open(output_file, 'w') as f:
        f.write(updated_content)
    f.close()

    return content, included_files


def rename_nodes(content, namelist):
 
# Compile regex pattern
    pattern = re.compile(r'^X(\S+)\s+(\S+)\s+(.*)$')

    # Find and print matching lines
    for line in content.split('\n'):
        match = pattern.match(line)
        if match and match.group(2) in namelist:

            #Add a * to the start of the line
            nodes = match.group(3).split()
            new_nodes = []
            for i in range(len(nodes)):
                new_nodes.append(nodes[i] + "_" + match.group(2))
            
           #REPLACE WORDS
            for nodes, new_nodes in zip(nodes, new_nodes):

                 content = content.replace(nodes, new_nodes)
        
            #comment out the line
            content = re.sub(r'^X(\S+)\s+(\S+)\s+(.*)$', r'*X\1 \2 \3', content, flags=re.MULTILINE)
           
        




    return content



def rename_parameters(content):
    #Get the circuit name:
    name_pattern = re.compile(r'^\.subckt\s+(\w+)\s+.*$', re.MULTILINE)
    match = name_pattern.search(content)

    # Extract the name from the match object
    if match:
        name = match.group(1)
        print(name)
    else:
        print('ERROR SUBCKT Name not found, please check your file')

    # Replace parameter names everywhere:

    name_map = {}
    for match in re.finditer(r'^\.param\s+(\w+)\s*=\s*([\w.+-]+)$', content, re.MULTILINE):
        old_name, value = match.groups()
        new_name = f"{old_name}_{name}"
        name_map[old_name] = new_name

    # Replace old names with new names
    for old_name, new_name in name_map.items():
        content = re.sub(rf'(?<!\w){old_name}(?!\w)', new_name, content)

    node_pattern = re.compile(r'^([a-zA-Z]\w*)\s+(\w+)\s+(\w+)\s+(.*)$', re.MULTILINE)
    # Find and replace nodes

    content = node_pattern.sub(rf'\1 \2_{name} \3_{name} \4', content)

    # Exception for nodes that are '0'
    content = re.sub(rf'(?<!\S)0_{name}(?!\S)', '0', content)

    # Add asterisks to subckt and ends lines
    content = re.sub(r'\.subckt', '*.subckt', content)
    content = re.sub(r'\.ends', '*.ends', content)
    return content,name



def main():
    input_file = 'testbench_old.cir'
    output_file = 'testbench.cir'

    import_circuits(input_file,output_file) #import all the .include circuits from the testbench.cir file


if __name__ == '__main__':
    main()
