#-----------------------------------------------------------------
#  Toy Blockchain for DSBA 20598 FinTech and Blockchain course
#  (c) 2019 Silvio Petriconi <myfirstname.mylastname@unibocconi.it>
#  License: GNU General Public License 3.0
#-----------------------------------------------------------------

import hashlib
import datetime
from collections import namedtuple
import binascii
import json
from utils import merkle
import struct

GENESIS_ROOT_DATA = [binascii.unhexlify('0000DEADBEEFBADCAFFEBAADF00D')]
GENESIS_ROOT_NONCE = 0
GENESIS_NONCE = 101  # FIXME
GENESIS_DIFFICULTY = 1   

# Every block header is a namedtuple, immutability is automatically enforced.
Blockheader = namedtuple('Blockheader', \
    'height prev timestamp difficulty merkleroot nonce')

# Data for the genesis block. It has no previous, so the prev hash is zero.
_genesisblock = Blockheader(
    height = 0,
    prev = binascii.unhexlify('0000000000000000000000000000000000000000000000000000000000000000'),
    timestamp = 1572328964,
    difficulty = GENESIS_DIFFICULTY,
    merkleroot = merkle.MerkleTree(GENESIS_ROOT_DATA).digest(),
    nonce = GENESIS_NONCE
)


class Blockchain:
    def __init__(self, genesis = _genesisblock, hashfunc = None):
        self._blockhdrs = []     # list of block headers
        self._blockindex = {}    # dict that maps blockheader hash to index
        self._hashfunc = hashfunc if hashfunc else lambda x : hashlib.sha256(x).digest()
        self._difficulty = GENESIS_DIFFICULTY 
        self._append_block(genesis) # append genesis block

    def create_blockheader(self, merkleroot, nonce):
        '''
        Creates a block candidate for the blockchain.
        :merkleroot: the merkle root of the block's data
        :param nonce: the nonce that generates a valid block hash
        :returns: the new block (without appending it to the chain)
        '''
        # compute hash of previous block
        if len(self._blockhdrs) > 0:
            prevhash = self._hashfunc(self._serialize_hdr(self._blockhdrs[-1]))
        else:
            # Genesis block has hash over empty set as previous field.
            prevhash = self._hashfunc(b'')

        thisBlock = Blockheader(
            height=len(self._blockhdrs), \
            prev = prevhash, \
            timestamp=int(datetime.datetime.now().timestamp()), \
            difficulty=self._difficulty,  \
            merkleroot=binascii.hexlify(merkleroot),  \
            nonce=nonce)
        return thisBlock

    def _serialize_hdr(self, blockhdr):
        # serializes a block header to binary format (big endian):
        # struct Blockheader {
        #     uint64             height;
        #     char[32]           prev;
        #     uint64             timestamp;
        #     uint64             difficulty;
        #     char[32]           merkleroot;
        #     uint64             nonce; 
        # }
        return struct.pack(">I32sII32sI", *blockhdr)

    def _deserialise_hdr(self, bindata):
        # returns a block header from serialized binary data, without
        # checking its validity in any way
        return Blockheader._make(struct.unpack(">I32sII32sI", bindata))

    def _append_block(self, blockheader):
        # actually appends block header without checking it
        blockhash = self._hashfunc(self._serialize_hdr(blockheader))
        if blockhash in self._blockindex:
            raise RuntimeError(f"Block {blockhash} already inserted.") 
        print("Block hash: ", blockhash)

        # if all checkes go through, save block hash in a dict
        blockheight = len(self._blockhdrs) 
        self._blockindex[blockhash] = blockheight
        self._blockhdrs.append(blockheader)
        return blockheight

    def can_append(self, block, diagnostics=False):
        '''
        Checks whether a candidate block is valid and can be
        appended to the chain. 
        :param block: candidate block to be verified
        :param diagnostics: if set True, returns diagnostics
        :returns: True if block is valid, False otherwise. If
        diagnostics is True, returns a tuple (valid, errorstring).
        '''
        if block.height != len(self._blockhdrs) or \
            block.prev != self._hashfunc(self._serialize_hdr(self._blockhdrs[-1])):
            return (False, "Bad block: block height or prev block invalid.") \
                if diagnostics else False
        
        if block.prev not in self._blockindex:
            return(False, "Bad prev hash pointer: prev block not in chain.") \
                if diagnostics else False

        if self._blockindex[block.prev] != len(self._blockhdrs)-1:
            return(False, "Can't append block: prev isn't at end of chain.") \
                if diagnostics else False
        
        # then, check that difficulty is set appropriately
        if self._difficulty != block.difficulty:
            return(False, "Block difficulty is not at current level.") \
                if diagnostics else False

        if not self._blockhash_matches_difficulty(block):
            raise ValueError("Block hash POW not commensurate to difficulty.")
        
        return (True,'') if diagnostics else True


    def append_block(self, block):
        '''
        :param block: block to be appended
        :returns: the height of the new blockchain. Raises RuntimeError
        if the block was already inserted or ValueError if the block
        is not a valid continuation of the chain.
        '''

        # first, validate that the block height is n+1 and
        # that prev hash points to the last block on chain
        append_ok, errormsg = self.can_append(block, diagnostics=True)

        if not append_ok:
            raise ValueError(errormsg)

        return self._append_block(block)

    def _blockhash_matches_difficulty(self, blockhdr):
        hexHashstring = str(binascii.hexlify(self._hashfunc(self._serialize_hdr(blockhdr))))
        return hexHashstring.startswith('0'*self._difficulty)

    def get_block_by_hash(self, its_hash):
        '''
        Finds a block by its hash value.
        :param its_hash:  (binary) hash value of the block
        :returns: the block if it exists in the chain, otherwise None.
        '''
        if its_hash in self._blockindex:
            return self._blockhdrs[self._blockindex[its_hash]]
        else:
            return None

    def is_valid(self):
        '''
        Verifies the validity of the entire chain.
        '''
        # FIXME
        pass

    def get_block(self, n):
        '''
        Obtains a block.
        :param n: the index of the block to be obtained
        :returns: the n-th block in the chain (0=genesis), None if not existent
        '''
        return self._blockhdrs[n] if n < len(self._blockhdrs) else None




if __name__=='__main__':
    B = Blockchain()
    nonce = 0
    while True:
        g = Blockheader(height=_genesisblock.height,
            prev=_genesisblock.prev,
            timestamp = _genesisblock.timestamp,
            difficulty=_genesisblock.difficulty,
            merkleroot=_genesisblock.merkleroot,
            nonce=nonce)
        print (f"Nonce: {nonce} Hash: ", binascii.hexlify(B._hashfunc(B._serialize_hdr(g))))
        if B._blockhash_matches_difficulty(g):
            print ("======= FOUND GENESIS NONCE: =========", nonce)
            break
        nonce += 1
    
    
