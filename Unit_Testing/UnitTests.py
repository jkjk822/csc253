"""
Each functions contains assert statements which test the appropriate method
Functions are named testFunc where Func corresponds to func, the function
being tested

test is a test list used in many of these assertions

"""
import Enumerable
import Tree
import copy

def testAll(test):
	assert test.all(lambda x: x < 7) == True
	assert test.all(lambda x: x > 3) == False
	assert test.all() == True
	assert Enumerable.Enumerable([1,2,None]).all() == False
	assert Enumerable.Enumerable([True,True,False]).all() == False

def testAny(test):
	assert test.any(lambda x: x > 7) == False
	assert test.any(lambda x: x > 3) == True
	assert Enumerable.Enumerable([True, False, 3]).any() == True
	assert Enumerable.Enumerable([False,False]).any() == False
	assert Enumerable.Enumerable([None, None]).any() == False

def testCollect(test):
	assert test.collect(lambda x: x%2) == [1,0,0]
	assert test.collect(lambda x: x > 3) == [False, False, True]
	assert Enumerable.Enumerable(["True", "False", "3"]).collect(lambda x: x+"test") == ["Truetest", "Falsetest", "3test"]
	assert test.collect(lambda x: "dogfish") == ["dogfish","dogfish","dogfish"]

def testCollect_concat(test):
	assert test.collect_concat(lambda x: [x%1,x%2]) == [0,1,0,0,0,0]
	assert test.collect_concat(lambda x: [x>3]) == [False, False, True]
	assert Enumerable.Enumerable([[True], [False], [3]]).collect_concat(lambda x: x+["test"]) == [True, "test", False, "test", 3, "test"]
	assert test.collect_concat(lambda x: ["dogfish"]) == ["dogfish","dogfish","dogfish"]

def testCount(test):
	assert test.count() == 3
	assert test.count(test.count()) == 0
	assert test.count(lambda x: x > 7) == 0
	assert test.count(lambda x: x < 3) == 2
	assert Enumerable.Enumerable([True, False, 3]).count(lambda x: x) == 2

def testCycle(test):
	print("\ntestCycle")
	test.cycle(block=lambda x: print(x+1))
	print("Should be the same as:")
	print("2,3,5,2,3,5,2,...etc\n")

	test.cycle(2,lambda x: print(x+1))
	print("Should be the same as:")
	print("2,3,5,2,3,5\n")

	assert Enumerable.Enumerable([]).cycle() == None 
	assert test.cycle(-1, lambda x: print(x+1)) == None

	Enumerable.Enumerable([None, None]).cycle(None, lambda x: print(x))
	print("Should be the same as:")
	print(None,None,None,None,"...etc\n")


def testDetect(test):
	assert test.detect(lambda x: x > 3) == 4
	assert test.detect(lambda x: x > 7) == None
	assert test.detect(lambda x: x > 7,sum(test)) == 7
	assert test.detect(lambda x: x > 7,lambda: sum(test)) == 7

def testDrop(test):
	assert test.drop(1) == [2,4]

def testDrop_while(test):
	assert test.drop_while(lambda x: x < 3) == [4]
	assert test.drop_while(lambda x: x < 7) == []
	assert test.drop_while(lambda x: x > 7) == [1,2,4]
	assert Enumerable.Enumerable([True, 1, None]).drop_while(lambda x: x) == [None]
	assert Enumerable.Enumerable([True, 2, False]).drop_while(lambda x: x) == [False]

def testEach_cons(test):
	print("\ntestEach_cons")
	test.each_cons(2,lambda x: print(x))
	print("Should be the same as:")
	print([1,2],[2,4])

def testEach_entry(test):
	print("\ntestEach_entry")
	test.each_entry(lambda x: print(2*x))
	print("Should be the same as:")
	print(2,4,8)

def testEach_slice(test):
	print("\ntestEach_slice")
	Enumerable.Enumerable([3,4,5,2,3,5,6,2]).each_slice(3,lambda x: print(x))
	print("Should be the same as:")
	print([3,4,5],[2,3,5],[6,2])

def testEach_with_index(test):
	print("\ntestEach_with_index")
	test.each_with_index(lambda x,i: print(x*i))
	print("Should be the same as:")
	print(0,2,8)

def testEach_with_object(test):
	assert test.each_with_object([1,2,4], lambda x,obj: obj.append(x*8)) == [1,2,4,8,16,32]
	assert test.each_with_object([1,2,4], lambda x,obj: x*3) == [1,2,4]

def testEntries(test):
	assert Enumerable.Enumerable((1,4,5)).entries() == [1,4,5]
	assert Enumerable.Enumerable(((3,1),(2,1),(4,3))).entries() == [(3,1), (2,1), (4,3)]

def testFind(test): #exactly the same as detect()
	assert test.detect(lambda x: x > 3) == 4
	assert test.detect(lambda x: x > 7) == None
	assert test.detect(lambda x: x > 7,sum(test)) == 7
	assert test.detect(lambda x: x > 7,lambda: sum(test)) == 7

def testFind_all(test):
	assert test.find_all(lambda x: x > 3) == [4]
	assert test.find_all(lambda x: x > 7) == []
	assert test.find_all(lambda x: x < 3) == [1,2]
	assert Enumerable.Enumerable([False, 1, None]).find_all(lambda x: x) == [1]

def testFind_index(test):
	assert test.find_index(2) == 1
	assert test.find_index(3) == None
	assert test.find_index(lambda x: x > 3) == 2
	assert test.find_index(lambda x: x > 7) == None
	assert test.find_index(lambda x: x < 7) == 0
	assert Enumerable.Enumerable([False, False, None]).find_index(lambda x: x) == 2
	assert Enumerable.Enumerable([False, 1, None]).find_index(lambda x: x) == 1

def testFirst(test):
	assert test.first() == 1
	assert test.first(2) == [1,2]
	assert Enumerable.Enumerable([]).first() == None

def testFlat_map(test): #exactly the same as collect_concat()
	assert test.flat_map(lambda x: [x%1,x%2]) == [0,1,0,0,0,0]
	assert test.flat_map(lambda x: [x>3]) == [False, False, True]
	assert Enumerable.Enumerable([[True], [False], [3]]).flat_map(lambda x: x+["test"]) == [True, "test", False, "test", 3, "test"]
	assert test.flat_map(lambda x: ["dogfish"]) == ["dogfish","dogfish","dogfish"]

def testGrep(test):
	assert Enumerable.Enumerable([1,"one", 2, "two", 3, "three"]).grep("one") == ["one"]
	assert Enumerable.Enumerable([1,"one", 2, "two", 3, "three"]).grep("one",lambda x: x+" more") == ["one more"]
	assert Enumerable.Enumerable([1,"one", 2, "two", 3, "three"]).grep(r'\d',lambda x: x*x) == [1,4,9]

def testGroup_by(test):
	assert Enumerable.Enumerable([1,"one", 2, "two", 3, "three"]).group_by(lambda x: "str" if type(x) is str else "not str") == {"str":("one","two","three"),"not str": (1,2,3)}

def testInclude(test):
	assert test.include(2) == True
	assert test.include(3) == False

def testInject(test):
	assert test.inject(lambda div, x: div/x) == .125
	assert test.inject(lambda div, x: div/x,128) == 16
	assert test.inject(lambda max, x: x if x>max else max) == 4
	assert Enumerable.Enumerable(["I","am","a","sentence"]).inject(lambda sentence, x: sentence+" "+x, "The sentence:") == "The sentence: I am a sentence"

def testMap(test): #exactly the same as collect()
	assert test.map(lambda x: x%2) == [1,0,0]
	assert test.map(lambda x: x > 3) == [False, False, True]
	assert Enumerable.Enumerable(["True", "False", "3"]).map(lambda x: x+"test") == ["Truetest", "Falsetest", "3test"]
	assert test.map(lambda x: "dogfish") == ["dogfish","dogfish","dogfish"]

def testMax(test):
	assert test.max() == 4
	assert test.max(2) == [4,2]
	assert test.max(block=lambda x,y: 1 if x>y else -1) == 4
	assert test.max(3, lambda x,y: 1 if x>y else -1) == [4,2,1]

def testMax_by(test):
	assert test.max_by(block=lambda x: x%3) == 2
	assert test.max_by(3, lambda x: x%3) == [2,1,4]

def testMember(test): #exactly the same as include()
	assert test.member(2) == True
	assert test.member(3) == False

def testMin(test):
	assert test.min() == 1
	assert test.min(2) == [1,2] 
	assert Enumerable.Enumerable(["A","a","c","E"]).min(block=lambda x,y: 1 if ord(x)>ord(y) else -1) == "A"
	assert Enumerable.Enumerable(["A","a","c","E"]).min(2, lambda x,y: 1 if ord(x)>ord(y) else -1) == ["A","E"]

def testMin_by(test):
	assert test.min_by(block=lambda x: x%3) == 1
	assert test.min_by(2, lambda x: x%3) == [1,4]

def testMinmax(test):
	assert test.minmax() == [1,4]
	assert Enumerable.Enumerable(["A","a","c","E"]).minmax(lambda x,y: 1 if ord(x)>ord(y) else -1) == ["A","c"]

def testMinmax_by(test):
	assert Enumerable.Enumerable([1,6,4,5,14]).minmax_by(lambda x: x%3) == [6,5]

def testNone(test):
	assert test.none(lambda x: x > 7) == True
	assert test.none(lambda x: x == 2) == False
	assert Enumerable.Enumerable([]).none() == True
	assert Enumerable.Enumerable([None, False]).none() == True
	assert Enumerable.Enumerable([None, 1, False]).none() == False

def testOne(test):
	assert test.one(lambda x: x > 7) == False
	assert test.one(lambda x: x == 2) == True
	assert Enumerable.Enumerable([None, False]).one() == False
	assert Enumerable.Enumerable([None, 1, False]).one() == True

def testPartition(test):
	assert test.partition(lambda x: x > 3) == [[4],[1,2]]

def testReduce(test): #exactly the same as inject()
	assert test.inject(lambda div, x: div/x) == .125
	assert test.inject(lambda div, x: div/x,128) == 16
	assert test.reduce(lambda max, x: x if x>max else max) == 4
	assert Enumerable.Enumerable(["I","am","a","sentence"]).reduce(lambda sentence, x: sentence+" "+x,"The sentence:") == "The sentence: I am a sentence"

def testReject(test): #inverse of find_all()
	assert test.reject(lambda x: x > 3) == [1,2]
	assert test.reject(lambda x: x > 7) == [1,2,4]
	assert test.reject(lambda x: x < 3) == [4]
	assert Enumerable.Enumerable([False, 1, None]).reject(lambda x: x) == [False, None]

def testReverse_each(test): #inverse of each_entry()
	print("\ntestReverse_each")
	assert test.reverse_each(lambda x: print(x*2))
	print("Should be the same as:")
	print(8,4,2)

def testSelect(test): #exactly the same as find_all()
	assert test.select(lambda x: x > 3) == [4]
	assert test.select(lambda x: x > 7) == []
	assert test.select(lambda x: x < 3) == [1,2]
	assert Enumerable.Enumerable([False, 1, None]).select(lambda x: x) == [1]

def testSort(test):
	assert test.sort() == [1,2,4]
	assert Enumerable.Enumerable(["A","a","c","E"]).sort(lambda x,y: 1 if ord(x)>ord(y) else -1) == ["A","E","a","c"]

def testSort_by(test):
	assert Enumerable.Enumerable([1,6,4,5,14]).sort_by(lambda x: x%3) == [6,1,4,5,14]

def testTake(test):
	assert Enumerable.Enumerable([1,6,4,5,14]).take(3) == [1,6,4]

def testTake_while(test): #inverse of drop_while()
	assert test.take_while(lambda x: x < 3) == [1,2]
	assert test.take_while(lambda x: x < 7) == [1,2,4]
	assert test.take_while(lambda x: x > 7) == []
	assert Enumerable.Enumerable([True, 1, None]).take_while(lambda x: x) == [True, 1]
	assert Enumerable.Enumerable([True, 2, False]).take_while(lambda x: x) == [True, 2]

def testTo_a(test):
	assert Enumerable.Enumerable((1,4,5)).to_a() == [1,4,5]
	assert Enumerable.Enumerable(((3,1),(2,1),(4,3))).to_a() == [(3,1), (2,1), (4,3)]

def testTo_h(test):
	assert Enumerable.Enumerable([3,1,2,1,4,3]).to_h() == {2:1, 3:1, 4:3}
	assert Enumerable.Enumerable((1,4)).to_h() == {1:4}

def testZip(test):
	assert test.zip(list(reversed(test)),[0,1,2],[1,2,3]) == [(1,4,0,1),(2,2,1,2),(4,1,2,3)]
	#assert test.zip(list(reversed(test)),lambda x: print(x)) == print((1,4),(2,2),(4,1)) #can't actually assert, needs manual test

def testInsert(tree): #beware, these unit tests change "tree"
	assert tree.insert(4) == [1,2,4,5,3,8,2,6]+[4]
	assert tree.insert("test") == [1,2,4,5,3,8,2,6]+[4]+["test"]
	assert tree.insert(None) == [1,2,4,5,3,8,2,6]+[4]+["test"]+[None]

def testEach(tree): #beware, these unit tests change "tree"
	assert tree.each(lambda x: x**2) == [1,4,16,25,9,64,4,36]

def testEach_with_level(tree): #beware, these unit tests change "tree"
	assert tree.each_with_level(lambda x, d: x+d) == [1,3,5,7,5,10,4,9]



test = Enumerable.Enumerable([1,2,4])

#assertion tests

testAll(test)
testAny(test)
testCollect(test)
testCollect_concat(test)
testCount(test)
testDetect(test)
testDrop(test)
testDrop_while(test)
testEach_with_object(test)
testEntries(test)
testFind(test)
testFind_all(test)
testFind_index(test)
testFirst(test)
testFlat_map(test)
testGrep(test)
testGroup_by(test)
testInclude(test)
testInject(test)
testMap(test)
testMax(test)
testMax_by(test)
testMember(test)
testMin(test)
testMin_by(test)
testMinmax(test)
testMinmax_by(test)
testNone(test)
testOne(test)
testPartition(test)
testReduce(test)
testReject(test)
testSelect(test)
testSort(test)
testSort_by(test)
testTake(test)
testTake_while(test)
testTo_a(test)
testTo_h(test)
testZip(test)

print("************************************\nAssertion Tests Exited Without Error\n************************************\n")


#output tests (some assertion in cycle)
#look at the output of these to verify it is the same (whitespace disregarded)

#testCycle(test) #this one prints infinite (nearly) text, so it's cases should be commented out and tested individually
testEach_cons(test)
testEach_entry(test)
testEach_slice(test)
testEach_with_index(test)
testReverse_each(test)


#tree tests
tree = Tree.Tree([1,2,4,5,3,8,2,6])
testEach(copy.deepcopy(tree))
testEach_with_level(copy.deepcopy(tree))
testInsert(copy.deepcopy(tree))

print("\n\n*******************************\nTree Tests Exited Without Error\n*******************************\n")

