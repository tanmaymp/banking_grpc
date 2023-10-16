import grpc
import bank_pb2
import bank_pb2_grpc
import consts
import multiprocessing
import json

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None

    # TODO: students are expected to create the Customer stub
    def createStub(self):
        '''
        generates and returns a client stub
        code referred from : https://grpc.io/docs/languages/python/quickstart/
        '''
        port = consts.BASE_PORT+self.id
        channel = grpc.insecure_channel('localhost:{}'.format(port))
        stub = bank_pb2_grpc.BankStub(channel)
        self.stub = stub
        return stub
        
    def executeEvents(self):
        '''
        for every event makes the RPC call and returns responses
        '''
        output={"id":self.id, "recv":[]}
        stub = self.createStub()
        for event in self.events:
            type = 'customer'
            balance = 0
            if('money' in event.keys()):
                money = int(event['money'])
            else:
                money = 0
            request = bank_pb2.BankRequest(id = int(self.id), type='customer', interface=event['interface'], balance=balance, money=money)
            response = stub.MsgDelivery(request)
            if response.interface in ('deposit', 'withdraw'):
                resp = {"interface":response.interface, "result":response.result}
            elif response.interface == 'query':
                resp = {"interface":response.interface, "balance":response.balance}
            output['recv'].append(resp)
        return output
    
def execute_customer_processes(id, events):
    '''
    calls the executeEvents and consolidates responses and generated final output
    '''
    cust_obj = Customer(id=id, events=events)
    output_obj = cust_obj.executeEvents()
    with open(consts.OUTPUT_FILE, 'a') as file:
        json.dump(output_obj, file)
        file.write('\n')

def initialize_customer_processes(customer_list):
    '''
    initiates customer processes
    '''
    for customers in customer_list:
        cust_process = multiprocessing.Process(target=execute_customer_processes, args=(customers['id'], customers['events']))
        cust_process.start()
        cust_process.join()