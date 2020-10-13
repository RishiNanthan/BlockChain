
from blockchain.blockchain import BlockChain
from flask import Flask, jsonify, request


CONSTANTS = None


ACK_MSG = {
    "acknowledged": True,
}


app = Flask(__name__)


@app.route('/')
def index():
    data = {
        "IP_ADDRESS": f"{ CONSTANTS.IP }:{ CONSTANTS.PORT }",
        "CONNECTED_NODES": CONSTANTS.CONNECTED_NODES,
    }
    return jsonify(data)


@app.route('/invite_for_block')
def invite_for_block():
    block_id = request.args.get("block_id")
    address_to_ask = request.args.get("ip_address")
    print(block_id, address_to_ask)
    if CONSTANTS.BLOCKCHAIN.get_block(block_id) is not None:
        CONSTANTS.BLOCK_INVITES[block_id] = address_to_ask
    return jsonify(ACK_MSG)


@app.route('/invite_for_transaction')
def invite_for_transaction():
    transaction_id = request.args.get("transaction_id")
    address_to_ask = request.args.get("ip_address")
    print(transaction_id, address_to_ask)
    if CONSTANTS.BLOCKCHAIN.get_transaction(transaction_id) is not None:
        CONSTANTS.TRANSACTION_INVITES[transaction_id] = address_to_ask
    return jsonify(ACK_MSG)


@app.route('/get_transaction')
def get_transaction():
    transaction_id = request.args.get('transaction_id')
    transaction_data = CONSTANTS.BLOCKCHAIN.get_transaction(transaction_id)
    return jsonify(transaction_data)


@app.route('/get_block')
def get_block():
    block_id = request.args.get('block_id')
    block_data = CONSTANTS.BLOCKCHAIN.get_block(block_id)
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
    CONSTANTS.CONNECTED_NODES.push(address)
    return jsonify(ACK_MSG)


def run_app(debug=True):
    IP = input("Enter IP Address: ")
    PORT = int(input("Enter PORT Number: "))
    app.run(IP, PORT, debug=debug)
