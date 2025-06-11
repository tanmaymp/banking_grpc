import grpc
import bank_pb2
import bank_pb2_grpc
import consts
import multiprocessing
import json
import logger

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
        # logical clock
        self.logclock = 0
        # event tracker
        self.event_tracker = []

    # TODO: students are expected to create the Customer stub
    def createStub(self, branch_id):
        '''
        generates and returns a client stub
        code referred from : https://grpc.io/docs/languages/python/quickstart/
        '''
        port = consts.BASE_PORT+branch_id
        channel = grpc.insecure_channel('localhost:{}'.format(port))
        stub = bank_pb2_grpc.BankStub(channel)
        self.stub = stub
        return stub
        
    def executeEvents(self):
        '''
        for every event makes the RPC call and returns responses
        '''
        output_list = []
        #output={"id":self.id, "recv":[]}
        #stub = self.createStub(self.id)
        
        for event in self.events:
            output={"id":self.id, "recv":[]}
            type = 'customer'
            balance = 0
            if('money' in event.keys()):
                money = int(event['money'])
            else:
                money = 0
            self.logclock = self.logclock + 1
            request = bank_pb2.BankRequest(id = int(self.id), eventid=event['id'], type='customer', interface=event['interface'], balance=balance, money=money,  logclock=self.logclock, event_tracker=self.event_tracker)
            #logger.logfile(type, event['interface'], event['id'], self.logclock, self.id)
            stub = self.createStub(event['branch'])
            #print("Here")
            response = stub.MsgDelivery(request)
            #print("Here")
            #print("RESP ", response)
            if response.interface in ('deposit', 'withdraw'):
                resp = {"interface":response.interface, "branch":response.branch_id, "result":response.result}
                self.event_tracker.append(event['id'])
                # output['recv'].append(resp)
            elif response.interface == 'query':
                resp = {"interface":response.interface, "branch":response.branch_id, "balance":response.balance}
                # output['recv'].append(resp)
            output['recv'].append(resp)
            output_list.append(output)
            #print(output)
        return output_list
    
def execute_customer_processes(id, events):
    '''
    calls the executeEvents and consolidates responses and generated final output
    '''
    cust_obj = Customer(id=id, events=events)
    output_obj = cust_obj.executeEvents()
    # logger.writelog()
    with open(consts.OUTPUT_FILE, 'w+') as file:
        json.dump(output_obj, file, indent=4)
        file.write('\n')

def initialize_customer_processes(customer_list):
    '''
    initiates customer processes
    '''
    for customers in customer_list:
        cust_process = multiprocessing.Process(target=execute_customer_processes, args=(customers['id'], customers['events']))
        cust_process.start()
        cust_process.join()
        # logger.writelog()
    
