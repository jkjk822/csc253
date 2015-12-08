require_relative "mychash.so"
require_relative "myhash.rb"

x = MyCHash.new
x[1] = 4
puts x.size
x[56] = 435
x[42] = 3
x[132] = 23
puts x.size
x[2] = 4
puts x.size
x[56] = 35
puts x.size
x[41] = 3
x[131] = 23
puts x.size
x[3] = 4
x[96] = 439
puts x.size
x[43] = 3
puts x.size
x[232] = 23
puts x.size
x[2] = 5
puts x.size
x[93] = 435
x[412] = 3
puts x.size
x[232] = 23
x["hello"] = 32
puts x.size
x.each {|k,v| puts "[#{k},#{v}]"}