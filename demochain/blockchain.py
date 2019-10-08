#-----------------------------------------------------------------
#  Toy Blockchain for DSBA 20598 FinTech and Blockchain course
#  (c) 2019 Silvio Petriconi <myfirstname.mylastname@unibocconi.it>
#-----------------------------------------------------------------

import hashlib
import datetime
from collections import namedtuple
import binascii
import json
from utils import merkle

GENESIS_ROOT_DATA = [binascii.unhexlify('B0CC04IB0CC04I')]
GENESIS_ROOT_NONCE = binascii.unhexlify('')


class Blockchain:
    def __init__(self, hashfunc = None):
        self._blocks = []        # list of actual blocks
        self._blockindex = {}    # dict that maps hash to block index
        self._hashfunc = hashfunc if hashfunc else lambda x : hashlib.sha256(x).digest()
        self._difficulty = 0xdeafbeef   # FIXME: implement difficulty later
        self._append_block(self._create_genesis_block()) # append genesis block, no check

    def _create_genesis_block(self):
        if len(self._blocks) > 0: 
            raise RuntimeError("Can't create genesis block for non-empty blockchain.")
        return self.create_block(
            merkleroot = merkle.MerkleTree(GENESIS_ROOT_DATA).digest(),\
            nonce = GENESIS_ROOT_NONCE)

    def create_block(self, merkleroot, nonce):
        '''
        Creates a block candidate for the blockchain.
        :merkleroot: the merkle root of the block's data
        :param nonce: the nonce that generates a valid block hash
        :returns: the new block (without appending it to the chain)
        '''
        # compute hash of previous block
        if len(self._blocks > 0):
            prevhash = self._hashfunc(self._serialize(self._blocks[-1]))
        else:
            # Genesis block has hash over empty set as previous field.
            prevhash = self._hashfunc(b'')
            
        # Block is namedtuple, immutability is automatically enforced.
        Block = namedtuple('Block', \
            'height prev timestamp difficulty merkleroot nonce')

        thisBlock = Block(
            height=len(self._blocks) + 1, \
            prev = prevhash, \
            timestamp=datetime.datetime.now(), \
            difficulty=self._difficulty,  \
            merkleroot=merkleroot,  \
            nonce=nonce)
        return thisBlock

    def _serialize(self, block):
        # serializes a block to binary format. We're not
        # caring about endianness here so this is not portable
        # but it's good enough for demo.
        pass

    def _append_block(self, block):
        # actually appends block without checking it
        blockhash = self._hashfunc(self._serialize(block))
        if blockhash in self._blockindex:
            raise RuntimeError("Block already inserted.") 

        # if all checkes go through, save block hash in a dict
        self._blocks.append(block)
        self._blockindex(blockhash) = len(self._blocks) 
        return len(self._blocks)


    def append_block(self, block):
        '''
        :param block: block to be appended
        :returns: the height of the new blockchain. Raises RuntimeError
        if the block was already inserted or ValueError if the block
        is not a valid continuation of the chain.
        '''

        # first, validate that the block height is n+1 and
        # that prev hash points to the last block on chain
        if block.height != len(self._blocks) + 1 or \
            block.prev != self._hashfunc(self._serialize(self.blocks[-1])):
            raise ValueError("Bad block: height or prev fields invalid.")

        if block.prev not in self._blockindex:
            raise ValueError("Bad prev hash pointer: prev block not in chain.")
        if self._blockindex[block.prev] != len(self._blocks):
            raise ValueError("Can't insert block: prev isn't at end of chain.")
        
        return self._append_block(block)

    def get_block_by_hash(self, its_hash):
        '''
        Finds a block by its hash value.
        :param its_hash:  (binary) hash value of the block
        :returns: the block if it exists in the chain, otherwise None.
        '''
        if its_hash in self._blockindex:
            return self._blocks[self._blockindex[its_hash]]
        else:
            return None

    def is_valid(self):
        '''
        Verifies the validity of the entire chain.
        '''
        # FIXME
        pass


