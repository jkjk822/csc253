# Metaprogramming

# In all problems, do not use class methods (i.e. self.foo) and class attributes (@@bar).
# Submit your homework as a single .rb file.  Use comments to explain your approach
# for each problem.


###############################
# P1. Class Object Extension. #
###############################
# Define a child class of Array called CntArray.
# Each object created is counted and the call CntArray.cnt
# will give the number of objects that have been created.

class CntArray < Array
	@cnt = 0
	class << self
		attr_accessor :cnt
	end
	def initialize
		self.class.cnt += 1
		super
	end
end

raise "Error" unless CntArray.cnt==0
a = CntArray.new
raise "Error" unless CntArray.cnt==1

#########################
# P2. Meta-programming. #
#########################
# The getter/setter methods in Ruby can be generated automatically.
# The following class
# class A
#   attr_reader :a
# end
# is equivalent to
# class A
#   def a
#     @a
#   end
# end
# Implement cs200_attr_reader to have the same effect as attr_reader.
# Add this method to Class, so it can be used by all classes (Class objects).
# Answer the question whether the method may be called by Class

class Class 
	def cs200_attr_reader(name)
		class_eval("def #{name}() @#{name} end")
	end
end

class Class
	cs200_attr_reader :a

	def initialize
		@a = 110
	end
end

class Test
	cs200_attr_reader :a

	def initialize
		@a = 100
	end
end
test = Test.new
raise "Error" unless test.a==100
x = Class.new
raise "Error" unless x.a==110

# Yes, it can be called by class.
# Class is an instance of Class, and since the method is defined for all instances
# Class itself can call it. Exemplified above

################################
# P3.  Meta-class Inheritance. #
################################
# If Child is a child class of Parent, what is the relation
# between Child's meta-class and Parent's meta-class? 
# Support your answer with code examples.

class Parent
end
class Child < Parent
end

# The metaclass of Child is the child of the metaclass of Parent
metaChild = class << Child; self; end
metaParent = class << Parent; self; end
raise "Error" unless metaChild.superclass == metaParent

#####################
# P4.  Forwardable. #
#####################
# A useful design pattern is delegation,
# which related to the proxy and decorator patterns.
# Ruby provides a module called Forwardable to make delegation easy to specify.
# Read a solution for Forwardable on
# github at https://github.com/ruby/ruby/blob/c84bb5df6dff60d17ff692306aa94fd53bed9638/lib/forwardable.rb 
# In its comments, there are nice examples showing the power of this pattern,
# e.g. creating a Queue class from Array by selecting/renaming array methods. 
# Read the solution, understand it, and (hint) be able to implement it yourself
# (in a close-note and close-book scenario, e.g. mid-term exam).
# Explain how to use Forwardable, and how it could be implemented.

# It is used by simply extending it and then creating delegate object with
# `def_delegator :@obj, :firstmethod, :secondmethod` where first and second method
# are the methods you wish to forward to @obj.
# It is implemented by using eval (module, class, or instance) to create a method which
# sends the request to the delegate object instead of the class

##################################
# P5. Advanced Meta-programming. #
##################################
# Define a module Cnt, so that a class can start counting the number of object creations
# by simply including the module.

module Cnt
	class << self
		def extended(clazz)
			super
			clazz.instance_eval{@cnt = 0}
			clazz.instance_eval("class << self;attr_accessor :cnt;def new(*args);#{clazz}.cnt += 1;super;end;end")
			clazz.instance_eval("class << self;def [](*args);#{clazz}.cnt += 1;end;end")
		end
	end
end
class Array
	extend Cnt
end
raise "Error" unless Array.cnt == 0
# a = [1, 2, 3] #can't support
raise "Error" unless Array.cnt == 0
x = Array.new(4,3)
raise "Error" unless Array.cnt == 1
#really only array specific
Array.[](1,2,3)
raise "Error" unless Array.cnt == 2

######################
# P6. (Extra credit) #
######################
# Solve P5 where the module is mixed in using include instead of extend.

module Cnt2
	class << self
		def included(clazz)
			super
			clazz.instance_eval{@cnt = 0}
			clazz.instance_eval("class << self;attr_accessor :cnt;def new(*args);#{clazz}.cnt += 1;super;end;end")
			clazz.instance_eval("class << self;def [](*args);#{clazz}.cnt += 1;end;end")
		end
	end
end
class String
	include Cnt2
end
raise "Error" unless String.cnt == 0
String.new
raise "Error" unless String.cnt == 1
