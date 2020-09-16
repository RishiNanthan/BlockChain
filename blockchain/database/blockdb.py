import pymongo

SERVER = "mongodb://localhost:27017"
DATABASE_NAME = "BlockChain_DB"
COLLECTION_NAME = "Block"


"""
                    BLOCK DOCUMENT STRUCTURE
                    
                    {
                        block_hash: str,
                        previous_block: str,
                        nonce: int,
                        total_input: float,
                    }

"""

class BlockModel:
    
    def __init__(self):
        client = pymongo.MongoClient(SERVER)
        db = client.get_database(DATABASE_NAME)
        self.collection = db.get_collection(COLLECTION_NAME)

    def add_block(self, block):
        pass

    def get_block(self):
        pass