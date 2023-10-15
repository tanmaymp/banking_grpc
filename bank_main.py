import json
import logging
import Branch
import Customer
import consts

def read_input_to_dict(filename):
    with open(filename) as file:
        return json.load(file)
    
def parse_input_tolists(filename):
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

def execute_customer_processes(id, events):
    cust_obj = cust_obj = Customer.Customer(id=id, events=events)
    output_obj = cust_obj.executeEvents()
    with open(consts.OUTPUT_FILE, 'a') as file:
        json.dump(output_obj, file)
        file.write('\n')

if __name__ == "__main__":
    customer_list, branch_list = parse_input_tolists(consts.INPUT_FILE)

    #Initiating branch processes
    print("Creating branch processes...")
    Branch.initialize_branch_processes(branch_list)
    #Initiating customer processes
    print("\nCreating customer processes...")
    print("\nExecuting customer processes...")
    Customer.initialize_customer_processes(customer_list)
    #Initiating server termination
    print("\nTerminating all processes...")
    Branch.terminate_branch_processes()
    #Create output file
    print("\nOutput written to output.txt file")