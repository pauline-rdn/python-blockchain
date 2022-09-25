from email import message
import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-d85de339-f3d8-4162-9062-796ffa1b338b'
pnconfig.publish_key = 'pub-c-9938880e-990e-4726-a0b7-2fe1a5c70bb6'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:] #[ 0:len(self.blockchain.chain)]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
                print(f'\n-- Successfully replaced the local chain: {e}')
            except Exception as e:
                print(f'\n-- Did not replace chain: {e}')
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n -- Set the new transaction in the transaction pool')


class PubSub():
    """
    Handles the publish/subscribe layer of the app.
    Provides communication between the nodes of the Blockchain network
    """
    
    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels([CHANNELS.values()]).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes
        """

        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes
        """

        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())

def main():
    pubsub = PubSub()

    # make sure that pubnub.publish() doesn't occur until time.sleep() finishes
    time.sleep(1)
    
    pubsub.publish(CHANNELS['TEST'], { 'foo' : 'bar' })

if __name__=='__main__':
    main()



