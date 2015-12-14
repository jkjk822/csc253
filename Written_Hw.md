# Written Homework
## Csc 253
### Johnny Jacobs

#### ==== (Essence of OO, 25 points)

**In the class, we defined Object and Class using a diagram.  In this
exercise, define Object and Class in text, i.e.  explaining in
narrative the circular definition that Object is an instance of Class,
and a class is an object.  Based on the definitions of Object and
Class, define an object and a class.
To receive full credits, the definitions must be precise and complete.
For precision, make sure that every concept used in your text is
defined before used.  Extra credits may be given for ease of
understanding and concision, at the discretion of the grader.**


An object is a collection of information, or data. If neither of these are precise enough, consider data equivilant to function (as defined below).

A class is an object whose data consists of functions, functions being defined as they were in class: a relation from a set of inputs to a set of possible outputs (size of both sets range from empty-unbounded)

At this point classes/objects are not really differentiated, but simply different interpretations of the same thing. Below we use their different names to define their unique properties.

All objects are an instance of some class, this just means that for every object, there exists some other object, which is a class, which stores the functions the base object can use to manipulate its data.

Since all classes are objects, all classes are instances of a class as well.
The special case is the Class object, which is its own class, and thus stores its own functions.

All classes inherit from/are children of some object, meaning for every class, there exists some other object, whose data is also considered the data of the class (for all purposes, including further inheritence). This does not break the definition of class as data can interpreted as a simplistic function.

Classes either inherit from other classes, or a base object, Object.

As Object is not a class, it does not have a parent. Object is, however, an instance of Class. Class, as a class, must have a parent, which in this case is Object.


#### ==== (Object behavior, 15 points)
**Use your current version of Ruby and its interpreter when answering
the following questions.  It is recommended (not required) that you go
through the exercises on slide 56, lecture 15.  
To ease the narrative, we define the following terms for a class,
e.g. File.  The *instance behavior* of a class is the set of its
instance methods, e.g. File.instance_methods.  The *class behavior* of
a class is the set of its object methods, e.g. File.methods.  Answer
the following questions:**  
**1) Show how to find the minimal object behavior, that is, the set of
methods that every object has in Ruby.**  
`Object.instance_methods`  
**2) Show how to find precise difference in behavior between a module
and a class.**  
`Class.instance_methods - Module.instance_methods` (technically one might want to add `+ (Module.instance_methods - Class.instance_methods)` but this is unecessary as it is known that as the parent, Module has no extra methods)  
**3) Since a class is an instance of the Class class, is it always the case
that the class behavior of a class, e.g. Object, is identical to the
instance behavior of the Class class?  If not, explain why they may
differ and give an example class that has a different behavior.**  
Yes, their behavior will always be the same, as class methods are `klass.class.instance_methods` which, for a class, should always give the same as `Class.instance_methods`



#### ==== (Type class, 15 points)
**Define the following Haskell types/classes.  You should try to 
define them yourself before looking up Hasekell documentation.  
1) Define the boolean type Bool**  
`data Bool = False | True`  
**2) Given the type Ordering defined as follows
data Ordering           =  EQ | LT | GT 
The type class 'Ord x' has the following methods: compare, <, <=, >, >=, max, min.  Give their types.**

	class Ord x where 
		compare:: a -> a -> Int
		<:: a -> a -> Bool
		<=:: a -> a -> Bool
		>:: a -> a -> Bool
		>=:: a -> a -> Bool
		max:: a -> a -> a
		min:: a -> a -> a

**3) The actual definition in Haskell is below, which stipulates a
dependence/inheritance in Ord x  from Eq x
class Eq x => Ord x where ...
Evaluate this design especially whether the dependence is necessary.**

Inheritence is never strictly necessary, you can always just reimplement the parent method functionality.
However, in this case it is also not necessary because you can implement all methods simply using `<` and `>`. For `compare`, `min`, and `max`, simply test both and if neither are true, you know you are in the equal case. For `<=` and `>=` just use the inverse of `>` and `<`.

#### ==== (Polymorphism, 5 points)
**If function type B is a subtype of function type A, any B function can
be substituted any place where function type A is specified.  A and B
must have the same number of parameters, each parameter covariant, and
the return value contravariant.  Is 'Cat -> Cat' a subtype of 'Animal
-> Animal'?  Explain your answer.**  

No, each parameter is covariant (a child) but the return type is not contravariant (a parent), but rather covariant. Thus 'Cat -> Cat' is not a subtype of 'Animal -> Animal'. A correct subtype would be 'Cat -> Organism'


#### ==== (Unified process, 0 point)
**Answer the following from your memory.  Give the five workflows
and 4 stages of the unified software development process.**





























Requirements, Analysis, Design, Implementation, Testing
Inception, Elaboration, Construction, Transition

