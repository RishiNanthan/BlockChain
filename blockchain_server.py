
from blockchain.blockchain import BlockChain
from flask import Flask, jsonify, request, render_template, url_for

import random


IP = None
PORT = None
CONNECTED_NODES = []
BLOCKCHAIN = BlockChain()
BLOCK_INVITES = []
TRANSACTION_INVITES = []


ACK_MSG = {
    "acknowledged": True,
}


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    """
    data = {
        "IP_ADDRESS": f"{ IP }:{ PORT }",
        "CONNECTED_NODES": CONNECTED_NODES,
    }
    return jsonify(data)
    """
    return render_template("index.html")


@app.route('/connect')
def connect():
    ip = request.args.get("ip_address")
    CONNECTED_NODES.append(ip)
    return jsonify(ACK_MSG)


@app.route('/invite_for_block')
def invite_for_block():
    block_id = request.args.get("block_id")
    address_to_ask = request.args.get("ip_address")
    print(block_id, address_to_ask)
    if BLOCKCHAIN.get_block(block_id) is not None:
        BLOCK_INVITES[block_id] = address_to_ask
    return jsonify(ACK_MSG)


@app.route('/invite_for_transaction')
def invite_for_transaction():
    transaction_id = request.args.get("transaction_id")
    address_to_ask = request.args.get("ip_address")
    print(transaction_id, address_to_ask)
    if BLOCKCHAIN.get_transaction(transaction_id) is not None:
        TRANSACTION_INVITES[transaction_id] = address_to_ask
    return jsonify(ACK_MSG)


@app.route('/get_transaction')
def get_transaction():
    transaction_id = request.args.get('transaction_id')
    transaction_data = BLOCKCHAIN.get_transaction(transaction_id)
    return jsonify(transaction_data)


@app.route('/get_block')
def get_block():
    block_id = request.args.get('block_id')
    block_data = BLOCKCHAIN.get_block(block_id)
    return jsonify(block_data)


@app.route('/get_next_block')                         #   To be completed
def get_next_block():
    cur_block_id = request.args.get('block_id')
    return jsonify({})


@app.route('/create_transaction', methods=["POST"])                     #   To be completed
def create_transaction():
    print(request.get_data())
    return jsonify({})


@app.route("/create_address") 
def create_address():
    public_key, private_key = BlockChain.generate_keys()
    data = {
        "public_key": public_key,
        "private_key": private_key,
    }
    return jsonify(data)


@app.route("/get_client_transactions")                 # To be completed
def get_client_transactions():
    transaction = {
        "transaction_id": "fgdjAGFUGu" + str(random.randrange(5000)),
        "description": "Hello World",
        "public_key": "dgyZGGuf",
        "signature": "fgvujAGFU",
        "timestamp": "17-01-2000 12:00:00",
        "inputs": [
            {
                "previous_transaction": "gfkbgbghg",
                "index": 0,
                "value": random.randrange(0, 500),
                "script": "OP_CHKSIG SIG",
            }
        ],
        "outputs": [
            {
                "value": 4.5,
                "script": "OP_CHKSIG",
            },
        ],
    }

    data = {
        "transactions": [transaction],
    }
    return jsonify(data)



def run_server():
    app.run(IP, PORT, debug=False)
