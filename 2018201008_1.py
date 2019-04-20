import sys

disk_data = dict()
ram_data = dict()
temp_data = dict()
actions = dict()
file_name = sys.argv[1]
X = int(sys.argv[2])

first_line = True
n_a = 0
trans_name = ""
transactions = list()
total_lines = dict()
exec_lines = dict()
trans_start = dict()

out = open("2018201008_1.txt", "w")

with open(file_name) as f:
    for line in f:
        line = line.strip()
        if line != "":
            if first_line:
                first_line = False
                dd = line.split(" ")
                curr_char = ""
                for i in range(0,len(dd)):
                    if i%2==0:
                        curr_char = dd[i]
                    else:
                        disk_data[curr_char] = int(dd[i])
            else:
                if n_a == 0:
                    t = line.split(" ")
                    trans_name = t[0].strip()
                    transactions.append(trans_name)
                    actions[trans_name] = list()
                    n_a = int(t[1].strip())
                    total_lines[trans_name] = n_a
                    exec_lines[trans_name] = n_a
                    trans_start[trans_name] = True
                else:
                    actions[trans_name].append(line.strip())
                    n_a -= 1


def program_complete(exec_lines):
    for key in exec_lines:
        if exec_lines[key]!=0:
            return False
    return True

def execute_action(transaction, action):
    if "READ" in action:
        action = action.replace("READ","")
        action = action.replace("(","")
        action = action.replace(")","")
        lex = action.split(',')
        lex = [x.strip() for x in lex]
        temp_data[lex[1]] = disk_data[lex[0]]
        ram_data[lex[0]] = disk_data[lex[0]]
    elif "WRITE" in action:
        action = action.replace("WRITE","")
        action = action.replace("(","")
        action = action.replace(")","")
        lex = action.split(',')
        lex = [x.strip() for x in lex]
        prev_data = ram_data[lex[0]]
        ram_data[lex[0]] = temp_data[lex[1]]
        # print '<'+transaction +','+' '+lex[0]+','+' '+str(prev_data)+'>'
        out.write("<"+transaction +","+" "+lex[0]+","+" "+str(prev_data)+">\n") 
        if not ram_data:
            out.write("\n")
        else:
            print_str = ''
            # for key in ram_data:
            for c in range(65,91):
                if chr(c) in ram_data:
                    print_str += chr(c)+' '+str(ram_data[chr(c)])+' '
            out.write(print_str+'\n')
        if not disk_data:
            out.write("\n")
        else:
            print_str = ''
            # for key in disk_data:
            for c in range(65,91):
                if chr(c) in disk_data:
                    print_str +=  chr(c)+' '+str(disk_data[chr(c)])+' '
            out.write(print_str+'\n')
    elif "OUTPUT" in action:
        action = action.replace("OUTPUT","")
        action = action.replace("(","")
        action = action.replace(")","")
        action = action.strip()
        # if action in ram_data:
        #     print ram_data[action]
    else:
        lex = action.split(':=')
        target = lex[0].strip()
        action = lex[1].strip()
        if "+" in action:
            operands = action.split("+")
            try:
                a = int(operands[0].strip())
                b = int(operands[1].strip())
                temp_data[target] = a + b
            except ValueError:
                a = operands[0].strip()
                b = int(operands[1].strip())
                temp_data[target] = temp_data[a] + b
        elif "-" in action:
            operands = action.split("-")
            try:
                a = int(operands[0].strip())
                b = int(operands[1].strip())
                temp_data[target] = a - b
            except ValueError:
                a = operands[0].strip()
                b = int(operands[1].strip())
                temp_data[target] = temp_data[a] - b
        elif "*" in action:
            operands = action.split("*")
            try:
                a = int(operands[0].strip())
                b = int(operands[1].strip())
                temp_data[target] = a * b
            except ValueError:
                a = operands[0].strip()
                b = int(operands[1].strip())
                temp_data[target] = temp_data[a] * b
        elif "/" in action:
            operands = action.split("/")
            try:
                a = int(operands[0].strip())
                b = int(operands[1].strip())
                temp_data[target] = a / b
            except ValueError:
                a = operands[0].strip()
                b = int(operands[1].strip())
                temp_data[target] = temp_data[a] / b

while not program_complete(exec_lines):
    for t in transactions:
        if trans_start[t]:
            out.write("<START "+t+">\n")
            if not ram_data:
                out.write("\n")
            else:
                print_str = ''
                # for key in ram_data:
                for c in range(65,91):
                    if chr(c) in ram_data:
                        print_str += chr(c)+' '+str(ram_data[chr(c)])+' '
                out.write(print_str+'\n')
            if not disk_data:
                out.write("\n")
            else:
                print_str = ''
                # for key in disk_data:
                for c in range(65,91):
                    if chr(c) in disk_data:
                        print_str +=  chr(c)+' '+str(disk_data[chr(c)])+' '
                out.write(print_str+'\n')
            trans_start[t] = False
        for i in range(0,X):
            index = total_lines[t] - exec_lines[t]
            if index < len(actions[t]):
                action = actions[t][index]
                execute_action(t,action)
                exec_lines[t] -= 1
                if index == len(actions[t])-1:
                    out.write("<COMMIT "+t+">\n")
                    if not ram_data:
                        out.write("\n")
                    else:
                        print_str = ''
                        # for key in ram_data:
                        for c in range(65,91):
                            if chr(c) in ram_data:
                                print_str += chr(c)+' '+str(ram_data[chr(c)])+' '
                        out.write(print_str+'\n')
                    if not disk_data:
                        out.write("\n")
                    else:
                        print_str = ''
                        # for key in disk_data:
                        for c in range(65,91):
                            if chr(c) in disk_data:
                                print_str +=  chr(c)+' '+str(disk_data[chr(c)])+' '
                        out.write(print_str+'\n')

out.close()
