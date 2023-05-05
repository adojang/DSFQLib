import re

def process_text(text):
    lines = text.split("\n")
    processed_lines = []

    for line in lines:
        if line.startswith(".param"):
            # Remove extra whitespaces
            line = re.sub(r'\s+', ' ', line).strip()

            # Split into two parts
            name1, namex = re.split(r'\s*=\s*', line)

            # Replace NAME1 with NAME1_cake
            name1_cake = name1 + "_cake"

            # Replace words in NAMEX with words_cake
  
            namex = re.sub(r'\b([a-zA-Z]+(?:\d+)?)\b', r'\1_cake', namex)


            # words = re.findall(r'\b[a-zA-Z]+\b', namex)
            # for word in words:
            #     # print("Word:", word)
            #     namex = namex.replace(word, word + "_cake")

            # Combine and add to processed_lines
            processed_line = f"{name1_cake} = {namex}"
            processed_lines.append(processed_line)
        else:
            processed_lines.append(line)

    return "\n".join(processed_lines)

# Test
input_text = """.param LB=2p
.param BiasCoef=h55
.param ib2 = 87u
.param ib4 = biascoef*ic0*b4
.param lrb2 = (rb2/rsheet)*lsheet
random example text here

B1 1 2 jjmit area=B1
B2 4 5 jjmit area=B2
B3 7 8 jjmit area=B3
B4 13 14 jjmit area=B4
B5 17 18 jjmit area=B5
B6 10 11 jjmit area=B6
B7 20 18 jjmit area=B7
B8 18 19 jjmit area=B8
B9 21 22 jjmit area=B9

IB1 0 3 pwl(0 0 5p IB1)
IB2 0 6 pwl(0 0 5p IB2)
IB3 0 9 pwl(0 0 5p IB3)
IB4 0 15 pwl(0 0 5p IB4)
IB5 0 23 pwl(0 0 5p IB5)

LB1 3 1 LB1
LB2 6 4 LB2
LB3 8 9 LB3
"""

expected_output = """.param LB=2p
.param BiasCoef_cake=h55_cake
.param ib2_cake = 87u
.param ib4_cake = biascoef_cake*ic0_cake*b4_cake
.param lrb2_cake = (rb2_cake/rsheet_cake)*lsheet_cake
random example text here"""

output = process_text(input_text)
print(output)
# assert output == expected_output, f"Expected:\n{expected_output}\nGot:\n{output}"
# print("Test p?assed successfully.")
