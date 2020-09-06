
class Transaction:

    def __init__(self, inputs: list=None, outputs: list=None, timestamp: str=None, transaction_id: str=None,description: str=None):
        self.inputs = inputs
        self.outputs = outputs
        self.timestamp = timestamp
        self.transaction_id = transaction_id            # Hash of transaction
        self.description = description


    @staticmethod
    def get_transaction(transaction_id: str):
        """
            Fetches transaction from blockchain given transaction id
        """
        return Transaction()


    def find_transaction_id(self):
        pass


