

class Output:

    def __init__(self, index: int, value: float, script_publickey: str):
        self.index = index
        self.value = value
        self.script_publickey = script_publickey        #  Locking Script


    def json_data(self):
        data = {
            "index": self.index,
            "value": self.value,
            "script_publickey": self.script_publickey,
        }
        return data


    def from_json(self, output_document: dict):
        self.index = output_document['index']
        self.value = output_document['value']
        self.script_publickey = output_document['script_publickey']
        

    def __str__(self):
        return f"index: {self.index}, value: {self.value}, scriptPubSig: {self.script_publickey}"
