import base64


class Input:
    def __init__(self, transaction_id: str, index: int, script_signature: str):
        self.transaction_id = transaction_id
        self.index = index
        self.script_signature = script_signature                                 # unlocking scripts
        
        """

        Example Locking Script:
            " OP_DUP OP_HASH160 <pub_key_hash> OP_EQUALVERIFY OP_CHECKSIG "
        
        Example Unlocking Script:
            " <signature> <pub_key> "

        For unlocking the LOCKING script is concatenated to the UNLOCKING script and verified
            " <signature> <pub_key> OP_DUP OP_HASH160 <pub_key_hash> OP_EQUALVERIFY OP_CHECKSIG "

        """
        
    def verify_script(self):
        pass
