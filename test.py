import sys 
sys.path.insert(1,r"C:\Users\Kavi Priya\Documents\GitHub\BlockChain\transaction")
from transaction.Input import Input 

sample_transaction=Input("A245678BET",3,"123456789")
print(sample_transaction)