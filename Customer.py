import logging
import grpc
import bank_pb2
import bank_pb2_grpc
import time
import consts

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
        port = consts.BASE_PORT+self.id
        # channel = grpc.insecure_channel('localhost:{}'.format(port))
        channel = grpc.insecure_channel('localhost:{}'.format(port))
        stub = bank_pb2_grpc.BankStub(channel)
        self.stub = stub
        # print("stub on ",port)
        return stub
    '''
    # TODO: students are expected to send out the events to the Bank
    def executeEvents(self):
        output={"id":self.id, "recv":[]}
        print("Executing customer object , id {}".format(self.id))
        stub = self.createStub()
        # self.createStub()
        # print(stub)s
        for event in self.events:
            print("Executing event {}".format(event))
            if event['interface'] == 'query':
                request = bank_pb2.CustomerQueryRequest(id = int(self.id))
                response = stub.BranchQuery(request)
                output['recv'].append({"interface":"query", "balance":response.msg})
            elif event['interface'] == 'deposit':
                request = bank_pb2.CustomerTransactRequest(id = int(self.id), money=int(event['money']))
                response = stub.BranchDeposit(request)
                output['recv'].append({"interface":"deposit", "result":response.msg})

            elif event['interface'] == 'withdraw':
                request = bank_pb2.CustomerTransactRequest(id = int(self.id), money=int(event['money']))
                response = stub.BranchWithdraw(request)
                output['recv'].append({"interface":"deposit", "result":response.msg})
            else:
                logging.error("Invalid interface defined for event")
        
        return output
    '''
    def executeEvents(self):
        output={"id":self.id, "recv":[]}
        print("Executing customer object , id {}".format(self.id))
        stub = self.createStub()
        # self.createStub()
        # print(stub)s
        for event in self.events:
            print("Executing event {}".format(event))
            type = 'customer'
            balance = 0
            if('money' in event.keys()):
                money = int(event['money'])
            else:
                money = 0
            request = bank_pb2.BankRequest(id = int(self.id), type='customer', interface=event['interface'], balance=balance, money=money)
            response = stub.MsgDelivery(request)
            '''
            if event['interface'] == 'query':
                request = bank_pb2.CustomerQueryRequest(id = int(self.id))
                response = stub.BranchQuery(request)
                output['recv'].append({"interface":"query", "balance":response.msg})
            elif event['interface'] == 'deposit':
                request = bank_pb2.CustomerTransactRequest(id = int(self.id), money=int(event['money']))
                response = stub.BranchDeposit(request)
                output['recv'].append({"interface":"deposit", "result":response.msg})

            elif event['interface'] == 'withdraw':
                request = bank_pb2.CustomerTransactRequest(id = int(self.id), money=int(event['money']))
                response = stub.BranchWithdraw(request)
                output['recv'].append({"interface":"deposit", "result":response.msg})
            else:
                logging.error("Invalid interface defined for event")
            '''
            output['recv'].append({"interface":response.interface, "result":response.result, "balance":response.balance})
        return output