# Ruby C-Extension
## Csc 253
### Johnny Jacobs (jjaco16)

#### Files:
- `report.md` this file
- `my_hash.c` c source code for ruby hash table C-extension
- `extconf.rb` ruby file to create makefile for C-extension
- `myhash.rb` ruby hash table implementation
- `unit_tests.rb` unit tests for both ruby and C-extension tables
- `driver.rb` runs unit tests and performance tests

#### Steps to run
- ensure all files are present
- run `ruby extconf.rb`
- run `make`
- run `ruby driver.rb`
You should see output which tells you how the unit and performance tests fared



## Methods

Tests were done by generating random numbers (using `Ruby::Random`) in the range `size*2` to `size*4` where `size` was either 1 thousand (small-scale test case) or 10 million (large-scale test case). The range was offset by a factor of `size*2` in an attempt to spread out the hash keys. This range was chosen as it is large enough to give a suitable number of unique values (>75% unique), while also being small enough to make random access hashes likely to find real values instead of only `nil`.

To illustrate this, imagine generating 1000 random numbers in the range 0 to 1000. In this scenario, one is virtually guaranteed to generate the same number more than once, and in reality, this repetition happens numerous times. However, when generating 1 million random keys (this is how many random hashes were used)  in the range 0 to 1000, one is *very* likely to get a key that corresponds to a real value, instead of just `nil`.  
Now imagine generating 1000 random numbers in the range 0 to 2^62. One will get entirely unique numbers nine times out of ten. However, generating even 1 million random keys does not give a high chance of finding one that corresponds to a real value, so 99% of the hashes will access `nil` values, which is obviously not a good metric nor realistic.

Testing was done on two types of data, `Fixnum` and `Symbol`. `Symbol` was included because `object_id` was used as the hash function, giving an unfair advantage to `Fixnum` data. This advantage stems from the fact that `object_id` simply returns `(2*x)+1` if `x` is a `Fixnum`. This means an even distribution of data and little clustering, making `object_id` an excellent hash function for a range of `Fixnum` objects. Adding `Symbol`, for which `object_id` gives a much more random distribution, allows a fairer comparison of hash rates with Ruby's built-in hashtable. Additionally, since all `Symbol` with a multiple of twenty, it provides a relatively collision-heavy testing environment.

Testing was done using `Ruby::Benchmark` specifically `Benchmark::bmbm`, which supposedly erases inequitable effects of garbage collection and memory allocation.

## Results

*Hashes per second were calculated by dividing 1 million (the number of hashes done) by the total time taken as given by `Ruby::Benchmark`, averaged across three runs.*


#### Fixnum Test with table size: 1000

800 unique values generated on average

| Implementation | Hashes/s      |
|:-------------  |:-------------:|
| Built-In       | 1.3mil 		 |
| Ruby 		     | 780K		     |
| C 			 | 1.2mil 		 |

-----------------------------------------


#### Fixnum Test with table size: 10000000


7.86mil unique values generated on average

| Implementation | Hashes/s      |
|:-------------  |:-------------:|
| Built-In       | 680K 		 |
| Ruby 		     | 660K		     |
| C 			 | 940K 		 |

-----------------------------------------


#### Symbol Test with table size: 1000

780 unique values generated on average

| Implementation | Hashes/s      |
|:-------------  |:-------------:|
| Built-In       | 950K 		 |
| Ruby 		     | 300K		     |
| C 			 | 580K 		 |

-----------------------------------------


#### Symbol Test with table size: 10000000

7.87mil unique values generated on average

| Implementation | Hashes/s      |
|:-------------  |:-------------:|
| Built-In       | 230K 		 |
| Ruby 		     | 110K		     |
| C 			 | 140K 		 |

-----------------------------------------


## Dicussion

As expected, and as the results make clearly evident, a C-extension library is faster than a hashtable implemented in Ruby proper. What's interesting is the comparison between the C-extension hashtable and the Ruby built-in hashtable. Here the `Fixnum` and `Symbol` cases are quite different.

Presumably, the built-in implementation uses a better collision resolution strategy than the infamous and trivial chaining table. This, coupled with a clever, dynamic hashing algorithm that is also presumably part of the Ruby built-in implementation (and the fact that the built-in table is also C at its core), seems like it should be enough to let the built-in table win out over the C-extension table in all conceivable scenarios.

In the collision-heavy scenario (`Symbol`), this was indeed the case. The built-in table consistently outperformed the C-extension table by a factor of about 1.6, in both the small and large-scale test cases.

However in the collision-sparse scenario (`Fixnum`), it was a different story altogether. The two tables were similar in speed on the small-scale test case, with the built-in table outperforming the C-extension table by less than 10%. In the large-scale test case, the built-in table performed atrociously, barely managing to outperform even the Ruby implemented table (and in some runs, even under-performing it). And as for the C-extension table, it was nearly 40% faster than the built-in table.  
Perhaps it was all due to the `object_id` hashing algorithm being well suited to the dataset, which would explain why the Ruby implementation performed so well compared to the built-in implementation, as well as the domination of the C-extension. However this does not explain why the built-in table did not dynamically chose a similarly efficient algorithm to use as a hashing function. A sequential range of numbers is not only a trivial hashing case, it (or a slight permutation thereof) is a quite common one as well. It is possible that the built-in hash implementation assumes an `Array` will be used for the sequential case, and thus does not bother with it, but arrays have trouble with the permuted cases. Whatever the reason, it is worrying to say the least that a built-in class would have such poor performance on such a prominent use-case.