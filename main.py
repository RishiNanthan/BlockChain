
from blockchain.blockchain import BlockChain
import blockchain_client
import blockchain_server


IP = None
PORT = None
CONNECTED_NODES = []        # list of addresses
BLOCKCHAIN = BlockChain()
BLOCK_INVITES = []          # list of {"block_id": block_id, "ip_address": ip_address}
TRANSACTION_INVITES = []    # list of {"transaction_id": transaction_id, "ip_address": ip_address}


def initialise():
    global IP, PORT, CONNECTED_NODES, BLOCKCHAIN, BLOCK_INVITES, TRANSACTION_INVITES

    IP = input("Enter IP address: ")
    PORT = int(input("Enter PORT number: "))

    blockchain_client.IP = IP
    blockchain_client.PORT = PORT
    blockchain_client.CONNECTED_NODES = CONNECTED_NODES
    blockchain_client.BLOCKCHAIN = BLOCKCHAIN
    blockchain_client.BLOCK_INVITES = BLOCK_INVITES
    blockchain_client.TRANSACTION_INVITES = TRANSACTION_INVITES

    blockchain_server.IP = IP
    blockchain_server.PORT = PORT
    blockchain_server.CONNECTED_NODES = CONNECTED_NODES
    blockchain_server.BLOCKCHAIN = BLOCKCHAIN
    blockchain_server.BLOCK_INVITES = BLOCK_INVITES
    blockchain_server.TRANSACTION_INVITES = TRANSACTION_INVITES


if __name__ == '__main__':

    initialise()

    blockchain_client.run_client(mining=True)
    blockchain_server.run_server()
    
