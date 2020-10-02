import base64
from .script import Script

"""

Example Locking Script (Output's Script):
    " OP_DUP OP_HASH160 <pub_key_hash> OP_EQUALVERIFY OP_CHECKSIG "

Example Unlocking Script (Input's Script):
    " <signature> <pub_key> "

For unlocking the LOCKING script is concatenated to the UNLOCKING script and verified
    " <signature> <pub_key> OP_DUP OP_HASH160 <pub_key_hash> OP_EQUALVERIFY OP_CHECKSIG "

"""


class Input:
    
    def __init__(self, transaction_id: str, index: int, value: float, script_signature: str):
        self.transaction_id = transaction_id
        self.value = value
        self.index = index
        self.script_signature = script_signature                                 # unlocking script
        
        
    def json_data(self) -> dict:
        data = {
            "transaction_id": self.transaction_id,
            "index": self.index,
            "value": self.value,
            "script_signtaure": self.script_signature,
        }
        return data


    def from_json(self, input_document: dict):
        self.transaction_id = input_document['transaction_id']
        self.index = input_document['index']
        self.value = input_document['value']
        self.script_signature = input_document['script_ssignature']
        

    def __str__(self) -> str:
        return f"transaction_id: {self.transaction_id}, index: {self.index}, value: {self.value}, scriptSig: {self.script_signature}"
