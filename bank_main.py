import json
import logging
from time import sleep
import Branch
import multiprocessing
import Customer

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
    print("Processing ", id, events)
    cust_obj = cust_obj = Customer.Customer(id=id, events=events)
    output_obj = cust_obj.executeEvents()
    with open("outputs/output.txt", 'a') as file:
        json.dump(output_obj, file)
        file.write('\n')

if __name__ == "__main__":
    customer_list, branch_list = parse_input_tolists('tests/dummy_input.json')

    print("Count of lists c ; {}, b : {}".format(customer_list, branch_list) )

    #Initiating branch processes
    branch_processes = []
    print("Creating branch processes")
    for branch in branch_list:
        branch_process = multiprocessing.Process(target=Branch.serve, args=(branch['id'], branch['balance']))
        branch_processes.append(branch_process)
        # print("Starting branch")
        branch_process.start()
    
    sleep(3)
    #Initiating customer processes
    
    print("\nCreating customer processes")
    
    for customers in customer_list:
        cust_process = multiprocessing.Process(target=execute_customer_processes, args=(customers['id'], customers['events']))
        # _processes.append(process)
        # print("Starting branch")
        cust_process.start()
        cust_process.join()
    '''
    for customers in customer_list:
        create_customer_processes(customers['id'], customers['events'])
    '''

    
    #Initiating server termination
    print("\nTerminating branch processes")
    for proc in branch_processes:
        print("herere")
        proc.terminate()
    
    #Create output file
    print("\nOutput written to output.txt file")
    #Create servers
    # for branch in branch_list:
    #     # print(branch)
    #     Branch.serve(branch['id'], branch['balance'])