import sys
import pathlib
import hashlib
import rsa
from ..encoding import base58_decode, base58_encode, decode_public_key


class Script:

    def __init__(self, script: str, transaction_id: str):
        self.script = script
        self.transaction_id = transaction_id

    def verify_script(self):
        script_operations = self.script.split()
        script_operations = [i.strip() for i in script_operations]
        
        stack = []
        try:
            for operation in script_operations:
                
                if operation == "OP_DUP":
                    stack.append(stack[-1])

                elif operation == "OP_HASH160":
                    val = stack.pop(-1)
                    out_hash = Script.op_hash160(val)
                    stack.append(out_hash)

                elif operation == "OP_EQUALVERIFY":
                    val1 = stack.pop(-1)
                    val2 = stack.pop(-1)
                    if not Script.op_equalverify(val1, val2):
                        return False

                elif operation == "OP_CHECKSIG":
                    pubkey = stack.pop(-1)
                    signature = stack.pop(-1)
                    if not Script.op_checksig(pubkey, signature, self.transaction_id):
                        return False

                else:
                    stack.append(operation)

        except IndexError:
            return False

        except Exception as e:
            print(e)
            return False

        if not len(stack):
            return True

    
    @staticmethod
    def op_hash160(val: str):
        """
            op_hash160(val) = Base58_encode( RIPEMD160( SHA_256( Base58_decode( val ) ) ) )
        """
        val = base58_decode(val)
        val_decoded = bytes.fromhex(val)
        
        sha256 = hashlib.sha256()
        sha256.update(val_decoded)
        sha256_hash = sha256.digest()

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        ripemd_hash = ripemd160.hexdigest()

        out_decode = base58_encode(ripemd_hash)        
        return out_decode

    @staticmethod
    def op_equalverify(val1, val2):
        if val1 == val2:
            return True
        return False


    @staticmethod
    def op_checksig(public_key: str, signature: str, transaction_id: str):
        public_key = decode_public_key(public_key)
        signature = bytes.fromhex(signature)
        transaction_id = bytes.fromhex(transaction_id)
        try:
            rsa.verify(transaction_id, signature, public_key)
            return True
        except rsa.VerificationError:
            return False

