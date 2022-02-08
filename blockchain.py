from hashlib import sha256
import json
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def hash_computation(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # Number of zeroes that hash starts with
    N_zeros = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis()

    def create_genesis(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.hash_computation()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def create_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is a valid hash of block and satisfies
        the number of zeros criteria.
        """
        return (block_hash.startswith('0' * Blockchain.N_zeros) and
                block_hash == block.hash_computation())

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our Number of zeros criteria.
        """
        block.nonce = 0

        computed_hash = block.hash_computation()
        while not computed_hash.startswith('0' * Blockchain.N_zeros):
            block.nonce += 1
            computed_hash = block.hash_computation()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.create_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index
    
    def check_chain_validity(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if(current.hash != current.hash_computation()):
                print("The current hash of the block does not equal the generated hash of the block.")
                return False
            if(current.previous_hash != previous.hash_computation()):
                print("The previous block's hash does not equal the previous hash value stored in the current block.")
                return False
        return True



