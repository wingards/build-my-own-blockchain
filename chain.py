
from time import sleep

import json
from sha import to_sha
from block import Block

class BlockChain:
    def __init__(self):
        self.chains = []
        self.transactions = []

        self.savename = "mychain.txt"

        try:
            with open(self.savename) as fp:
                print("Initialize block chain from local data")
                self._to_chains(self.json_to_dict(fp.read()))
        except IOError:
            self.init_chain()

    def chain_length(self):
        return len(self.chains)

    def get_chains(self):
        return self.chains

    def init_chain(self):
        print("initialize block chain with genesis block")
        genesis_block = Block(0, 0, 0, [])
        self.add_block(genesis_block)

    def clear_chain(self):
        self.chains.clear()
        self.transactions.clear()

    def save_chain(self):
        with open(self.savename, "w") as fp:
            fp.write(self.to_json())

    def chain_to_dict(self):
        chains = []
        for block in self.chains:
            chains.append(block.block_to_dict())

        transactions = []
        for transaction in self.transactions:
            transactions.append(transaction.transaction_to_dict())

        data = {'chains' : chains, 'transactions' : transactions}
        return data

    def to_json(self):
        return json.dumps(self.chain_to_dict())

    def json_to_dict(self, json_string):
        return json.loads(json_string)

    def to_chains(self, data):

        chains = data['chains']
        transactions = data['transactions']

        chain = []
        for block_dict in chains:
            block = Block(0, 0, 0, [])
            block.to_block(block_dict)
            chain.append(block)

        transaction = []
        for transaction_dict in transactions:
            transaction = Transaction(None, None, None, 0)
            transaction.to_transaction(transaction_dict)
            transaction.append(transaction)

        return chain, transaction

    def _to_chains(self, chain):

        self.clear_chain()

        self.chains, self.transactions = self.to_chains(chain)

    def get_difficulty(self, block_height):
        return 1

    def mining_validation(self, block_hash, nonce, difficulty):
        string = str(block_hash) + str(nonce)
        string_hash = to_sha(string)
        return string_hash[:difficulty] == '0'*difficulty

    def chain_validation(self, chains = None):

        if not chains:
            chains = self.chains

        print("Start blockchain Validation")

        last_hash = chains[0].hash_block()

        for block in chains[1:]:
            if last_hash != block.previous_hash:
                print("Validate failed at block {} with hash value error".format(block.block_number))
                return False

            if self.mining_validation(block.previous_hash, block.nonce, self.get_difficulty(block.block_number)) == False:
                print("Validate failed at block {} with validatation error".format(block.block_number))
                return False

            last_hash = block.hash_block()

        print("Validation Pass. Validate Totally {} blocks".format(len(chains[1:])))
        return True

    def proof_of_work(self):
        last_block = self.chains[-1]
        last_hash = last_block.hash_block()

        nonce = 0

        while True:
            if self.mining_validation(last_hash, nonce, 1) is False:
                if last_block != self.chains[-1]:
                    return -1
                nonce += 1
                sleep(0.001)
            else:
                break

        return nonce

    def add_block(self, block):
        self.chains.append(block)

        self.save_chain()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

        self.save_chain()

    def mine(self):
        last_block = self.chains[-1]
        last_hash = last_block.hash_block()

        nonce = self.proof_of_work()

        if nonce < 0:
            return None

        next_block = Block(len(self.chains), nonce, last_hash, self.transactions)

        self.add_block(next_block)

        return next_block

    def list_blocks_hash(self):

        chains = []

        for i in range(1, len(self.chains)):
            chains.append(self.chains[i].previous_hash)

        chains.append(self.chains[-1].hash_block())

        return chains

if __name__ == '__main__':
    blockchain = BlockChain()

    blockchain.mine()
    blockchain.mine()

    print(blockchain.list_blocks_hash())

    if blockchain.chain_validation() == True:
        pass

    print(blockchain.to_json())

    chain_dict = blockchain.chain_to_dict()
    chain_dict['chains'][1]['nonce'] = 100

    blockchain._to_chains(chain_dict)

    if blockchain.chain_validation() == True:
        pass
