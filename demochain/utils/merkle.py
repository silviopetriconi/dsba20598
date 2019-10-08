import hashlib


class MerkleTree:
    '''
    The merkle_tree object represents a Merkle tree and calculates
    Merkle roots, performs Merkle proofs
    :param leaves: leaves (optional) is a list-like object containing
    the leaves of the tree. Leave it None to start with an empty tree.
    :type arg: list
    :param `hashfunc`: A hash function; SHA256 if not specified.
    '''
    def __init__(self, leaves = [], hashfunc = lambda x:hashlib.sha256(x).digest()):
        self._leaves = leaves 
        self._hashfunc = hashfunc

    def digest(self):
        '''
        Digests hashes in the tree and calculates the merkle root.
        :returns: the tree's merkle root, or None if the tree is empty.
        '''
        if len(self._leaves) < 1:
            return None
        hashes = [self._hashfunc(l) for l in self._leaves]
        while len(hashes) > 1:
            if len(hashes) % 2 > 0:
                hashes.append(hashes[-1])
            # build new hashes by hashing over pairs of the current level of the tree
            newhashes = [self._hashfunc(hashes[2*i]+hashes[2*i+1]) for i in range(len(hashes)//2)]
            hashes = newhashes
        # once there is only one hash left, it's done. Return its value as the merkle root.
        return hashes[0]  


