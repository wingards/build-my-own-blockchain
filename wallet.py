
import sys
import copy
import time
import json
import threading
from flask import jsonify

import Crypto.Random as random
from Crypto.PublicKey import RSA

from sha import to_sha
from block import Block
from transaction import Transaction

from node import node
from chain import BlockChain

class Wallet(node.Node_Interface):
    def __init__(self, address = "127.0.0.1", port = 9527, filename : str = None):

        super().__init__(address, port)

        if filename == None:
            self.private_key = RSA.generate(1024, random.new().read)

            fp = open("mykey.txt", "wb")
            fp.write(self.private_key.exportKey('PEM'))
            fp.close()
            print('Generate New Wallet:\n', self.private_key.exportKey())
        else:
            fp = open(filename, "rb")
            private_key = fp.read()
            fp.close()

            self.private_key = RSA.importKey(private_key)
            print('Open Wallet:\n', self.private_key.exportKey().decode('ascii'))

        #[IMPORTANT] Overwrite recieve message
        self.server._response = self._recieve_message

        self.public_key = self.private_key.publickey()
        self.address = to_sha(self.private_key.exportKey().decode('ascii'))

        self.blockchain = BlockChain()
        self._init_connections()
        chains = self.update_chains()

    def _init_connections(self):#Todo
        pass

    def update_chains(self):
        data = {'key':'update', 'value':self.blockchain.chain_length()}
        self.broadcast(json.dumps(data))
        return None

    def broadcast(self, message):
        self.broadcast_message(message)

    def generate_transaction(self, reciever_address, value):
        transaction = Transaction(self.address, self.private_key.exportKey().decode('ascii'), reciever_address, value)
        return transaction.to_json()
        return transaction.hash_transaction()
        return jsonify(transaction.transaction_to_dict())

    def broadcast_transaction(self, transaction):
        data = {'key':'transaction', 'value':transaction}
        self.broadcast(json.dumps(data))

    def mine(self):
        block = self.blockchain.mine()

        #if return value is not none means that it successfully mined a new block
        if block:
            self.broadcast_block(block.block_to_dict())

    def broadcast_block(self, block):
        data = {'key':'block', 'value':block}
        self.broadcast(json.dumps(data))

    def _recieve_message(self, msg):

        message = json.loads(msg)
        key = message['key']
        if key == 'transaction':#new transaction

            transaction_dict = json.loads(message['value'])
            transaction = Transaction()
            transaction.to_transaction(transaction_dict)

            self.blockchain.add_transaction(transaction)
            self.server.server.send_string(msg)

        elif key == 'block':#

            block_dict = json.loads(message['value'])
            block = Block()
            block.to_block(block_dict)

            if self.blockchain.get_last_hash() != block.previous_hash:
                self.server.server.send_string("1")
            elif self.blockchain.chain_length != block.block_number:
                self.server.server.send_string("2")
            elif self.blockchain.mining_validation(block.previous_hash, block.nonce, self.blockchain.get_difficulty(block.block_number)) == False:
                self.server.server.send_string("3")
            else:
                self.blockchain.add_block(block)
                self.server.server.send_string("0")

        elif key == 'update':

            length = message['value']
            if length < self.blockchain.chain_length():#remote chain shorter than local
                data = {'key':'chain', 'value':self.blockchain.chain_to_dict()}
            else:#update local
                data = {'key':'update', 'value':self.blockchain.chain_length()}
            self.server.server.send_string(json.dumps(data))

        elif key == 'chain':

            chain, transaction = self.blockchains.to_chains(message['value'])
            if count(chain) > self.blockchain.chain_length() and self.blockchain.chain_validation(chain) == True:
                print('Replace local chains with remote longest chain with length:{}\n'.format(count(chain)))
                self.blockchain._to_chains(message['value'])

    def _recieve(self):
        while True:
            if not self.query_message:
                time.sleep(0.001)
                continue

            messages = copy.deepcopy(self.query_message)
            self.query_message.clear()

            for message in messages:
                self._recieve_message(message)

    def recieve(self):
        thread = threading.Thread(target = self._recieve, args=())
        thread.start()

if __name__ == '__main__':

    if len(sys.argv) == 1:
        wallet = Wallet()
    elif len(sys.argv) == 2:
        wallet = Wallet(filename = sys.argv[1])

    transaction = wallet.generate_transaction(wallet.address, 0)

    wallet.listen()
    wallet.broadcast_transaction(transaction)
