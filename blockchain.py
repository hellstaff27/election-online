import hashlib
import datetime
import copy

class Block():
	def __init__(self, index, timestamp, date, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.date = date
		self.previous_hash = previous_hash
		self.hash = self.hashing()
	def hashing(self):
		key = hashlib.sha256()
		key.update(str(self.index).encode('utf-8'))
		key.update(str(self.timestamp).encode('utf-8'))
		key.update(str(self.date).encode('utf-8'))
		key.update(str(self.previous_hash).encode('utf-8'))
		return key.hexdigest()

class Chain():
	def __init__(self):
		self.blocks = [self.__get_genesis_block()]
	def __get_genesis_block(self):
		return Block(0, datetime.datetime.utcnow(), 'Genesis', 'arbitrary')
	def add_block(self, date):
		return self.blocks.append(Block(len(self.blocks), datetime.datetime.utcnow(), date, self.blocks[len(self.blocks) - 1].hash))
	def get_chain_size(self):
		return len(self.blocks) - 1
	def verify(self, verbose = True):
		flag = True
		for i in range(1, len(self.blocks)):
			if self.blocks[i].index != i:
				flag = False
				if verbose:
					print(f'Wrong block index at block {i}')
			if self.blocks[i - 1].hash != self.blocks[i].previous_hash:
				flag = False
				if verbose:
					print(f'Wrong previous hash at block {i}')
			if self.blocks[i].hash != self.blocks[i].hashing():
				flag = False
				if verbose:
					print(f'Wrong hash at block {i}')
			if self.blocks[i - 1].timestamp >= self.blocks[i].timestamp:
				flag = False
				if verbose:
					print(f'Backdating at block {i}')
		return flag
	def fork(self, head = 'latest'):
		if head in ['latest', 'whole', 'all']:
			return copy.deepcopy(self)
		else:
			c = copy.deepcopy(self)
			c.blocks = c.blocks[0: head + 1]
		return c
	def get_root(self, chain_2):
		min_chain_size = min(self.get_chain_size(), chain_2.get_chain_size())
		for i in range(1, min_chain_size):
			if self.blocks[i] != chain_2.blocks[i]:
				return self.fork(i - 1)
		return self.fork(min_chain_size)