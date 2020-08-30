
class Transaction:

    def __init__(self, inputs: list=None, outputs: list=None, timestamp: str=None, transaction_id: str=None, description: str):
        self.inputs = inputs
        self.outputs = outputs
        self.timestamp = timestamp
        self.transaction_id = transaction_id
        self.description = description

    def get_transaction(self, transaction_id: str):
        """
            Fetches transaction from blockchain given transaction id
        """
        pass

