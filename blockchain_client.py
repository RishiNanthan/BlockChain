import requests
import threading
import time

CONSTANTS = None

class BlockChain_Client:

    def __init__(self):
        self.ip_address = f"{ CONSTANTS.IP }:{ CONSTANT.PORT }"


    def get_invited_transaction(self):

        while True: 
            if not len(CONSTANTS.TRANSACTION_INVITES):
                print("Waiting for invites")
                time.sleep(10)
                continue

            transcaction_ids = CONSTANTS.TRANSACTION_INVITES.keys()

            for transaction_id in transcaction_ids:
                try:
                    address = f"http://{CONSTANTS.TRANSACTION_INVITES}/get_transaction"
                    req = requests.get(address, {"transaction_id": transaction_id})
                    if req.ok:
                        transaction_data = req.json
                        CONSTANTS.BLOCKCHAIN.store_transaction(transaction_data)
                        CONSTANTS.TRANSACTION_INVITES.pop(transaction_id)
                    else:
                        continue
                except Exception:
                    continue


                    
                