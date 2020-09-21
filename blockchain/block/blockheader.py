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
	

	def __init__(self, block ):
			assert(block != None)
			document = block.json_data()
			self.version = document.get("version")
			self.previous_block = document.get("previous_block")
			self.transactions = document.get("transactions")
			self.merkleroot = self.compute_merkleroot(self.transactions)
			self.timestamp = document.get("timestamp")
			self.difficulty = document.get("difficulty")
			self.nonce = document.get("nonce")


	def json_data(self) -> dict:
		data = {
			"version":self.version,previous_block:self.previous_block,
			"merkleroot":self.merkleroot,
			"timestamp":{self.timestamp},
			"difficulty":{self.difficulty},
			"nonce":{self.nonce}
		}


	def little(self,string):
		t= bytearray.fromhex(string)
		t.reverse()
		return ''.join(format(x,'02x') for x in t)
	

	def compute_merkleroot(self, transactions: list) -> str:
		merkleroot = ""
		merklelist = transactions.copy()
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


	def __str__(self) -> str:
		return str(self.json_data())

