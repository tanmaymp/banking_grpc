# Distributed Banking System Using gRPC

## Problem Statement:
To design a distributed banking system which allows multiple customers to interact with bank branches enabling them to perform actions such as depositing, withdrawing, and checking their account balances. The primary objective.is to leverage gRPC to create interfaces which the system can utilize to execute customer requests while maintaining consistency of balance across the branches in the system.

## Key assumptions:
1.	Every customer interacts exclusively with a specific branch in the system, and both the customer and the branch share a common identifier(ID).
2.	All customers direct their transactions to a shared account within the bank, and the branch's balance is synonymous with the account balance. This underscores the critical requirement that any modification to the balance of any branch must be synchronized across all branches in the system.
3.	No concurrent transactions occur on any branch. 

## Execution setup
1.	Input file 
The input file must be a valid json file and should be placed in the “test/” folder with the name “input.json”. If needed, the input file name can be changed but to ensure that the code reads it the value set for global variable INPUT_FILE in consts.py should be updated accordingly

2.	Output file
The final output is stored in a text file “output.txt” which is generated in the same directory(./output.txt). If needed, the output file name can be changed as well by updating the global variable OUTPUT_FILE in consts.py accordingly.

3.	Executing the system
Once the input file is set, run the bank_main.py file to initiate the system. It would read the input file, process everything and generate the output.txt.


## Implementation Processes

### Interfaces

Customer to Branch interfaces

Query		  - used by customer processes to the check the current balance in the branch process.
Deposit		- used by customer processes to deposit/increment balance in the branch process.
Withdraw	- used by customer processes to withdraw/decrement balance from the branch.

Branch to Branch interfaces

PropagateDeposit	– used by branch processes to propagate the deposit to other branches of the         system to maintain consistency
PropagateWithdraw	– used by branch processes to propagate the deposit to other branches of the system to maintain consistency

## Code Implementation

| Operation           | Function                                      | Description                                                                 |
|---------------------|-----------------------------------------------|-----------------------------------------------------------------------------|
| Query               | `Branch.BranchQuery()`                        | Returns the current balance from `Branch.balance`                           |
| Deposit             | `Branch.BranchDeposit(money)`                 | Increments `Branch.balance` by `money`                                      |
| Withdraw            | `Branch.BranchWithdraw(money)`                | Decrements `Branch.balance` by `money`                                      |
| Propagate Deposit   | `Branch.BranchPropagateDeposit(money)`        | Propagates deposit to all branches and increments their `Branch.balance`    |
| Propagate Withdraw  | `Branch.BranchPropagateWithdraw(money)`       | Propagates withdraw to all branches and decrements their `Branch.balance`   |
