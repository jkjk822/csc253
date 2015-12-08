require 'benchmark'
require_relative 'unit_tests'

integer = lambda {|x| x}
symbol = lambda {|x| x.to_s.to_sym}

[integer, symbol].each do |transform|
	[10**3, 10**7].each do |size|
		klass = transform.call(2).class
		puts ""
		puts "#"*(27+klass.to_s.size+size.to_s.size)
		puts "# #{klass} Test with table size: #{size} #"
		puts "#"*(27+klass.to_s.size+size.to_s.size)

		hash = Hash.new(size)
		my_hash = MyHash.new(size)
		my_c_hash = MyCHash.new(size)

		tables = [hash,my_hash,my_c_hash]

		seed = Random.new_seed
		gen = Random.new(seed)

		tables.each do |table|
			gen = Random.new(seed)
			size.times do |i|
				key = transform.call(gen.rand(size*2..size*4))
				val = gen.rand(size*2..size*4)
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
			x.report("Built-In implementation") { (10**6).times{hash[transform.call(gen.rand(size*2..size*4))] } }
			gen = Random.new(seed)
			x.report("Ruby implementation")  { (10**6).times{my_hash[transform.call(gen.rand(size*2..size*4))] } }
			gen = Random.new(seed)
			x.report("C implementation")  { (10**6).times{my_c_hash[transform.call(gen.rand(size*2..size*4))] } }
		end
		puts ""
		puts ""
		puts ""
	end
end