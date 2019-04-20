import sys

disk_data = dict()

file_name = sys.argv[1]

out = open("2018201008_2.txt", "w")

data = dict()

transactions = list()
first_line = True
with open(file_name) as f:
    for line in f:
        line = line.strip()
        if line != "":
            if first_line:
                first_line = False
                data_split = line.split(' ')
                curr_var = None
                for i in range(0,len(data_split)):
                    if i%2 == 0:
                        curr_var = data_split[i]
                    else:
                        data[curr_var] = data_split[i]
            else:
                transactions.append(line)

transaction_complete = dict()
transaction_wise_writes = dict()
transaction_wise_items = dict()

def process_action(action):
    action = action.replace("<","")
    action = action.replace(">","")
    if "START" in action:
        if "CKPT" not in action:
            lex = action.split(' ')
            lex = [x.strip() for x in lex]
            transaction_complete[lex[1]] = False
            transaction_wise_writes[lex[1]] = list()
            transaction_wise_items[lex[1]] = list()

    elif "COMMIT" in action:
        lex = action.split(' ')
        lex = [x.strip() for x in lex]
        transaction_complete[lex[1]] = True
        for t in transaction_wise_writes:
            for w in transaction_wise_writes[t]:
                for i in transaction_wise_items[lex[1]]:
                    if w['item'] == i:
                        w['status'] = 'SAFE'
    
    else:
        lex = action.split(',')
        lex = [x.strip() for x in lex]
        temp = dict()
        temp['action'] = action
        temp['item'] = lex[1]
        temp['status'] = 'UNSAFE'
        temp['value'] = int(lex[2])
        transaction_wise_writes[lex[0]].append(temp)
        transaction_wise_items[lex[0]].append(lex[1])

for t in transactions:
    process_action(t)

for t in transaction_wise_writes:
    for a in transaction_wise_writes[t]:
        if a['status'] == 'UNSAFE':
            data[a['item']] = a['value']

print_str = ''
for c in range(65,91):
    if chr(c) in data:
        print_str += chr(c)+' '+str(data[chr(c)])+' '
out.write(print_str)
out.close()
