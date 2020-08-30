

class Output:

    def __init__(self, index: int, value: float, script_publickey: str):
        self.index = index
        self.value = value
        self.script_publickey = script_publickey        #  Locking Script


    def __str__(self):
        return f"index: {self.index}, value: {self.value}, scriptPubSig: {self.script_publickey}"

    