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
def random_transaction():
    names = ["Alice", "Bob", "Mallory", "Jack", "Dina", "Ehab", "Mahmoud", "Salma", "Mazen", "Hesham"]
    transaction = {"sender": names[random.randint(0,len(names)-1)],
    "receiver": names[random.randint(0,len(names)-1)],
    "amount": random.randint(10, 1000) }

    return transaction

app =  Flask(__name__)
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block(): 

    for t in range(random.randint(0, 5)):
        blockchain.add_new_transaction(random_transaction())
        
    block = blockchain.mine()
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"chain": chain_data})

# Mining a new block
@app.route('/attack', methods=['GET'])
def attack(): 

    for t in range(random.randint(0, 5)):
        blockchain.add_new_transaction(random_transaction())
        
    block = blockchain.mine()
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    blockchain.chain[1].transactions = "fake_transactions"

    if blockchain.check_chain_validity() == True:
        return "VALID CHAIN"
    elif blockchain.check_chain_validity() == False:
        return "ATTACK - INVALID CHAIN"


# Check if chain is invalid
@app.route('/chain_validity', methods=['GET'])
def chain_validity(): 
    if blockchain.check_chain_validity() == True:
        return "VALID CHAIN"
    elif blockchain.check_chain_validity() == False:
        return "INVALID CHAIN"



@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})
app.run(debug = True, port = 4000)