import json
from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
    #return blockchain.__repr__()
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'
    blockchain.add_block(transaction_data)
    
    return jsonify(blockchain.chain[-1].to_json())

app.run(port=5001)
