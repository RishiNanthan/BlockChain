
from blockchain.blockchain import BlockChain
from flask import Flask, jsonify, request


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


@app.route('/')
def index():
    data = {
        "IP_ADDRESS": f"{ IP }:{ PORT }",
        "CONNECTED_NODES": CONNECTED_NODES,
    }
    return jsonify(data)


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


@app.route('/create_transaction')                     #   To be completed
def create_transaction():
    return jsonify({})


@app.route('/add_node')
def add_node():
    address = request.args.get('ip_address')
    CONNECTED_NODES.push(address)
    return jsonify(ACK_MSG)


def run_server(debug=True):
    app.run(IP, PORT, debug=debug)
