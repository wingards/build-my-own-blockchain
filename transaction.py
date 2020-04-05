
import json
import binascii
import Crypto.Random as random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from sha import to_sha

class Transaction_Interface:
    def __init__(self, sender_address, private_key, reciever_address, value):
        self.sender_address = sender_address
        self.private_key = private_key
        self.reciever_address = reciever_address
        self.value = value

    def hash_transaction(self):
        return to_sha(self.to_json())

    def transaction_to_dict(self):
        data = data = {'sender_address' : self.sender_address, 'private_key' : self.private_key, 'reciever_address' : self.reciever_address, 'value' : self.value}

        return data

    def to_json(self):
        return json.dumps(self.transaction_to_dict())

    def json_to_dict(self, json_string):
        transaction = json.loads(json_string)
        return transaction

    def to_transaction(self, transaction):

        self.sender_address = transaction.get('sender_address')
        self.private_key = transaction.get('private_key')
        self.reciever_address = transaction.get('reciever_address')
        self.value = transaction.get('value')

    def sign_transaction(self):

        private_key = RSA.importKey(str(self.private_key))
        transaction_hash = self.hash_transaction()

        encrypt = PKCS1_v1_5.new(private_key)
        return encrypt.sign(SHA.new(transaction_hash.encode('ascii')))

class Transaction(Transaction_Interface):
    pass

class Dispatch_List(Transaction_Interface):
    def __init__(self, sender_address, private_key, reciever_address, value):
        super().__init__(sender_address, private_key, reciever_address, value)
        self.deadline = 0


if __name__ == '__main__':
    private_key = RSA.generate(1024, random.new().read)
    public_key = private_key.publickey()
    private_key = private_key.exportKey().decode('ascii')
    address = to_sha(private_key)
    transaction = Transaction(address, private_key, address, 0)
    print(transaction.sign_transaction())

    transaction.to_transaction(transaction.transaction_to_dict())
    print("Transaction Info Before Modified:{}".format(transaction.to_json()))

    transaction_dict = json.loads(transaction.to_json())
    transaction_dict['value'] = 2
    transaction.to_transaction(transaction_dict)

    print("Transaction Info After Modified:{}".format(transaction.to_json()))
