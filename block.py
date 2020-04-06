
import json
from time import time

from sha import to_sha
from transaction import Transaction

class Block:
    def __init__(self, block_number = None, nonce = None, previous_hash = None, transactions = None):
        self.timestamp = time()
        self.block_number = block_number
        self.nonce = nonce
        self.previous_hash = previous_hash

        self.transactions = transactions

    def hash_block(self):
        return to_sha(self.to_json())

    def block_to_dict(self):
        
        transactions = []
        for transaction in self.transactions:
            transactions.append(transaction.transaction_to_dict())

        data = {'timestamp' : self.timestamp, 'block_number' : self.block_number, 'nonce' : self.nonce, 'previous_hash' : self.previous_hash, 'transactions' : transactions}

        return data

    def to_json(self):
        return json.dumps(self.block_to_dict())

    def json_to_dict(self, json_string):
        return json.loads(json_string)

    def to_block(self, block):

        self.timestamp = block['timestamp']
        self.block_number = block['block_number']
        self.nonce = block['nonce']
        self.previous_hash = block['previous_hash']
        
        transactions = []
        for transaction_dict in block['transactions']:
            transaction = Transaction()
            transaction.to_transaction(transaction_dict)
            transactions.append(transaction)
        self.transactions = transactions

if __name__ == '__main__':

    transactions = []
    transaction = Transaction()
    transactions.append(transaction)

    block = Block(0, 0, 0, transactions)
    print(block.hash_block())

    print("Block info Before Modified:{}".format(block.to_json()))

    block_dict = json.loads(block.to_json())
    block_dict['nonce'] = 1

    block_dict['transactions'][0]['value'] = 1

    block.to_block(block_dict)

    print("Block info After Modified:{}".format(block.to_json()))
