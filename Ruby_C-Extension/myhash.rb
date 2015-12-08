class MyHash

	attr_reader :size

	include Enumerable

	class HashNode
		attr_accessor :key
		attr_accessor :val
		attr_accessor :nextNode

		def initialize(key, val)
			@key = key
			@val = val
			@nextNode = nil
		end
	end

	def initialize(capacity=10)
		@capacity = capacity
		@size = 0
		@data = []
	end

	def fetch(key)
		node = @data[key.object_id % @capacity]
		while (node and node.key != key)
			node = node.nextNode
		end
		return if node == nil
		return node.val
	end

	def [](key)
		return fetch(key)
	end

	def store(key, val)
		if @size > @capacity
			@size = 0
			@capacity = @capacity*2
			temp = []
			each{|k,v| temp.push([k,v])}
			@data = []
			temp.each{|k,v| store(k, v)}
		end
		node = @data[key.object_id % @capacity]
		if node == nil
			@size += 1
			@data[key.object_id % @capacity] = HashNode.new(key, val) 
			return self
		end
		if node.key == key
			node.val = val 
			return self
		end
		while(node.nextNode != nil)
			if node.nextNode.key == key
				node.nextNode.val = val 
				return self
			end
			node = node.nextNode
		end
		@size += 1
		node.nextNode = HashNode.new(key, val)
		return self
	end

	def []=(key, val)
		return store(key, val)
	end

	def delete(key)
		node = @data[key.object_id % @capacity]
		return if node == nil
		if node.key == key
			@size -= 1
			@data[key.object_id % @capacity] = node.nextNode
			return node.val
		end
		while(node.nextNode.key != key)
			return if node.nextNode == nil
			node = node.nextNode
		end
		temp = node.nextNode.val
		node.nextNode = node.nextNode.nextNode
		@size -= 1
		return temp
	end

	def each
		@data.each do |node|
			while node != nil
				yield node.key, node.val
				node = node.nextNode
			end
		end
		return
	end
end