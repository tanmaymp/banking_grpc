import grpc
import bank_pb2
import bank_pb2_grpc
from concurrent import futures
import consts

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
        pass

    def BranchQuery(self,request, context):
        response = bank_pb2.CustomerQueryResponse()
        response.msg = int(self.balance)
        return response

    def BranchDeposit(self,request, context):
        response = bank_pb2.NotificaionResponse()
        try:
            self.balance = int(self.balance) + int(request.money)
            response.msg = 'success'
            return response
        except:
            response.msg = 'failure'
            return response
        
    def BranchWithdraw(self,request, context):
        response = bank_pb2.NotificaionResponse()
        try:
            self.balance = int(self.balance) - int(request.money)
            response.msg = 'success'
            return response
        except:
            response.msg = 'failure'
            return response
        
    def BranchPropogateWithdraw(self,request, context):
        pass
    def BranchPropogateDeposit(self,request, context):
        pass

def serve(id, balance):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    port = str(consts.BASE_PORT+int(id))
    bank_pb2_grpc.add_BankServicer_to_server(Branch(id=id, balance=balance, branches='1'), server)
    # server.add_insecure_port("localhost:{}".format(port))
    server.add_insecure_port("localhost:{}".format(port))
    server.start()
    print("Starting server {}, Listening on port {}".format(id, port))
    server.wait_for_termination()