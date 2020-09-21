import pymongo


SERVER = "mongodb://localhost:27017"
DATABASE_NAME = "BlockChain_DB"
COLLECTION_NAME = "BlockChain"

class BlockChainModel:

    def __init__(self):
        client = pymongo.MongoClient(SERVER)
        db = client.get_database(DATABASE_NAME)
        self.collection = db.get_collection(COLLECTION_NAME)

