import unittest
import hashlib
import binascii

from blockchain import Blockchain, Blockheader


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.B = Blockchain()
        

    def test_serialize_deserialize_blockhdr(self):
        somehash = hashlib.sha256(b"Just a test").digest()
        anotherhash = hashlib.sha256(b"Another one").digest()
        testhdr = Blockheader(height=191, \
            prev=somehash, 
            timestamp=65535, 
            difficulty=100, 
            merkleroot=anotherhash, 
            nonce=99)
        bindata = self.B._serialize_hdr(testhdr)
        # now see if one can recover the same block from the serialized data
        result = self.B._deserialise_hdr(bindata)
        self.assertEqual(result.height, 191)
        self.assertEqual(result.timestamp, 65535)
        self.assertEqual(result.difficulty, 100)
        self.assertEqual(result.prev, somehash)
        self.assertEqual(result.merkleroot, anotherhash)
        self.assertEqual(result.nonce, 99)


    def test_more(self):
        pass
    

    