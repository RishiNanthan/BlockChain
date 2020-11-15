import requests
import threading
import time
from blockchain.blockchain import BlockChain

# General Constants for main.py, blockchain_server.py
IP = None
PORT = None
CONNECTED_NODES = []
BLOCKCHAIN = BlockChain()
BLOCK_INVITES = []
TRANSACTION_INVITES = []

# Constants for this file

TRANSACTION_COUNT_PER_BLOCK = 10

class BlockChain_Client:

    def __init__(self):
        self.ip_address = f"{ IP }:{ PORT }"


    def get_invited_transaction(self):

        while True: 
            if not len( TRANSACTION_INVITES ):
                print("Waiting for invites")
                time.sleep(10)
                continue

            for transaction in TRANSACTION_INVITES:
                transaction_id = transaction["transaction_id"]
                ip_address = transaction["ip_address"]
                try:
                    address = f"http://{ ip_address }/get_transaction"
                    req = requests.get(address, {"transaction_id": transaction_id})
                    if req.ok:
                        transaction_data = req.json
                        BLOCKCHAIN.store_transaction(transaction_data)
                        TRANSACTION_INVITES.pop(transaction)
                    else:
                        continue
                except Exception:
                    continue


    def get_invited_block(self):

        while True:
            if not len( BLOCK_INVITES ):
                print("Waiting for BLOCK invites")
                time.sleep(10)
                continue

            for block in BLOCK_INVITES:
                block_id = block["block_id"]
                ip_address = block["ip_address"]
                try:
                    address = f"http://{ ip_address }/get_block"
                    req = requests.get(address, {"block_id": block_id})
                    if req.ok:
                        block_data = req.json
                        BLOCKCHAIN.store_block(block_data)
                        BLOCK_INVITES.pop(block)
                    else:
                        continue
                except Exception:
                    continue


    def send_transaction_invite(self, transaction_id: str):
        for nodes in CONNECTED_NODES:
            address = f"http://{ node }/invite_for_transaction"
            print(f"Sending Transaction invite to { node }")
            try:
                req = requests.get(address, {
                    'transaction_id': transaction_id,
                    'ip_address': f"{ IP }:{ PORT }"
                })
            except Exception as e:
                print(e)
                

    def send_block_invite(self, block_id: str):
        for nodes in CONNECTED_NODES:
            address = f"http://{ node }/invite_for_block"
            print(f"Sending Block invite to { node }")
            try:
                req = requests.get(address, {
                    'block_id': block_id,
                    'ip_address': f"{ IP }:{ PORT }"
                })
            except Exception as e:
                print(e)


    def start_mining(self):
        print("Mining Started")
        while True:
            block_hash = BLOCKCHAIN.mine_block(transaction_count=TRANSACTION_COUNT_PER_BLOCK)
            if block_hash is not None:
                self.send_block_invite(block_hash)



def run_client(mining=True):
    client = BlockChain_Client()
    threading.Thread(target=client.get_invited_transaction, name="Transaction invites processing thread").start()
    threading.Thread(target=client.get_invited_block, name="Block invites processing thread").start()
    if mining:
        threading.Thread(target=client.start_mining, name="Mining thread").start()
