# README:
## Johnny Jacobs, CSC 253

Run `UnitTests.py` using Python 3.5 and it will assert the assertion tests, print the print tests to output for your viewing pleasure, and then assert the tree tests. (`python UnitTest.py` in a terminal) (`python3` instead of `python` on csug machines) Be sure to note that when testing, blocks must be passed as parameters (though often optional)

Python3, because it's easy and I know it

Stop iteration? Why, that's impossible! MUWAHAHAHAHA (yea you can just `ctrl-c` that badboy)

Most methods have a default block which does something standard when no block is given instead of an error  
Blocks are almost entirely optional! wooo  
Sentinel used in places where optional args failed me  
Cool things like:  
 `count()` only taking 0-1 args despite taking a block/number/nothing  
 `cycle()` terminating at maximum recursion and printing helpful stuff instead of errors (while returning -1)  
 `find()`/`detect()` can process `ifnone`'s that are functions or simply expressions
 `grep()` can use regex for matching    
 `reduce()`/`inject()` cannot take plain symbols, but requires the corresponding func (operator.add, etc)  
 `zip()` is very neat, it can take infinite lists to zip together, with the block at the beginning, end, or not at all!  

Tree is implemented as a list, and the `insert`, `each`, and `each_with_level` methods change the underlying array and return it (`each` and `each_with_level` assign the result of `block(element)` into `element` for any `block` passed)

Documentation is a bit limited as I have run out of time =(