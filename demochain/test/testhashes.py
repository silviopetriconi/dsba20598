import unittest
import hashlib
import binascii

from utils.cryptohash import merkle_tree


RANDOMDATA_HEX = [
'db3e68ef01baa018d3aa4c8d37f5c044c56b5b399967606660353fd4519aba63',
'433c5bab332f40f1e1bfddcfc668f91f7a52c5912e3d37ffe906b0d0aa5a7532',
'eb47d9f3a6c379b5c5a3792312251fce8213b7d7179d108feddb462b074f96c8',
'3c9a87a39900c2b0813325051bc9d058c0d64fbb7987ce4e72489a73314f1c02',
'93e99ac4b00d21a57d0d995d107cecbb7ab01a5a296e5a5ebcec35f9c884c582',
]

RANDOMDATA_BINARY = [binascii.unhexlify(i) for i in RANDOMDATA_HEX]


class TestMerkleTree(unittest.TestCase):

	def test_empty_merkle_tree(self):
		mtree = merkle_tree()
		self.assertTrue(mtree.digest() is None)

	def test_simple_merkle_tree(self):
		mtree = merkle_tree(RANDOMDATA_BINARY[0:2])
		sha256 = lambda x : hashlib.sha256(x).digest()
		hashes = [sha256(x) for x in RANDOMDATA_BINARY[0:2]]
		self.assertEqual(mtree.digest(), hashlib.sha256(hashes[0]+hashes[1]).digest())
		
