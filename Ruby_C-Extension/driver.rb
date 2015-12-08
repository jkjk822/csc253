require 'benchmark'
require_relative 'unit_tests'

[10**3, 10**7].each do |size|
	puts ""
	puts "#"*(26+size.to_s.size)
	puts "# Test with table size: #{size} #"
	puts "#"*(26+size.to_s.size)
	hash = Hash.new(size)
	my_hash = MyHash.new(size)
	my_c_hash = MyCHash.new(size)

	tables = [hash,my_hash,my_c_hash]

	seed = Random.new_seed
	gen = Random.new(seed)

	tables.each do |table|
		gen = Random.new(seed)
		size.times do |i|
			key = gen.rand(size*2)
			val = gen.rand(size*2)
			table[key] = val
		end
	end

	raise "Sizes unequivilant" unless hash.size == my_hash.size and hash.size == my_c_hash.size

	puts ""
	puts "#{hash.size} unique values generated"
	puts ""

	raise "Tables unequivilant" unless hash.each {|k, v| v == my_hash[k] and v == my_c_hash[k]}.all?

	seed = Random.new_seed
	Benchmark.bmbm do |x|
		gen = Random.new(seed)
		x.report("Built-In implementation") { (10**6).times{hash[gen.rand(size*2)] } }
		gen = Random.new(seed)
		x.report("Ruby implementation")  { (10**6).times{my_hash[gen.rand(size*2)] } }
		gen = Random.new(seed)
		x.report("C implementation")  { (10**6).times{my_c_hash[gen.rand(size*2)] } }
	end
	puts ""
	puts ""
	puts ""
end


# The evaluation must be reported scientifically.
# You must provide information enough for other to reconstruct the testing environment and
# reproduce your results if they choose to.  The writing must be clear, unambiguous, and easy to read.
# Take a look at a published paper for a precedence to follow.