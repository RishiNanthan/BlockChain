import sys
import pathlib
import hashlib
from ecdsa import VerifyingKey as PublicKey, BadSignatureError
from ..encoding.encoding import base58_decode, base58_encode, decode_public_key


class Script:

    def __init__(self, script: str, transaction_id: str):
        self.script = script
        self.transaction_id = transaction_id
        self.stack = []

    def verify_script(self):
        script_operations = self.script.split()
        script_operations = [i.strip() for i in script_operations]
        
        try:
            for operation in script_operations:
                
                if operation == "OP_DUP":
                    # Duplicate the topmost of stack
                    self.stack.append(self.stack[-1])

                elif operation == "OP_HASH160":
                    # Hash the topmost with SHA_256 and then with RIPEMD160
                    self.op_hash160()

                elif operation == "OP_EQUALVERIFY":
                    # Take two top elements of stack and check if equal, if not equal throw error
                    self.op_equalverify()

                elif operation == "OP_CHECKSIG":
                    # Take top two and check whether the signature is correct
                    self.op_checksig()

                elif operation == "OP_NOP":
                    # No operation
                    continue

                elif operation == "OP_EQUAL":
                    # Equates top two stack elements and push the result to stack
                    self.op_equal()

                elif operation == "OP_RIPEMD160":
                    self.op_ripemd160()

                elif operation == "OP_SHA256":
                    self.op_sha256()

                else:
                    #  not an operation, it might be pubkey, signature, hash etc.
                    self.stack.append(operation)

        except IndexError:
            return False

        except Exception as e:
            print(e)
            return False

        if len(self.stack) == 1 and self.stack[0] == True:
            return True
        return False


    def op_ripemd160(self):
        val = self.stack.pop(-1)

        val = base58_decode(val)
        val_decoded = bytes.fromhex(val)

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(val_decoded)
        ripemd_hash = ripemd160.hexdigest()

        out_decode = base58_encode(ripemd_hash)        
        self.stack.append(out_decode)


    def op_sha256(self):
        val = self.stack.pop(-1)

        val = base58_decode(val)
        val_decoded = bytes.fromhex(val)
        
        sha256 = hashlib.sha256()
        sha256.update(val_decoded)
        sha256_hash = sha256.digest()

        out_decode = base58_encode(sha256_hash)        
        self.stack.append(out_decode)


    def op_hash160(self):
        """
            op_hash160(val) = Base58_encode( RIPEMD160( SHA_256( Base58_decode( val ) ) ) )
        """
        val = self.stack.pop(-1)

        val = base58_decode(val)
        val_decoded = bytes.fromhex(val)
        
        sha256 = hashlib.sha256()
        sha256.update(val_decoded)
        sha256_hash = sha256.digest()

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        ripemd_hash = ripemd160.hexdigest()

        out_decode = base58_encode(ripemd_hash)        
        self.stack.append(out_decode)


    def op_equal(self):
        val1 = self.stack.pop(-1)
        val2 = self.stack.pop(-1)
        if val1 == val2:
            self.stack.append(True)
        else:
            self.stack.append(False)
    

    def op_equalverify(self):
        val1 = self.stack.pop(-1)
        val2 = self.stack.pop(-1)
        if val1 == val2:
            return True
        raise Exception("Script Verification Error")


    def op_checksig(self):
        public_key = self.stack.pop(-1)
        signature = self.stack.pop(-1)

        public_key = decode_public_key(public_key)
        signature = bytes.fromhex(signature)
        transaction_id = bytes.fromhex(self.transaction_id)

        public_key.verify(signature, transaction_id)
        self.stack.append(True)

