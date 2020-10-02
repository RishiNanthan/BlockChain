
from blockchain.blockchain import BlockChain
import blockchain_server
import blockchain_client


class Initialiser:
    def __init__(self, ip: str, port: int):
        self.IP = ip
        self.PORT = port

        self.CONNECTED_NODES = set()
        self.TRANSACTION_INVITES = {}
        self.BLOCK_INVITES = {}

        self.BLOCK_CHAIN = BlockChain()


CONSTANTS = Initialiser("127.0.0.1", 8000)
blockchain_server.CONSTANTS = CONSTANTS
blockchain_client.CONSTANTS = CONSTANTS


blockchain_server.run_app()
