import logging
import grpc
import bank_pb2
import bank_pb2_grpc
from concurrent import futures
import consts
import multiprocessing
from time import sleep
import logger

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
        # logical clock
        self.logclock = 0
        # event tracker
        self.event_tracker = []

        # TODO: students are expected to store the processID of the branches
        pass

    # TODO: students are expected to process requests from both Client and Branch
    def MsgDelivery(self,request, context):
        '''
        recieves requests from customer/branches and executes the interfaces accordingly and retunrs a response
        '''
        response = bank_pb2.BankResponse()
        response.interface = request.interface
        response.branch_id = self.id
        
        #print("Logging..")
        #print("interface = ", request.interface)
        #print("ID = ", self.id)
        #print("stub = ", request.id)
        self.logclock = max(self.logclock, request.logclock) + 1
        #logger.logfile('branch', request.interface, request.eventid, self.logclock, self.id, request.id, tag='R')
        # Compute log clock

        while(request.interface in ['query', 'deposit', 'withdraw'] and self.event_tracker != request.event_tracker):
            #print("Blocking branch {} and waiting for propogartion".format(self.id))
            sleep(1)

        
        if request.type == 'customer':
            if request.interface == 'query':
                response.balance = self.BranchQuery()
                return response
            elif request.interface == 'deposit':
                #print("Depositing")
                response.result = self.BranchDeposit(request.money)
                self.event_tracker.append(request.eventid)
                self.BranchPropogateDeposit(request)
                return response
                # response
            elif request.interface == 'withdraw':
                response.result = self.BranchWithdraw(request.money)
                self.event_tracker.append(request.eventid)
                self.BranchPropogateWithdraw(request)
                return response 
            else:
                logging.error("Invalid interface defined for event")
        elif request.type == 'branch':
            if request.interface == 'propogate_deposit':
                #print("Propagating Depositing")
                self.BranchDeposit(request.money)
                self.event_tracker.append(request.eventid)
            elif request.interface == 'propogate_withdraw':
                self.BranchWithdraw(request.money)
                self.event_tracker.append(request.eventid)
        else:
            logging.info("Invalid request type received")   
        
        return response

    def BranchQuery(self):
        '''
        Query interface
        '''
        return self.balance

    def BranchDeposit(self, money):
        '''
        Deposit interface
        '''
        try:
            self.balance = int(self.balance) + int(money)
            return 'success'
        except:
            return 'failure'
        
    def BranchWithdraw(self, money):
        '''
        Withdraw interface
        '''
        try:
            self.balance = int(self.balance) - int(money)
            return 'success'
        except:
            return 'failure'
        
    def BranchPropogateWithdraw(self, request):
        '''
        PropagateWithdraw interface
        '''
        global branch_objects
        #self.logclock = self.logclock + 1
        for stub in self.stubList:
            interface, balance = 'propogate_withdraw', 0
            self.logclock = self.logclock + 1
            request = bank_pb2.BankRequest(id = int(self.id), eventid=request.eventid, type='branch', interface=interface, balance=balance, money=request.money, logclock=self.logclock, event_tracker=self.event_tracker)
            #print("propagating from ", self.id, "to ", stub['branch'])
            
            stub["stub"].MsgDelivery(request)
            #logger.logfile('branch', interface, request.eventid, self.logclock, request.id, stub=stub['branch'], tag='S')

    def BranchPropogateDeposit(self, request):
        '''
        PropagateDeposit interface
        '''
        #print("Propagated!!")
        global branch_objects
        #self.logclock = self.logclock + 1
        for stub in self.stubList:
            #print("in loop")
            interface, balance = 'propogate_deposit', 0
            self.logclock = self.logclock + 1
            request = bank_pb2.BankRequest(id = int(self.id), eventid=request.eventid, type='branch', interface=interface, balance=balance, money=request.money, logclock=self.logclock, event_tracker=self.event_tracker)
            #print("propagating from ", self.id, "to ", stub['branch'])
            
            stub["stub"].MsgDelivery(request)
            #print("Propagated!!")
            #logger.logfile('branch', interface, request.eventid, self.logclock, request.id, stub=stub['branch'], tag='S')

def serve(id, balance, stubList):
    '''
    initializes a branch server, also populates the stubList for branches.
    code referred from : https://grpc.io/docs/languages/python/quickstart/
    '''
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
    '''
        generates and returns a client stub
        code referred from : https://grpc.io/docs/languages/python/quickstart/
    '''
    port = consts.BASE_PORT+int(other_branch.id)
    # print("port", port)
    channel = grpc.insecure_channel('localhost:{}'.format(port))
    stub = bank_pb2_grpc.BankStub(channel)
    return stub

def create_branch_subs():
    '''
    populates stub list for other branches
    '''
    global branch_objects
    for i in range(len(branch_objects)):
        stub_list = []
        for j in range(len(branch_objects)):
            if i == j:
                continue
            branch_stub = createStub(branch_objects[j])
            #print("stublist1", branch_stub)
            stub_list.append({"branch":j+1, "stub":branch_stub})
        branch_objects[i].stubList = stub_list
        #print("stublist", branch_objects[i].stubList)

def initialize_branch_processes(branch_list):
    '''
    initiates branch processes
    '''
    global branch_processes
    global branch_objects
    for branch in branch_list:
        branch_objects.append(Branch(id=branch['id'], balance=branch['balance'], branches='1'))
    create_branch_subs()
    for branch in branch_objects:
        branch_process = multiprocessing.Process(target=serve, args=(branch.id, branch.balance, branch.stubList))
        branch_processes.append(branch_process)
        branch_process.start()
    sleep(5)
    return

def terminate_branch_processes():
    '''
    terminates branch processes
    '''
    global branch_processes
    for proc in branch_processes:
        proc.terminate()


