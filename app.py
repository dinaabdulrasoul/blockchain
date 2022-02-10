import json
import copy
from flask import Flask
from random import seed, random
import random
from blockchain import Blockchain
# curl  http://127.0.0.1:4000/mine_blocks

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
replica = Blockchain()


# Mining a new block
@app.route('/mine_blocks', methods=['GET'])
def mine_blocks():
    global blockchain
    global replica
    attacker_compute_power = 0.3 ## the higher this value is, the lower the security of the system
    while True:
        p = random.random()
        if p > attacker_compute_power:
            for t in range(random.randint(0, 5)):
                blockchain.add_new_transaction(random_transaction())
                
            block = blockchain.mine()
        else:
            for t in range(random.randint(0, 5)):
                replica.add_new_transaction(random_transaction())
                
            block = replica.mine()
        
        if len(blockchain.chain) - len(replica.chain) > 5:
            print("block chain won")
            replica = copy.deepcopy(blockchain)
            break
        elif len(replica.chain) - len(blockchain.chain) > 5:
            print("attacker says haha!")
            blockchain = copy.deepcopy(replica)
            break
    
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"chain": chain_data})
    

# Simple attack
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


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})
app.run(debug = True, port = 4000)