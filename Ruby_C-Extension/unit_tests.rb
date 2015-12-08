require 'test/unit'
require  'test/unit/ui/console/testrunner'
require_relative 'mychash.so'
require_relative 'myhash.rb'

module Tests

	@@klass = nil

	def self.klass
		return @@klass
	end

	def self.klass=(arg)
		@@klass = arg
	end

	###########
	# Setup   #
	###########
	def setup

		@table = @@klass.new
		assert_equal(0, @table.size, "#{@@klass}: size not properly initialized")
		#all stores
		@table[1] = 4
		@table[56] = :hi
		@table[42] = 3
		#strings can be used as keys, though since hash is based on object_id, this can lead to unexpected behavior
		@table["dsf"] = 23
		@table[2] = 4
		@table[56] = 35 #update
		@table[41] = {"blue" => :you}
		@table[131] = "dssd"
		@table[3] = 4
		@table[["oh", "no"]] = 120
		@table[96] = 439
		@table[:taco] = "3"
		@table[232] = ["red", "blue"]
		@table[2] = 5 #update
		@table[93] = 435
		@table[{"red" => :me}] = 3
		@table[232] = 23 #update
		@table[8] = 1223
		#15 insertions
		assert_equal(15, @table.size, "#{@@klass}: size not properly updated")
	end



	#########################################################
	# Tests													#
	#########################################################
	
	def test_fetch
		x = @@klass.new
		assert_nil(x.fetch(3), "#{@@klass}: fetch of uninitialized item was non-nil")
		assert_nil(x.fetch("dsf"), "#{@@klass}: fetch of uninitialized item was non-nil")
		assert_nil(x.fetch(["oh", "no"]), "#{@@klass}: fetch of uninitialized item was non-nil")
		assert_nil(x.fetch({"red" => :me}), "#{@@klass}: fetch of uninitialized item was non-nil")
		assert_nil(x.fetch(:taco), "#{@@klass}: fetch of uninitialized item was non-nil")

		assert_equal(4, @table.fetch(3), "#{@@klass}: fetch of initialized item returned unexpected value")
		assert_equal(23, @table.fetch("dsf"), "#{@@klass}: fetch of initialized item returned unexpected value")
		assert_equal(120, @table.fetch(["oh","no"]), "#{@@klass}: fetch of initialized item returned unexpected value")
		assert_equal(3, @table.fetch({"red" => :me}), "#{@@klass}: fetch of initialized item returned unexpected value")
		assert_equal("3", @table.fetch(:taco), "#{@@klass}: fetch of initialized item returned unexpected value")
	end

	def test_store
		x = @@klass.new
		#initial store should update size
		x.store(:taco, 10)
		assert_equal(10, x[:taco], "#{@@klass}: unexpected value fetched")
		assert_equal(1, x.size, "#{@@klass}: size not incremented")

		#update store should update val but not size
		x.store(:taco, "rand")
		assert_equal("rand", x[:taco], "#{@@klass}: unexpected value fetched")
		assert_equal(1, x.size, "#{@@klass}: size erroneously incremented")

		#checks that linked list buckets work
		assert_equal(2.object_id%10, 7.object_id%10, "object_id's not equal")
		x.store(2, ["list A"])
		x.store(7, ["list B"])
		assert_equal(["list A"], x[2], "#{@@klass}: unexpected value fetched")
		assert_equal(["list B"], x[7], "#{@@klass}: unexpected value fetched")
	end

	def test_bracket
		x = @@klass.new
		assert_nil(x[3], "#{@@klass}: fetch (bracket) of uninitialized item was non-nil")
		assert_nil(x["dsf"], "#{@@klass}: fetch (bracket) of uninitialized item was non-nil")
		assert_nil(x[["oh", "no"]], "#{@@klass}: fetch (bracket) of uninitialized item was non-nil")
		assert_nil(x[{"red" => :me}], "#{@@klass}: fetch (bracket) of uninitialized item was non-nil")
		assert_nil(x[:taco], "#{@@klass}: fetch (bracket) of uninitialized item was non-nil")

		assert_equal(4, @table[3], "#{@@klass}: fetch (bracket) of initialized item returned unexpected value")
		assert_equal(23, @table["dsf"], "#{@@klass}: fetch (bracket) of initialized item returned unexpected value")
		assert_equal(120, @table[["oh","no"]], "#{@@klass}: fetch (bracket) of initialized item returned unexpected value")
		assert_equal(3, @table[{"red" => :me}], "#{@@klass}: fetch (bracket) of initialized item returned unexpected value")
		assert_equal("3", @table[:taco], "#{@@klass}: fetch (bracket) of initialized item returned unexpected value")
	end

	def test_bracket_eq
		x = @@klass.new
		#initial store should update size
		x[:taco] = 10
		assert_equal(10, x[:taco], "#{@@klass}: unexpected value fetched")
		assert_equal(1, x.size, "#{@@klass}: size not incremented")

		#update store should update val but not size
		x[:taco] = "rand"
		assert_equal("rand", x[:taco], "#{@@klass}: unexpected value fetched")
		assert_equal(1, x.size, "#{@@klass}: size erroneously incremented")

		#checks that linked list buckets work
		assert_equal(2.object_id%10, 7.object_id%10, "object_id's not equal")
		x[2] = ["list A"]
		x[7] = ["list B"]
		assert_equal(["list A"], x[2], "#{@@klass}: unexpected value fetched")
		assert_equal(["list B"], x[7], "#{@@klass}: unexpected value fetched")
	end

	def test_delete
		x = @@klass.new
		#initial store should update size
		x.store(:taco, 10)
		assert_equal(10, x[:taco], "#{@@klass}: unexpected value fetched")
		assert_equal(1, x.size, "#{@@klass}: size not incremented")

		#update store should update val but not size
		x.delete(:taco)
		assert_nil(x[:taco], "#{@@klass}: deleted value not nil")
		assert_equal(0, x.size, "#{@@klass}: size not decremented")

		#checks that deleting linked list elements works correctly
		assert_equal(5, 7.object_id%10, "object_id's not equal")
		assert_equal(5, 2.object_id%10, "object_id's not equal")
		assert_equal(5, 132.object_id%10, "object_id's not equal")
		x.store(2, ["list A"]) #head
		x.store(7, ["list B"]) #middle
		x.store(132, ["list C"]) #tail
		assert_equal(["list A"], x[2], "#{@@klass}: unexpected value fetched")
		assert_equal(["list B"], x[7], "#{@@klass}: unexpected value fetched")
		assert_equal(["list C"], x[132], "#{@@klass}: unexpected value fetched")
		x.delete(7) #delete middle
		assert_equal(["list A"], x[2], "#{@@klass}: unexpected value fetched")
		assert_nil(x[7], "#{@@klass}: deleted value not nil")
		assert_equal(["list C"], x[132], "#{@@klass}: unexpected value fetched")
		x.delete(2) #delete head
		assert_nil(x[2], "#{@@klass}: deleted value not nil")
		assert_nil(x[7], "#{@@klass}: deleted value not nil")
		assert_equal(["list C"], x[132], "#{@@klass}: unexpected value fetched")
	end

	def test_each
		assert_false(@table.all? {|k, v| k.class==Fixnum}, "#{@@klass}: all keys were erroneously of type Fixnum")
		assert(@table.any? {|k, v| k.class==Array}, "#{@@klass}: no key of class Array found")
		assert_equal(9, @table.count {|k, v| k.class == Fixnum and v.class == Fixnum}, "#{@@klass}: unexpected number of Fixnum => Fixnum pairs")
		assert_equal([41, {"blue"=>:you}], @table.find {|k, v| k.object_id < 100 and v.object_id > 1000}, "#{@@klass}: unexpected value found")
	end

	def test_dynamic_resize
		x = @@klass.new(2) #initial size 2
		assert_equal(0, x.size, "#{@@klass}: size error")
		x[2] = "ad"
		assert_equal(1, x.size, "#{@@klass}: size error")
		x[7] = "sd"
		assert_equal(2, x.size, "#{@@klass}: size error")
		#full
		x[:hey] = :nah #resize happens here
		assert_equal(3, x.size, "#{@@klass}: resize error")
	end
end



class Test1 < Test::Unit::TestCase
	include Tests

	class << self
		def startup
			@@klass = MyHash
			puts ""
			puts "Test1"
			puts "#"*(10+@@klass.to_s.size)
			puts "# Using #{@@klass} #"
			puts "#"*(10+@@klass.to_s.size)
		end
	end
end

class Test2 < Test::Unit::TestCase
	include Tests

	class << self
		def startup
			@@klass = MyCHash
			puts ""
			puts "Test2"
			puts "#"*(10+@@klass.to_s.size)
			puts "# Using #{@@klass} #"
			puts "#"*(10+@@klass.to_s.size)
		end
	end
end

Test::Unit::UI::Console::TestRunner.run(Test1)
Test::Unit::UI::Console::TestRunner.run(Test2)