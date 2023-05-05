import re





def replace_node_and_element_names(content, subckt_name):


    # Compile regex patterns
    element_pattern = re.compile(r'(\S+)\s+(\S+)\s+(\S+)\s+([\w\.]+)')
    node_pattern = re.compile(r'(\S+)')

    # Replace circuit element names and nodes
    def replace_element(match):
        element_name, node1, node2, value = match.groups()
        if node1 != '0':
            node1 = f"{node1}_{subckt_name}"
        if node2 != '0':
            node2 = f"{node2}_{subckt_name}"
        new_name = f"{element_name}_{subckt_name}"
        return f"{new_name} {node1} {node2} {value}"

    def replace_node(match):
        node_name = match.group(1)
        if node_name == 'jjmit' or node_name.startswith('area=') or node_name.startswith('pwl(') or node_name == '0' or node_name[-1].isdigit():
            return node_name
        else:
            return f"{node_name}_{subckt_name}"

    content = element_pattern.sub(replace_element, content)
    content = node_pattern.sub(replace_node, content)
    print(content)
    return content




def rename_nodes(input_file):
    # Load file contents
    with open(input_file, 'r') as f:
        content = f.read()

    # Compile regex patterns
    subckt_pattern = re.compile(r'\.subckt\s+(\S+)')
    element_pattern = re.compile(r'(\S+)\s+(\S+)\s+(\S+)\s+([\w\.]+)')

    # Find subckt names
    subckt_names = subckt_pattern.findall(content)
    print(subckt_names)
    # Loop over subckt names

    for subckt_name in subckt_names:

        # Replace parameter names
        param_pattern = re.compile(r'\.param\s+([^\n]+)')
        def replace_param(match):
            param_name, param_value = match.group(1).split('=')
            param_name = f"{param_name}_{subckt_name}"
            new_param = f"{param_name}={param_value}"
            return f".param {new_param}"
        # print(param_pattern.sub(replace_param, content))
        content = param_pattern.sub(replace_param, content)
        
        element_edits = replace_node_and_element_names(content, subckt_name)
        print(element_edits)
        # Replace circuit element names and nodes

    

    # Add asterisks to subckt and ends lines
    content = re.sub(r'\.subckt', '*.subckt', content)
    content = re.sub(r'\.ends', '*.ends', content)


    # print(content)
    return content







def main():
    input_file = 'expanded_testbench.cir'
    # output_file = 'expanded_testbench.cir'

    renamed_content = rename_nodes(input_file)

    with open("output.cir", 'w') as f:
        f.write(renamed_content)


if __name__ == '__main__':
    main()
