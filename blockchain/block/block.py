from ..encoding.encoding import base58_encode, base58_decode
from ..transaction.transaction import Transaction
from hashlib import sha256


HASH_DIFFICULTY = None                #  Proof of Work    INTEGER
VERSION = None                        #  Version of the Software  INTEGER


class Block:

    difficulty = HASH_DIFFICULTY
    version = VERSION

    def __init__(self, previous_block: str=None, block_id: str=None, timestamp: str=None, nonce: int=None,
     transactions: list=None):
        """
                The first transaction should be the coinbase transaction
        """
        self.block_id = block_id
        self.previous_block = previous_block
        self.timestamp = timestamp
        self.nonce = nonce
        self.transactions = transactions if transactions is not None else []
        self.__version = self.version
        self.__difficulty = self.difficulty


    def find_hash(self) -> str:
        # returns hash without encoding -change if it doesnt feel good
        document = self.json_data()
        document.pop("block_id")
        document_string = str(document)

        hash_fun = sha256()
        hash_fun.update(document_string)
        hash_string = hash_fun.hexdigest()
        return hash_string


    def find_block_id(self) -> str:
        hash_string = find_hash()
        return base58_encode(hash_string) 


    def verify_block(self) -> bool:
        block_hash = self.base58_decode(self.block_id)
        if not self.verify_proof_of_work(block_hash) or self.find_block_id() != self.block_id:
            return False
        
        for transaction in self.transactions:
            if not transaction.verify_transaction():
                return False
        
        return True
        

    def verify_proof_of_work(self, block_hash):
        
        block_id_number = int.from_bytes(bytes.fromhex(block_hash), "big")
        if block_id_number <= self.difficulty:
            return True
        return False


    def find_nonce(self) -> int:
        """
                Miners can replace this function so that they may compute nonce in reliable manner
        """
        self.nonce = 0
        block_hash = self.find_hash()
        while not self.verify_proof_of_work(block_hash):
            self.nonce += 1
            block_hash = self.find_hash()
        return self.nonce


    def json_data(self) -> dict:
        document = {
            "block_id": self.block_id,
            "version": self.version,
            "previous_block": self.previous_block,
            "timestamp": self.timestamp,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "transactions": self.transactions,
        }
        return document


    def from_json(self, block_document: dict):
        self.block_id = block_document['block_id']
        self.__version = block_document['version']
        self.previous_block = block_document['previous_block']
        self.timestamp = block_document['timestamp']
        self.__difficulty = block_document['difficulty']
        self.nonce = block_document['nonce']
        self.transactions = [ Transaction().from_json(doc) for doc in block_document['transactions'] ]


    def __str__(self):
        return str(self.json_data())


    def __repr__(self):
        return str(self.block_id)

