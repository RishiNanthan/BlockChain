from .block.block import Block
from .transaction.transaction import Transaction

from .database.blockchaindb import BlockChainModel
from .database.blockdb import BlockModel
from .database.transactiondb import TransactionModel
from .database.unspent_transactiondb import UnspentTransactionModel



class BlockChain:

    def __init__(self):
        """

            This is the Interface / Entry Point to all the internal components.

        """

        self.block_chain_model = BlockChainModel()
        self.block_model = BlockModel()
        self.transaction_model = TransactionModel()
        self.unspent_transaction_model = UnspentTransactionModel()
        

    def add_block(self, block_data: dict):
        """
            Adds the block to the database. If already found or not valid block, returns False

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


    def add_transaction(self, transaction_data: dict):
        """
            Adds the transaction to the database. If already found or not valid transaction, returns False

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
        block_data = self.get_block(block_id)
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


    def mine_block(self, mining_function=None):
        new_block = Block
        if mining_function is not None:
            new_block.find_nonce = mining_function

        pass
        


