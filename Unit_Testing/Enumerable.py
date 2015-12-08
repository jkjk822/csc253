import re
import copy

class Enumerable(list):
	default = lambda x: x #default func for methods that return
	defaultPrint = lambda x: print(x) #default func for methods that don't return
	compare = lambda x,y: 1 if x>y else -1 #default compare func
	sentinel = "sentinel#a93c64479e2661bf7b17e10859fb4e67dbe1a945" #(hopefully) unique sentinel value
	'''
	Passes each element of the collection to the given block.
	The method returns True if the block never returns False or None.
	If the block is not given, adds an implicit block of lambda x: x
	which will cause all to return True when none of the collection
	members are False or None.
	'''
	def all(self, block=default):
		for x in self:
			if not block(x):
				return False
		return True

	'''
	Passes each element of the collection to the given block.
	The method returns True if the block ever returns True.
	If the block is not given, adds an implicit block of lambda x: x
	that will cause any to return True if at least one of the collection
	members is not False or None.
	'''
	def any(self, block=default):
		for x in self:
			if block(x):
				return True
		return False

	'''
	Returns a new Enumerable with the results of running block once for
	every element in self.
	If no block is given, adds an implicit block of lambda x: x, which
	will cause collect to return a new Enumerable with all the non False and
	None elements.
	'''
	def collect(self, block=default):
		collected = []
		for x in self:
			collected.append(block(x))
		return Enumerable(collected)

	'''
	Returns a new Enumerable with the concatenated results of running block
	once for every element in self.
	If no block is given, adds an implicit block of lambda x: [x], which
	will cause collect_concat to return a new Enumerable with all the non False
	and	None elements.
	'''
	def collect_concat(self, block=lambda x: [x]):
		collected = []
		for x in self:
			collected.extend(block(x))
		return Enumerable(collected)

	'''
	Returns the number of items in self through enumeration.
	If an argument is given, the number of items in self that are equal to item
	are counted.
	If a block is given, it counts the number of elements yielding a true value.
	'''
	def count(self, block=lambda x: True):
		num = 0
		if not callable(block):
			block = lambda x: x == block
		for x in self:
			if block(x):
				num += 1
		return num

	'''
	Calls block for each element of self repeatedly n times or forever if none or
	None is given. If a non-positive number is given or the collection is empty,
	does nothing. Returns None if the loop has finished without getting interrupted.
	If no block is given, adds an implicit block of lambda x: print(x)
	that will cause cycle to print each element of self.
	Terminates when Python's maximum recursion depth is reached, prints "... forever"
	and returns -1.
	'''
	def cycle(self, n=float("inf"), block=defaultPrint):
		if n is None:
			n = float("inf")
		if n < 1:
			return None
		for x in self:
			block(x)
		try:			
			return self.cycle(n-1, block)
		except RuntimeError as e:
			if str(e) == "maximum recursion depth exceeded":
				print("... forever")
				return -1

	'''
	Passes each entry in self to block.
	Returns the first for which block is not False. If no object matches, returns
	ifnone (called if a function) and returns its result when it is specified, or
	returns None otherwise.
	If no block is given, adds an implicit block of lambda x: x
	that will cause detect the first non False element.
	'''
	def detect(self, block=default, ifnone=None):
		for x in self:
			if block(x) != False:
				return x
		if callable(ifnone):
			return ifnone()
		return ifnone

	def drop(self, n):
		return Enumerable(self[n:])

	def drop_while(self, block=default): #no block: drop False/None values
		for x in self:
			if not block(x):
				return self.drop(self.find_index(x))
		return Enumerable([])

	def each_cons(self, n, block=defaultPrint): #no block: print cons lists
		for x in self:
			i = self.find_index(x)
			if (i+n)<=len(self):
				block(Enumerable([self[i+j] for j in range(n) if (i+j)<len(self)]))

	def each_entry(self, block=defaultPrint): #no block: print entries
		for x in self:
			block(x)
		return self

	def each_slice(self, n, block=defaultPrint): #no block: print sliced lists
		for _ in range(n):
			block(self.take(n))
			self = self.drop(n)

	def each_with_index(self, block=lambda x, i: print((x,i))): #no block: print item and index
		for i, x in enumerate(self):
			block(x, i)
		return self

	def each_with_object(self, obj, block): #no block: error
		for x in self:
			block(x, obj)
		return obj

	def entries(self):
		return self

	def find(self, block=default, ifnone=None): #no block: see detect
		return self.detect(block, ifnone)

	def find_all(self, block=default): #no block: return list of all True values
		return Enumerable([x for x in self if block(x)])

	def find_index(self, block): #no block: error
		if not callable(block):
			temp = block
			block = lambda x: x == temp
		for i, x in enumerate(self):
			if block(x) != False:
				return i

	def first(self, n=None):
		if n != None:
			return self.take(n)
		return self[0] if len(self)>0 else None

	def flat_map(self, block=lambda x: [x]): #no block: see collect_concat
		return self.collect_concat(block)

	def grep(self, pattern, block=default): #no block: simply greps, no post-processing
		grepped = []
		for x in self:
			if re.compile(pattern).match(str(x)):
				grepped.append(block(x))
		return Enumerable(grepped)

	def group_by(self, block=default): #no block: groups by value
		dictionary = {}
		for x in self:
			dictionary.setdefault(block(x), []).append(x)
		for key in dictionary:
			dictionary[key] = tuple(dictionary[key])
		return dictionary

	def include(self, obj):
		for x in self:
			if x == obj:
				return True
		return False

	#does not support operators as plain symbols
	def inject(self, block, initial=sentinel): #no block: error
		if initial == Enumerable.sentinel:
			initial = self[0]
		for x in self:
			initial = block(initial, x)
		return initial

	def map(self, block=default): #no block: see collect
		return self.collect(block)

	def max(self, n=1, block=compare): #no block: compares with x>y -> 1, y>x -> -1
		self = copy.deepcopy(self)
		maxVal = self[0]
		for x in self:
			maxVal = x if block(x,maxVal)>0 else maxVal
		if n > 1:
			self.remove(maxVal)
			vals = [maxVal]
			vals.extend(self.maxList(n-1, block))
			return Enumerable(vals)
		return maxVal

	def maxList(self, n, block):
		maxVal = self[0]
		for x in self:
			maxVal = x if block(x,maxVal)>0 else maxVal
		if n > 1:
			self.remove(maxVal)
			vals = [maxVal]
			vals.extend(self.maxList(n-1, block))
			return vals
		return [maxVal]

	def max_by(self, n=1, block=default): #no block: compares with x>y -> 1, y>x -> -1
		self = copy.deepcopy(self)
		maxVal = self[0]
		for x in self:
			maxVal = x if block(x)>block(maxVal) else maxVal
		if n > 1:
			self.remove(maxVal)
			vals = [maxVal]
			vals.extend(self.maxList_by(n-1, block))
			return Enumerable(vals)
		return maxVal

	def maxList_by(self, n, block):
		maxVal = self[0]
		for x in self:
			maxVal = x if block(x)>block(maxVal) else maxVal
		if n > 1:
			self.remove(maxVal)
			vals = [maxVal]
			vals.extend(self.maxList_by(n-1, block))
			return vals
		return [maxVal]

	def member(self, obj):
		return self.include(obj)

	def min(self, n=1, block=compare): #no block: compares with x>y -> 1, y>x -> -1
		self = copy.deepcopy(self)
		minVal = self[0]
		for x in self:
			minVal = x if block(x,minVal)<0 else minVal
		if n > 1:
			self.remove(minVal)
			vals = [minVal]
			vals.extend(self.minList(n-1, block))
			return Enumerable(vals)
		return minVal

	def minList(self, n, block):
		minVal = self[0]
		for x in self:
			minVal = x if block(x,minVal)<0 else minVal
		if n > 1:
			self.remove(minVal)
			vals = [minVal]
			vals.extend(self.minList(n-1, block))
			return vals
		return [minVal]

	def min_by(self, n=1, block=default): #no block: compares with x>y -> 1, y>x -> -1
		self = copy.deepcopy(self)
		minVal = self[0]
		for x in self:
			minVal = x if block(x)<block(minVal) else minVal
		if n > 1:
			self.remove(minVal)
			vals = [minVal]
			vals.extend(self.minList_by(n-1, block))
			return Enumerable(vals)
		return minVal

	def minList_by(self, n, block):
		minVal = self[0]
		for x in self:
			minVal = x if block(x)<block(minVal) else minVal
		if n > 1:
			self.remove(minVal)
			vals = [minVal]
			vals.extend(self.minList_by(n-1, block))
			return vals
		return [minVal]

	def minmax(self, block=compare): #no block: compares with x>y -> 1, y>x -> -1
		return Enumerable([self.min(block=block), self.max(block=block)])

	def minmax_by(self, block=default): #no block: compares with x>y -> 1, y>x -> -1
		return Enumerable([self.min_by(block=block), self.max_by(block=block)])

	def none(self, block=default): #no block: True if none are True
		return not self.any(block)

	def one(self, block=default): #no block: True if exactly one is True
		return True if self.find_all(block).count() == 1 else False

	def partition(self, block=default): #no block: partition by truth value
		trueAry = []
		falseAry = []
		for x in self:
			if block(x):
				trueAry.append(x)
			else:
				falseAry.append(x)
		return Enumerable([Enumerable(trueAry), Enumerable(falseAry)])

	def reduce(self, block, initial=sentinel): #see inject
		return self.inject(block, initial)

	def reject(self, block=default): #no block: all non True elements
		rejected = []
		for x in self:
			if not block(x):
				rejected.append(x)
		return Enumerable(rejected)

	def reverse_each(self, block=defaultPrint): #no block: prints reversed list
		for x in reversed(self):
			block(x)
		return self

	def select(self, block=default): #no block: see find all
		return self.find_all(block)

	def sort(self, block=compare): #no block: compares with x>y -> 1, y>x -> -1
		return self.min(len(self), block)

	def sort_by(self, block=default): #no block: compares with x>y -> 1, y>x -> -1
		return self.min_by(len(self), block)

	def take(self, n):
		return Enumerable(self[:n])

	def take_while(self, block=default): #no block: takes up to True values
		for x in self:
			if not block(x):
				return self.take(self.find_index(x))
		return self

	def to_a(self):
		return self

	def to_h(self):
		dictionary = {}
		pairs = Enumerable(self[0::2]).zip(self[1::2])
		for key, value in pairs:
			if key in dictionary:
				dictionary[key] = [dictionary[key]]
				dictionary[key].append(value)
			else:
				dictionary[key] = value
		return dictionary

	def zip(self, block, *lists): #no block: no post-proccess, simply zips
		if not callable(block):
			lists = tuple([block])+lists
			if callable(lists[-1]):
				block = lists[-1]
				lists = lists[:-1]
			else:
				block = Enumerable.default
		return [tuple(block([x]+[item[i] if i<len(item) else None for item in lists])) for i, x in enumerate(self)]