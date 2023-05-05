import re

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

    # Extract the name of the subckt
    if match:
        name = match.group(1)
        # print("NAME OF SUBCKT: " + name)
    else:
        print('ERROR - check subcircuit titles and names')

    #Extract SUBCKT NODES



    # .PARAM Line Editing
    lines = content.split("\n")
    processed_lines = []
    for line in lines:
        if line.startswith(".param"):
            # print("Replace and Append:" ,name)
            # Remove extra whitespaces
            line = re.sub(r'\s+', ' ', line).strip()
            # Split into two parts
            name1, namex = re.split(r'\s*=\s*', line)
            # Replace NAME1 with NAME1_cake
            name1_cake = name1 + "_" + name
            # Replace words in NAMEX with words_cake
            namex = re.sub(r'\b([a-zA-Z]+(?:\d+)?)\b', r'\1_'+name, namex)
            # Combine and add to processed_lines
            processed_line = f"{name1_cake} = {namex}"
            processed_lines.append(processed_line)
        else:
            processed_lines.append(line)
    content = "\n".join(processed_lines)



    # Replace node names
    node_pattern = re.compile(r'^(?![xX])([BLRIV]\w*)\s+(\w+)\s+(\w+)\s+(.*)$', re.MULTILINE)
    for match in node_pattern.finditer(content):
        old_name, value1, value2, rest = match.groups()
        new_name = f"{old_name}_{name}"
        content = content.replace(f"{old_name} {value1} {value2}", f"{new_name} {value1}_{name} {value2}_{name}") + rest
    #FIRST RENAME HERE
    node_pattern = re.compile(r'^(?![xX])([a-zA-Z]\w*)\s+(\S+)\s+(\S+)\s+(.*)$', re.MULTILINE)
    content = node_pattern.sub(rf'\1_{name} \2_{name} \3_{name} \4', content)
  

    lines = content.split("\n")
    output = ""
    for line in lines:
        match = re.match(r"^(\w+\d+\w*)\s+(\S+)\s+(\S+)\s+(\S+)$", line)
        if match:
            if not re.match(r"^\d", match.group(4)):
                output += f"{match.group(1)} {match.group(2)} {match.group(3)} {match.group(4).rstrip()}_{name}\n"
            else:
                output += line + "\n"
        else:
            output += line + "\n"
    content = output

    #FIX =area issue. This is a hacky solution, but it works.
    regex = r'^(\S+\s+){4}(area=\S+)(\s+\S+)*$'
    modified_lines = []
    for i, line in enumerate(content.splitlines()):
        match = re.match(regex, line)
        if match:
            fifth_word = match.group(2)
            if fifth_word.startswith('area='):
                line = line.replace(fifth_word, fifth_word + "_" + name)
        modified_lines.append(line)
    content = "\n".join(modified_lines)

    #Fix PWL Error:
    modified_lines = []
    for line in content.splitlines():
        line = re.sub(r'(?<=\s)(\w+)\)', rf'\1_{name})', line)
        modified_lines.append(line)
    content = "\n".join(modified_lines)




    # Exception for nodes that are '0'
    content = re.sub(rf'(?<!\S)0_{name}(?!\S)', '0', content)

    #Spit out the modified name:
    # name = name + "_" + topname

    return content,name

    #Exception for nodes that are part of the subckt name

def replace_xsubcircuits(content,names_list,childname):
    # print(names_list)
    print(content)
    node_list = []
    lines = content.splitlines()
    def findsubcktname(name,lines):
        order_node_names = []
        for i in range(0, len(names_list), 1):
            if names_list[i].startswith(name):
                tail = names_list[i]
                # print("TAIL: ", tail)
                break
        #This is to allow for the lowest nest of nested subckts.
        if len(names_list) == 1:
             for i, line in enumerate(lines):
                if line.startswith('.subckt ' + name):
                    elements = line.strip().split()
                    order_node_names = elements[2:]
                    for i, node in enumerate(order_node_names):
                        order_node_names[i] += "_" + tail
                    break
        else:
             for i, line in enumerate(lines):
                if line.startswith('*.subckt ' + name):
                    elements = line.strip().split()
                    order_node_names = elements[2:]
                    for i, node in enumerate(order_node_names):
                        order_node_names[i] += "_" + tail
                    break


        # for i, line in enumerate(lines):
        #     if line.startswith('*.subckt ' + name):
        #         elements = line.strip().split()
        #         print(elements)
        #         order_node_names = elements[2:]
        #         print(order_node_names)

        #         for i, node in enumerate(order_node_names):
        #             order_node_names[i] += "_" + tail
        #         break
        return order_node_names
    
    subckt_nodes = []
    nodeloc =[]
    xmaster_nodes = []

    #FIND THE NODES OF MOTHER SUBCKT
    for i, line in enumerate(content.splitlines()):
        if line.startswith("x") and childname in line: #The three here should be childname.
            # extract the name and nodes
            subckt = line.split()
            name = subckt[1]
            xmaster_nodes.extend(subckt[2:])
            subckt_nodes = xmaster_nodes
            print(xmaster_nodes)

            #Write code to extract subckt oupa hannes andsave it to xmaster_nodes.
            

    insidenodes = xmaster_nodes.copy()

    
    


    # step 1 find the position of subckt nodes before they are renamed.
  
    for i, line in enumerate(content.splitlines()):
        if subckt_nodes and i>0:  # SKIP THE FIRST LINE
            # search for the nodes in the current line
            # print(line)
            for j, word in enumerate(line.split()):
                if word in subckt_nodes:
                    subckt_nodes.remove(word)
                    print(f"{word} found at line {i+1}, word {j+1}")
                    nodeloc.append([i+1,j+1])
                    if not subckt_nodes:  # if all nodes have been found
                        break
    

                    
    # Step 1 & 2: Scan through content and extract node names
    for k, line in enumerate(lines):
        if line.startswith('x'):
            elements = line.strip().split()
            nodes = elements[2:]  # Exclude the '.subckt' and 'NAME' elements
            xname = elements[1]
            node_list.append(nodes)
    
            #This returns the nodes we need to rename in a list in order.
            #EG: [node1 node2 node3]
            # print("\n\n\nxname", xname)
            # print("lines", lines)
            nodenames = findsubcktname(xname,lines)
            # print("Nodes",     nodes)
            # print("Node Names",     nodenames)

            #This code does the actual replacing.
            #scan through whole file, and replace node_nam
            #comment out xlines
            for i, node in enumerate(nodes): 
                nodes[i] = nodenames[i]

            for j in range(2, len(elements), 1):
                elements[j] = nodes[j-2]

            lines[k] = ' '.join(elements)

            #Search through file to find the subcircuit name
    content = '\n'.join(lines)

    # Step 3: Link master node names with inductors with values of 0L

    # initialize connect_nodes
   
    connect_nodes = []
    print(nodeloc)
    for loc in nodeloc:
        line_num = loc[0] - 1  # adjust for zero-based indexing
        word_num = loc[1] - 1  # adjust for zero-based indexing
        # print(line_num, word_num)
        line = content.splitlines()[line_num]
        words = line.split()
        if word_num < len(words):
            connect_nodes.append(words[word_num])

    # print the resulting list


    def connectnames(master_nodes, connect_nodes, content):
        # create the new lines
        # print("**************")
        # print(master_nodes)
        # print(connect_nodes)
        # print("**************")
        new_lines = [f"l_connect_{n} {master_nodes[n]} {connect_nodes[n]} 0\n" for n in range(len(master_nodes))]
        # print("\n New Lines: \n", new_lines)
        content_lines = content.split('\n')
        content_lines[1:1] = new_lines
        return '\n'.join(content_lines)
    
    content = connectnames(insidenodes,connect_nodes,content)
    return content


def extract_subcircuits(file_path):
    # Open the file for reading.
    with open(file_path, 'r') as f:
        content = [line.lower() for line in f.readlines()]
        # Initialize variables.
 
        linenumber = 0
        names_list = []
        sslist = []
        lssln = []
        # newmother = "plain"
        # name = "plain"
        for line in content: #Get Subckt lines
            # Check if we've entered a subckt.
            linenumber += 1
            if line.startswith('.subckt'):
                subckt_name = line.split()[1]
                
                lssln.append(linenumber)

                #cutoff the text and make a new text string file line
            
            if line.startswith('.ends'):
                # we know now that we have a subckt starting at lssln and anding at linenumber.
                #extract it:
                sssart = lssln.pop()
                linesx = content[sssart-1:linenumber]
                extracted_text = ''.join(linesx)
                
                sslist.append(extracted_text)



        print("Number of Sub-Circuits: ", len(sslist))

        def check_nest (mother):
             mlines = mother.splitlines()
             count=0
             for line in mlines:
                if line.startswith('.subckt'):
                    count += 1      
             if count > 1:
                return True
             else:
                 return False
             

        def update_nests(mother,child):
            #Problems: Adds 0 to ends
            #Adds an extra _three to the end of subsubckts
            def updateChild(child):
                newchild, newname = rename_parameters(child)
          
                #Replace .subckt with *.subckt and .ends with *.ends
                newchild = re.sub(r'(?<!\*)\.subckt', '*.subckt', newchild)
                newchild = re.sub(r'(?<!\*)\.ends', '*.ends', newchild)
                
                return newchild, newname

            def modifyMother(mother,child, childname):
                #Merge the modified child with the mother into one subckt.
                mother = '\n'.join(mother)
                child = '\n'.join(child)

                pattern = r"\.subckt " + childname + r"(.*?)\.ends"

                match = re.search(pattern, mother, re.DOTALL)

                # Replace the matched section with the text from A
                if match:
                    mother = mother[:match.start()] + child.strip() + mother[match.end():]
                else:
                    print("ERROR MOTHER NOT UPDATED ")
  
                # print(mother)
                return mother
            
            
            #Update Child
            # print("\n\nCHILD: ", child)
            # print("\n\nCHILD: ", child)
      
            child, childname = updateChild(child)
           
            child_lines = child.splitlines()
           
            #Replace child inside mother with modified child.
            lines = mother.splitlines()
            newmother = modifyMother(lines,child_lines, childname)
            return newmother, childname

      

        

        #CHECK IF THE CIRCUIT CONTAINS NESTED SUBCIRCUITS

        snames = []
        # nestwrite = []
        # for i in range(0, len(sslist)-1, 1): #EDIT ALL except the MASTER SUBCKT
        #     #STEP 1: Check if there are any nested subckts,
        #     #also get the names of all the subcircuits in the circuit.
        #     empty, sxnames = rename_parameters(sslist[i])
        #     snames.append(sxnames)
        #     if check_nest(sslist[i]):
        #         nestwrite.append(i) #Tells us where nest starts.
        # print(nestwrite)


        #STEP 2: If there are nested subckts, we need to update the names of the subcktsprint
        Cflag = False
        for i in range(0, len(sslist)-1, 1):
            
            if check_nest(sslist[i+1]): #AM I PART OF A NEST
                if not check_nest(sslist[i]):
                    if i != len(sslist)-2:
                        # print("I ", i)
                        # print(len(sslist)-3)
                        print("C")
                        nn = i
                        empty, childname = rename_parameters(sslist[i])
                        names_list.append(childname)
                        # print("C Child: ", childname)
                        
                        Cflag = True #The last element was a "C"
            
                        continue
                    else:
                        print("X")
                        sslist[i], name = rename_parameters(sslist[i])
                        names_list.append(name)
                    # print(snames[i])

            if not check_nest(sslist[i+1]):
                if not check_nest(sslist[i]):
                    # print("X")
                    sslist[i], name = rename_parameters(sslist[i])
                    names_list.append(name)
            
            if not check_nest(sslist[i+1]):
                if  check_nest(sslist[i]):
                    print("W_final")
            
                    if Cflag:
                        #The Last Element was the bottom of the nest. Get it's childname and feed into replace_xsubcircuits
                        childname = names_list.copy()
                        start_childname = childname.pop()

                        sslist[i] = replace_xsubcircuits(sslist[i], names_list,start_childname)
                        updated_mother, childname = update_nests(sslist[i],sslist[i-1])
                        empty, momname = rename_parameters(sslist[i])
                        names_list = names_list[:nn] + [item + "_" + momname for item in names_list[nn:]]
                        names_list.append(momname)
                        sslist[i] = updated_mother
                        Cflag = False

                    else:
                        
                        updated_mother, childname = update_nests(sslist[i],sslist[i-1])
                        # print(updated_mother)
                        print("\n***********************************\n")
                        empty, momname = rename_parameters(sslist[i])
                        names_list = names_list[:nn] + [item + "_" + momname for item in names_list[nn:]]
                        names_list.append(momname)
                        # print(print(sslist[2]))
                        sslist[i] = updated_mother
                        
                        sslist[i] = replace_xsubcircuits(sslist[i], names_list,childname)    
                    
                                
                    # #Check if the last element was a "C"
                    # if Cflag:
                    #     childname = names_list
                    #     start_childname = childname.pop()
                    # updated_mother, childname = update_nests(sslist[i],sslist[i-1])
                    # empty, momname = rename_parameters(sslist[i])
                    
                    # names_list = names_list[:nn] + [item + "_" + momname for item in names_list[nn:]]
                    # names_list.append(momname)

                    # print("SSLIST I *****************")
                    # print(sslist[i])
                    # print("SSLIST I *****************")

                    # sslist[i] = updated_mother
            
                    # #This step adds connectors to connect original XNAME to .subckt XNAME
                    
                    # if Cflag:
                    #     print("CHILD TRUE NAME IS: ", start_childname)
                    #     Cflag = False
                    #     sslist[i] = replace_xsubcircuits(sslist[i], names_list,start_childname)
                    # else:
                    #     print("CHILD NAME IS: ", childname)
                    #     sslist[i] = replace_xsubcircuits(sslist[i], names_list,childname)
                    # # print(sslist[i])





            if  check_nest(sslist[i+1]): #AM I PART OF A NEST
                if  check_nest(sslist[i]):
                    print("Wmid")
                    

                    if Cflag:
                        #The Last Element was the bottom of the nest. Get it's childname and feed into replace_xsubcircuits
                        childname = names_list.copy()
                        start_childname = childname.pop()

                        sslist[i] = replace_xsubcircuits(sslist[i], names_list,start_childname)
                        updated_mother, childname = update_nests(sslist[i],sslist[i-1])
                        empty, momname = rename_parameters(sslist[i])

                        names_list = names_list[:nn] + [item + "_" + momname for item in names_list[nn:]]

                        names_list.append(momname)
                        sslist[i] = updated_mother
                        Cflag = False

                    else:
                        # print("CHILD TRUE NAME IS: ", start_childname)

                        updated_mother, childname = update_nests(sslist[i],sslist[i-1])
                        empty, momname = rename_parameters(sslist[i])
                        names_list = names_list[:nn] + [item + "_" + momname for item in names_list[nn:]]
                        names_list.append(momname)
                        sslist[i] = updated_mother
                        sslist[i] = replace_xsubcircuits(sslist[i], names_list,childname)                        


            
            




        # for i in nestwrite:
          
            
        #     nestend = i
        #     sslist[nestend], endname = rename_parameters(sslist[nestend])
        #     names_list = [item + "_" + endname for item in names_list]
        


        
        if len(sslist) == 2:
                names_list = []
                sslist[0], cname = rename_parameters(sslist[0])
                names_list.append(cname)

  
        #This part does a final edit of the MASTER subckt.
        for i in range(0, len(sslist), 1):   

            #Replace all circuits into the master subckt
            master_subckt = sslist[len(sslist)-1]
            lines = master_subckt.splitlines()
            child_lines = sslist[i].splitlines()
            name_pattern = re.compile(r'^\.subckt\s+(\w+)\s+.*$', re.MULTILINE)
            match = name_pattern.search(sslist[i])
            if match:
                name = match.group(1)
                

                title_line = next(line for line in child_lines if line.startswith(".subckt " + name))
                
                start_line = next(i for i, line in enumerate(lines) if line.startswith(title_line))
                end_line = next(i for i, line in enumerate(lines[start_line:], start_line) if line.startswith(".ends"))
                lines = lines[:start_line] + lines[end_line+2:]
                lines = lines[:start_line] + child_lines + lines[start_line:]

                sslist[len(sslist)-1] = '\n'.join(lines)
                
                # print(sslist[len(sslist)-1])
                
            else:
                name = "ERROR"


            

        #STEP 3 - Append the mother subckt name to everything
       
        #THIS LINE STILL GIVES PROBLEMS ABOUT DOUBLE MSATERING CERTAIN LINES./
        # master_subckt, cname = rename_parameters(master_subckt)

        #ADD ALPHA TO EVERY SIGNLE NAME:

        # for name in range(0,len(names_list),1):
        #     names_list[name] = names_list[name] + "_" + cname

        # Add asterisks to subckt and ends lines
        master_subckt = re.sub(r'(?<!\*)\.subckt', '*.subckt', master_subckt)
        master_subckt = re.sub(r'(?<!\*)\.ends', '*.ends', master_subckt)
    f.close()
    return master_subckt,names_list

def integrate_subcircuits(file_path, file_out, content):
        with open(file_path, 'r') as f:
            original = f.read()
        f.close()
        with open(file_out, 'w') as f:
        
            f.write(original)
            f.write('\n\n******* INCLUDED FILES *******\n\n\n')
            f.write(content)
        f.close()



with open('rec.cir', 'r') as f:
    content = f.read()
    if (content is None):
        print("File is empty")
subcircuits, names_list = extract_subcircuits('rec.cir')
# print(replaced)

with open('rec_out.cir', 'w') as f:
    f.write(subcircuits)
    print("\nSucessfully written to file")
f.close()

integrate_subcircuits('testbench.cir', 'testbench_final.cir', subcircuits)





