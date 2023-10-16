import json
import logging
import Branch
import Customer
import consts

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

if __name__ == "__main__":
    customer_list, branch_list = parse_input_tolists(consts.INPUT_FILE)
    #Initiating branch processes
    print("Creating branch processes...")
    Branch.initialize_branch_processes(branch_list)
    #Initiating customer processes
    print("\nCreating customer processes...")
    print("\nExecuting customer processes...")
    Customer.initialize_customer_processes(customer_list)
    #Initiating process termination
    print("\nTerminating all processes...")
    Branch.terminate_branch_processes()
    #Create output file
    print("\nOutput written to output.txt file")