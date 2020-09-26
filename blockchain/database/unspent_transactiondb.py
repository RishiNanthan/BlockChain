import pymongo

SERVER = "mongodb://localhost:27017"
DATABASE_NAME = "BlockChain_DB"
COLLECTION_NAME = "Unspent_Transaction"

"""
            UNSPENT TRANSACTION DOCUMENT STRUCTURE

            {
                transaction_id: str,
                output_index: int,
            }

"""


class UnspentTransactionModel:


    def __init__(self):
        client = pymongo.MongoClient(SERVER)
        db = client.get_database(DATABASE_NAME)
        self.collection = db.get_collection(COLLECTION_NAME)


    def add_transaction(self, transaction):
        inputs = transaction.inputs
        outputs = transaction.outputs
        transaction_id = transaction.transaction_id

        for i in inputs:
            self.collection.delete_one(
                {
                    "transaction_id": i.transaction_id,
                    "output_index": i.index,
                }
            )

        unspent_documents = [
            {
                "transaction_id": transaction_id,
                "output_index": output.index
            } for output in outputs
        ]

        self.collection.insert_many(unspent_documents)


    def is_spent(self, transaction_input):
        queryset = self.collection.find(
            {
                "transaction_id": transaction_input.transaction_id,
                "output_index": transaction_input.index,
            }
        )
        return queryset.count()
