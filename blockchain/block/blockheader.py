from hashlib import sha256
from binascii import unhexlify
'''
Version-A version number to track software/protocol upgrades
Previous Block Hash-A reference to the hash of the previous (parent) block in the chain
Merkle Root-A hash of the root of the merkle tree of this block’s transactions
Timestamp-The approximate creation time of this block (seconds from Unix Epoch)
Difficulty Target-The proof-of-work algorithm difficulty target for this block
Nonce-A counter used for the proof-of-work algorithm
'''

class BlockHeader:
	
	def __init__(self, version: str, previousblockhash: str,  timestamp: str,
		difficulty: float,nonce: int, transactionlist: list):
			self.version = version
			self.previousblockhash = previousblockhash
			self.merkleroot = self.compute_merkleroot(transactionlist)
			self.timestamp = timestamp,
			self.difficulty = difficulty
			self.nonce = nonce

	def __str__(self) -> str:
		return f'''version: {self.version},previousblockhash: {self.previousblockhash},merkleroot: {self.merkleroot},timestamp: {self.timestamp},difficulty: {self.difficulty},nonce: {self.nonce}'''

	def json_data(self) -> dict:
		data = {
			"version":self.version,previousblockhash:self.previousblockhash,
			"merkleroot":self.merkleroot,
			"timestamp":{self.timestamp},
			"difficulty":{self.difficulty},
			"nonce":{self.nonce}
		}

	def little(self,string):
		t= bytearray.fromhex(string)
		t.reverse()
		return ''.join(format(x,'02x') for x in t)

	def compute_merkleroot(self, transactionlist: list) -> str:
		merkleroot = ""
		merklelist = transactionlist.copy()
		newmerklelist = []
		if(len(merklelist) == 0):
			#should raise exception
			pass
		elif(len(merklelist) == 1):
			merkleroot = merklelist [0]
		else:	
			if(len(merklelist)%2 != 0):
				merklelist.append(merklelist[-1])
			while(len(merklelist) != 1):
				newmerklelist = []
				for hashind in range(0,len(merklelist),2):
					combhash = self.little(merklelist[hashind]) + self.little(merklelist[hashind+1] )
					combhash = unhexlify(combhash)
					hash1 = sha256(combhash).hexdigest()
					hash2 = sha256(unhexlify(hash1)).hexdigest()
					newmerklelist.append(hash2)
				merklelist = newmerklelist
			merkleroot = self.little(merklelist[0])
            
		return merkleroot
