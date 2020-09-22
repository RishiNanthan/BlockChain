import pymongo

SERVER = "mongodb://localhost:27017"
DATABASE_NAME = "BlockChain_DB"
COLLECTION_NAME = "Transaction"

"""
                TRANSACTION DOCUMENT STRUCTURE

                {
                    transaction_id: str,
                    public_key: str,
                    signature: str,
                    description: str,
                    timestamp: str,
                    inputs: [
                        {
                            transaction_id: str,
                            index: int,
                            value: float,
                            script_signature: str,
                        },
                        ....
                    ],
                    outputs: [
                        {
                            index: int,
                            value: float,
                            script_publickey: str,
                        },
                        ....
                    ],
                }

"""

class TransactionModel:

    def __init__(self):
        client = pymongo.MongoClient(SERVER)
        db = client.get_database(DATABASE_NAME)
        self.collection = db.get_collection(COLLECTION_NAME)

    def add_transaction(self, transaction) -> bool:
        if self.transaction_exists(transaction_id=transaction.transaction_id):
            ack = self.collection.insert_one(transaction.json_data())
            return ack.acknowledged
        return False

    def transaction_exists(self, transaction_id: str) -> bool:
        transaction = self.collection.find_one({"transaction_id": transaction_id})
        return transaction is not None

    def get_transaction(self, transaction_id: str):
        transaction = self.collection.find_one({"transaction_id": transaction_id})
        return transaction

