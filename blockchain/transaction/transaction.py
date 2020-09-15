import hashlib
from ecdsa import BadSignatureError
from ..encoding.encoding import decode_public_key
from ..database.transactiondb import TransactionModel


class Transaction:

    def __init__(self, publickey: str = None, inputs: list = None, outputs: list = None, timestamp: str = None,
                 transaction_id: str = None, signature: str = None, description: str = None):

        self.publickey = publickey
        self.inputs = inputs if inputs is not None else []
        self.outputs = outputs
        self.timestamp = timestamp
        self.transaction_id = transaction_id  # Hash of transaction
        self.signature = signature  # signature of the hash of all details except transaction_id
        self.description = description

    @staticmethod
    def get_transaction(transaction_id: str):
        """
            Fetches transaction from transaction database given transaction id
        """
        transaction_data = TransactionModel().get_transaction(transaction_id)
        return transaction_data

    @staticmethod
    def add_transaction(transaction) -> bool:
        """
            Inserts transaction to the transaction database
        """
        return TransactionModel().add_transaction(transaction=transaction)

    def find_transaction_id(self) -> str:
        """
            Hash of the details of entire transaction
        """
        assert self.outputs is not None and self.timestamp is not None and self.signature is not None \
               and self.description is not None
        document = self.json_data()
        document.pop("transaction_id")
        document_str = str(document)

        sha256 = hashlib.sha256()
        sha256.update(document_str.encode('utf-8'))
        transaction_id = sha256.hexdigest()

        self.transaction_id = transaction_id
        return transaction_id

    def get_signing_message_hash(self) -> str:
        document = self.json_data()
        document.pop("signature")
        document.pop("transaction_id")
        document_str = str(document)

        sha256 = hashlib.sha256()
        sha256.update(document_str.encode('utf-8'))
        message_hash = sha256.hexdigest()

        return message_hash

    def json_data(self) -> dict:
        document = {
            "publickey": self.publickey,
            "inputs": [i.json_data() for i in self.inputs],
            "outputs": [i.json_data() for i in self.outputs],
            "description": self.description,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "transaction_id": self.transaction_id,
        }
        return document

    def verify_signature(self) -> bool:
        pubkey = decode_public_key(self.publickey)

        msg = self.get_signing_message_hash()
        msg = bytes.fromhex(msg)
        sign = bytes.fromhex(self.signature)

        try:
            if pubkey.verify(sign, msg):
                return True
        except BadSignatureError:
            pass

        return False

    def verify_transaction(self) -> bool:

        for i in self.inputs:
            if not i.verify_script():
                return False

        transaction_id = self.transaction_id
        if not self.find_transaction_id == transaction_id:
            return False
        return self.verify_signature()

    def get_total_input_value(self) -> float:
        total_input = 0
        for i in self.inputs:
            total_input += i.value
        return total_input

    def get_total_output_value(self) -> float:
        total_output = 0
        for i in self.outputs:
            total_output += i.value
        return total_output
