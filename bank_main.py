import json
import logging
import Branch
import Customer
import consts
import logger
import copy
def read_input_to_dict(filename):
    '''
    Reads the input file return a python dict.
    '''
    with open(filename) as file:
        return json.load(file)
    
def parse_input_tolists(filename):
    '''
    Parses the file returns customer, branch lists with customer and branch objects
    '''
    input_dict = read_input_to_dict(filename)
    customer_list, branch_list = [], []
    for obj in input_dict:
        if obj['type'] == 'customer': 
            customer_list.append(obj)
        elif obj['type'] == 'branch':
            branch_list.append(obj)
        else:
            logging.error("Invalid objects in input file")
    return customer_list, branch_list

def list_to_file(op_list, fname):
    with open(fname, 'w') as file:
        #for objs in op_list:
        #print(type(objs))
        json.dump(op_list, file, indent=4)
        #file.write('\n')

def generate_output_files():
    '''
    Parses the temp file and creats final outputs
    '''
    events=[]
    events_out, cust_out, branch_out = [], [], []
    with open(consts.OUTPUT_FILE_temp, 'r') as file:
        for line in file:
            events.append(json.loads(line))
    for event in events:
        added = False
        events_out.append(copy.deepcopy(event))
        if event['type'] == 'customer':
            for obj in cust_out:
                if obj['id'] == event['id']:
                    event.pop('type')
                    event.pop('id')
                    obj['events'].append(event)
                    added = True
                    break
            if not added:
                obj = {}
                obj['id'] = event['id']
                obj['type'] = 'customer'
                event.pop('type')
                event.pop('id')
                obj['events'] = [event]
                cust_out.append(obj)
                
        elif event['type'] == 'branch':
            for obj in branch_out:
                if obj['id'] == event['id']:
                    event.pop('type')
                    event.pop('id')
                    obj['events'].append(event)
                    added = True
                    break
            if not added:
                obj = {}
                obj['id'] = event['id']
                obj['type'] = 'branch'
                event.pop('type')
                event.pop('id')
                obj['events'] = [event]
                branch_out.append(obj)
        
        

    #print(cust_out)
    #print(branch_out)
    #print(events_out)

    list_to_file(cust_out, consts.OUTPUT_FILE_customer)
    list_to_file(branch_out, consts.OUTPUT_FILE_branch)
    list_to_file(events_out, consts.OUTPUT_FILE_events)
    
    with open(consts.OUTPUT_FILE_temp, 'w'):
    	pass
        

if __name__ == "__main__":
    customer_list, branch_list = parse_input_tolists(consts.INPUT_FILE)
    #Initiating branch processes
    # print(customer_list, '\n', branch_list)
    print("Creating branch processes...")
    Branch.initialize_branch_processes(branch_list)
    #Initiating customer processes
    print("\nCreating customer processes...")
    print("\nExecuting customer processes...")
    Customer.initialize_customer_processes(customer_list)
    #Initiating process termination
    # logger.writelog()
    print("\nTerminating all processes...")
    Branch.terminate_branch_processes()
    #Create output file
    # generate_output_files()
    print("\nOutput written to output.json")
    # logger.writelog()
    
