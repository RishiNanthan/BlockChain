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
        self.transactions = transactions


    def find_hash(self) -> str:
        document = self.json_data()
        document.pop("block_id")
        document_string = str(document)

        hash_fun = sha256()
        hash_fun.update(document_string)
        hash_string = hash_fun.hexdigest()

        return base58_encode(hash_string) 


    def verify_block(self) -> bool:
        if not self.verify_proof_of_work() or self.find_hash() != self.block_id:
            return False
        
        for transaction in self.transactions:
            if not transaction.verify_transaction():
                return False
        
        return True
        

    def verify_proof_of_work(self):
        block_hash = base58_decode(self.block_id)
        block_id_number = int.from_bytes(bytes.fromhex(block_hash), "big")
        if block_id_number <= self.difficulty:
            return True
        return False


    def find_nonce(self) -> int:
        """
                Miners can replace this function so that they may compute nonce in reliable manner
        """
        self.nonce = 0
        self.find_hash()
        while not self.verify_proof_of_work():
            self.nonce += 1
            self.find_hash()
        return self.nonce


    def json_data(self) -> dict:
        document = {
            "block_id": self.block_id,
            "version": self.version,
            "previous_block": self.previous_block,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "transactions": self.transactions,
        }
        return document


    def __str__(self):
        return str(self.json_data())


    def __repr__(self):
        return str(self.block_id)

