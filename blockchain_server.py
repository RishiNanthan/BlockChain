
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
    return jsonify({})


app.run(IP, PORT, debug=True)