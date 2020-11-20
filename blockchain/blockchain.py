# Classes
from .block.block import Block
from .transaction.transaction import Transaction
from .address import address

# Database Models
from .database.blockchaindb import BlockChainModel
from .database.blockdb import BlockModel
from .database.transactiondb import TransactionModel
from .database.unspent_transactiondb import UnspentTransactionModel

# Other Libraries
import time


class BlockChain:

    def __init__(self):
        """

            This is the Interface / Entry Point to all the internal components.

        """

        self.block_chain_model = BlockChainModel()
        self.block_model = BlockModel()
        self.transaction_model = TransactionModel()
        self.unspent_transaction_model = UnspentTransactionModel()

        self.transaction_pool = []
        self.block_pool = []


    @staticmethod
    def generate_keys() -> tuple:
        """
            Generates new private_key, public_key pair

            Returns:
            (public_key, private_key)

        """
        return address.generate_keys()
    

    def add_block_pool(self, block_data: dict) -> bool:
        """
            Adds the block to the block_pool

            Parameters:
                block_data: dict

            Returns:
                bool
        """

        block = Block()
        block.from_json(block_data)
        if block.verify_block():
            self.block_pool += [block]
            self.store_block(block_data)
            return True
        return False


    def add_transaction_pool(self, transaction_data: dict) -> bool:
        """
            Adds the transaction to the transaction pool

            Parameters:
                transaction_data: dict

            Returns:
                bool
        """

        transaction = Transaction()
        transaction.from_json(transaction_data)
        if transaction.verify_transaction():
            self.transaction_pool += [transaction]
            self.store_transaction(transaction_data)
            return True
        return False
        

    def store_block(self, block_data: dict) -> Block:
        """
            Stores the block to the database. If already found or not valid block, returns False

            Parameters:
                block_data: dict

            Returns:
                bool

        """

        block = Block()
        block.from_json(block_data)
        if block.verify_block():
            return self.block_model.add_block(block)
        else:
            return False


    def store_transaction(self, transaction_data: dict) -> Transaction:
        """
            Stores the transaction to the database. If already found or not valid transaction, returns False

            Parameters:
                transaction_data: dict

            Returns:
                bool

        """

        transaction = Transaction()
        transaction.from_json(transaction_data)
        if transaction.verify_transaction():
            return self.transaction_model.add_transaction(transaction)
        else:
            return False


    def get_block(self, block_id: str):
        """
            Gets the corresponding block from the database. If not found, returns None

            Parameters:
                block_id: str // hexadecimal string

            Returns:
                Block

        """

        block = Block()
        block_data = self.block_model.get_block(block_id)
        if block_data is None:
            return None
        block.from_json(block_data)
        return block


    def get_transaction(self, transaction_id: str):
        """
            Gets the corresponding transaction from the database. If not found, returns None

            Parameters:
                transaction_id: str // hexadecimal string

            Returns:
                Transaction

        """

        transaction = Transaction
        transaction_data = self.transaction_model.get_transaction(transaction_id)
        if transaction_data is None:
            return None

        transaction.from_json(transaction_data)
        return transaction


    def mine_block(self, mining_function=None, transaction_count=10):
        """
            Creates a block using transactions from transaction_pool, returns None incase of failure

            Parameters:
                mining_function: Function  // in case you need more efficient algorithm
                transaction_count: int     // transactions per block

            Returns:
                str    // Block_Hash
  
        """

        new_block = Block()
        if mining_function is not None:
            new_block.find_nonce = mining_function

        while len(new_block.transactions) < transaction_count:
            if not len(self.transaction_pool):
                print("Waiting 5 seconds for new transactions to create block ... ")
                time.sleep(5)
                continue

            transaction = self.transaction_pool.pop(0)
            new_block.transactions += [transaction]

        nonce = new_block.find_nonce()
        block_hash = new_block.find_hash()

        if self.add_block_pool(new_block.json_data()):
            print(f" Block [{ block_hash }] Created ...")
            return block_hash

        print(" Block creation Failed ...")
        return None
        
