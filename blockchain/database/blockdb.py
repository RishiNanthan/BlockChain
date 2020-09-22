import pymongo

SERVER = "mongodb://localhost:27017"
DATABASE_NAME = "BlockChain_DB"
COLLECTION_NAME = "Block"


"""
                    BLOCK DOCUMENT STRUCTURE
                    
                    {
                        block_id: str,
                        version: int,
                        previous_block: str,
                        timestamp: str,
                        nonce: int,
                        transactions: [
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
                            },
                            ....
                        ]
                    }

"""

class BlockModel:
    
    def __init__(self):
        client = pymongo.MongoClient(SERVER)
        db = client.get_database(DATABASE_NAME)
        self.collection = db.get_collection(COLLECTION_NAME)

    def add_block(self, block) -> bool:
        query_result = self.collection.insert_one(block.json_data())
        return query_result.acknowledged

    def get_block(self, block_id: str) -> dict:
        query_result = self.collection.find_one({ "block_id": block_id }, { "id": 0 })
        return query_result
        