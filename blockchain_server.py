
from blockchain.blockchain import BlockChain
from flask import Flask, jsonify, request


IP = "127.0.0.1"
PORT = 8000
CONNECTED_NODES = []
BLOCKCHAIN = BlockChain()


app = Flask(__name__)


@app.route('/')
def index():
    data = {
        "IP_ADDRESS": f"{IP}:{PORT}",
        "CONNECTED_NODES": CONNECTED_NODES,
    }
    return jsonify(data)


@app.route('/invite_for_block')
def invite_for_block():
    block_id = request.args.get("block_id")
    address_to_ask = request.args.get("ip_address")
    print(block_id, address_to_ask)
    print(request.json)  
    return jsonify({})


@app.route('/invite_for_transaction')
def invite_for_transaction():
    transaction_id = request.args.get("transactiom_id")
    address_to_ask = request.args.get("ip_address")
    print(transaction_id, address_to_ask)
    return jsonify({})


@app.route('/get_transaction')
def get_transaction():
    transaction_id = request.args.get('transaction_id')
    return jsonify({})


@app.route('/get_block')
def get_block():
    block_id = request.args.get('block_id')
    return jsonify({})


@app.route('/get_next_block')
def get_next_block():
    cur_block_id = request.args.get('block_id')
    return jsonify({})


@app.route('/create_transaction')
def create_transaction():
    return jsonify({})


app.run(IP, PORT, debug=True)