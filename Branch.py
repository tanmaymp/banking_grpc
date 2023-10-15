import logging
import grpc
import bank_pb2
import bank_pb2_grpc
from concurrent import futures
import consts
import multiprocessing
from time import sleep

branch_objects = []
branch_processes = []

class Branch(bank_pb2_grpc.BankServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches

        # TODO: students are expected to store the processID of the branches
        pass

    # TODO: students are expected to process requests from both Client and Branch
    def MsgDelivery(self,request, context):
        response = bank_pb2.BankResponse()
        response.interface = request.interface
        if request.type == 'customer':
            if request.interface == 'query':
                response.balance = self.BranchQuery()
                return response
            elif request.interface == 'deposit':
                response.result = self.BranchDeposit(request.money)
                self.BranchPropogateDeposit(request.money)
                return response
                # response
            elif request.interface == 'withdraw':
                response.result = self.BranchWithdraw(request.money)
                self.BranchPropogateWithdraw(request.money)
                return response 
            else:
                logging.error("Invalid interface defined for event")
        elif request.type == 'branch':
            if request.interface == 'propogate_deposit':
                self.BranchDeposit(request.money)
            elif request.interface == 'propogate_withdraw':
                self.BranchWithdraw(request.money)
        else:
            logging.info("Invalid request type received")   
        return response

    def BranchQuery(self):
        return self.balance

    def BranchDeposit(self, money):
        try:
            self.balance = int(self.balance) + int(money)
            return 'success'
        except:
            return 'failure'
        
    def BranchWithdraw(self, money):
        try:
            self.balance = int(self.balance) - int(money)
            return 'success'
        except:
            return 'failure'
        
    def BranchPropogateWithdraw(self, money):
        global branch_objects
        for stub in self.stubList:
            interface, balance = 'propogate_withdraw', 0
            request = bank_pb2.BankRequest(id = int(self.id), type='branch', interface=interface, balance=balance, money=money)
            stub.MsgDelivery(request)

    def BranchPropogateDeposit(self, money):
        global branch_objects
        for stub in self.stubList:
            interface, balance = 'propogate_deposit', 0
            request = bank_pb2.BankRequest(id = int(self.id), type='branch', interface=interface, balance=balance, money=money)
            stub.MsgDelivery(request)

def serve(id, balance, stubList):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    port = str(consts.BASE_PORT+int(id))
    branch_obj = Branch(id=id, balance=balance, branches='1')
    branch_obj.stubList = stubList
    bank_pb2_grpc.add_BankServicer_to_server(branch_obj, server)
    server.add_insecure_port("localhost:{}".format(port))
    server.start()
    print("Starting server {}, Listening on port {}".format(branch_obj.id, port))
    server.wait_for_termination()

def createStub(other_branch):
    port = consts.BASE_PORT+int(other_branch.id)
    # print("port", port)
    channel = grpc.insecure_channel('localhost:{}'.format(port))
    stub = bank_pb2_grpc.BankStub(channel)
    return stub

def create_branch_subs():
    global branch_objects
    for i in range(len(branch_objects)):
        stub_list = []
        for j in range(len(branch_objects)):
            if i == j:
                continue
            branch_stub = createStub(branch_objects[j])
            stub_list.append(branch_stub)
        branch_objects[i].stubList = stub_list

def initialize_branch_processes(branch_list):
    global branch_processes
    global branch_objects
    for branch in branch_list:
        branch_objects.append(Branch(id=branch['id'], balance=branch['balance'], branches='1'))
    create_branch_subs()
    for branch in branch_objects:
        branch_process = multiprocessing.Process(target=serve, args=(branch.id, branch.balance, branch.stubList))
        branch_processes.append(branch_process)
        branch_process.start()
    sleep(3)
    return

def terminate_branch_processes():
    global branch_processes
    for proc in branch_processes:
        # print("herere")
        proc.terminate()

