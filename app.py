from hashlib import sha256
import json
import time
from xml.etree.ElementTree import TreeBuilder
from flask import Flask, request
import requests
from random import seed, random
import random
import string
from blockchain import Blockchain, Block
# curl  http://127.0.0.1:4000/check_validity

seed(0)
# Random Transactions generator
def random_alphanumeric(length, char_set = string.ascii_letters):

    return ''.join( random.choice(char_set) for _ in range(length) )

app =  Flask(__name__)
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block(): 

    for t in range(random.randint(0, 5)):
        blockchain.add_new_transaction(random_alphanumeric(random.randint(10, 30)))
        
    block = blockchain.mine()
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"chain": chain_data})

# Mining a new block
@app.route('/chain_validity', methods=['GET'])
def chain_validity(): 
    if blockchain.check_chain_validity() == True:
        return "VALID"
    elif blockchain.check_chain_validity() == False:
        return "INVALID"



@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})
app.run(debug = True, port = 4000)