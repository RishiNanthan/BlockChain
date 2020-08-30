import base64
from .transaction import Transaction
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
    def __init__(self, transaction_id: str, index: int, script_signature: str):
        self.transaction_id = transaction_id
        self.index = index
        self.script_signature = script_signature                                 # unlocking script
        
        
    def verify_script(self):
        transaction = Transaction.get_transaction(self.transaction_id)

        locking_script = transaction.outputs[self.index].script_publickey
        script_string = self.script_signature + " " + locking_script

        script = Script(script_string, self.transaction_id)
        if script.verify_script():
            return True
        return False

    def __str__(self):
        return f"transaction_id: {self.transaction_id}, index: {self.index}, scriptSig: {self.script_signature}"
        
