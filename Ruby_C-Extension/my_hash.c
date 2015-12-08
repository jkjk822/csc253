#include <ruby.h>
#include <stddef.h>

struct chashdata {
	long capacity;
	struct node ** hash;
};

struct node{
	VALUE key;
	VALUE val;
	struct node * next;
};

static VALUE alloc(VALUE);
static void dealloc(void *);
static size_t memsize_chash(const void *);

static const rb_data_type_t chashdata_type = {
		"chashdata",
		{
			0,
			dealloc,
			memsize_chash,
		},
		0,
		0,
		RUBY_TYPED_FREE_IMMEDIATELY,
};

static VALUE c_hash;

static VALUE
init(int argc, VALUE* argv, VALUE hash){
	struct chashdata *data = ALLOC(struct chashdata);
	long capacity = 10;

	if (argc > 1)  // there should only be 0 or 1 arguments
		rb_raise(rb_eArgError, "wrong number of arguments");
	else if(argc == 1){
		Check_Type(argv[0], T_FIXNUM);
		capacity = FIX2LONG(argv[0]);
	}

	DATA_PTR(hash) = data;
	data->capacity = capacity;
	data->hash = ZALLOC_N(struct node *, capacity);
	rb_iv_set(hash, "size", INT2FIX(0));

	return hash;
}

static VALUE
get_size(VALUE hash){
	return rb_iv_get(hash, "size");
}

static void
update_size(VALUE hash, int update){
	long size = FIX2LONG(get_size(hash));
	size += update;
	rb_iv_set(hash, "size", LONG2FIX(size));
}

static VALUE
fetch(VALUE hash, VALUE key){
	struct chashdata * data;
	struct node * node;

	//Retrieve hashtable
	TypedData_Get_Struct(hash, struct chashdata, &chashdata_type, data);

	long hashkey = FIX2LONG(rb_funcall(key,  rb_intern("object_id"), 0));
	node = data->hash[hashkey % data->capacity];

	//while(node and node.key != key)
	while(node && !RTEST(rb_equal(node->key, key)))
		node = node->next;

	if(node == NULL)
		return Qnil;

	return node->val;
}

static VALUE
store(VALUE hash, VALUE key, VALUE val){
	struct chashdata * data;
	struct node * node;

	//Retrieve hashtable
	TypedData_Get_Struct(hash, struct chashdata, &chashdata_type, data);

	long size = FIX2LONG(get_size(hash));
	if(size >= data->capacity){ //if not enough capacity
		struct node * temp[size];
		for(long i = 0, j = 0; i < data->capacity; i++){ //store nodes in temp
			node = data->hash[i];
			while(node){
				temp[j] = node;
				node = node->next;
				j++;
			}
		}
		data->capacity *= 2; //resize

		//rezalloc
		xfree(data->hash);
		data->hash = ZALLOC_N(struct node *, data->capacity);

		update_size(hash, -size); //size = 0

		//rehash
		for(long i = 0; i < size; i++)
			store(hash, temp[i]->key, temp[i]->val);
	}

	long hashkey = FIX2LONG(rb_funcall(key,  rb_intern("object_id"), 0));
	node = data->hash[hashkey % data->capacity];

	//Make new node
	if(node == NULL){
		node = ALLOC(struct node);
		node->key = key;
		node->val = val;
		node->next = NULL;
		data->hash[hashkey % data->capacity] = node;
		update_size(hash, 1);
		return hash;
	}
	if(RTEST(rb_equal(node->key, key))){
		node->val = val;
		return hash;
	}

	while(node->next){
		if(RTEST(rb_equal(node->next->key, key))){
			node->next->val = val;
			return hash;
		}
		node = node->next;
	}
	struct node * new_node = ALLOC(struct node);
	new_node->key = key;
	new_node->val = val;
	new_node->next = NULL;
	node->next = new_node;
	update_size(hash, 1);
	return hash;
}

static VALUE
delete(VALUE hash, VALUE key){
	struct chashdata * data;
	struct node * node;

	//Retrieve hashtable
	TypedData_Get_Struct(hash, struct chashdata, &chashdata_type, data);

	long hashkey = FIX2LONG(rb_funcall(key,  rb_intern("object_id"), 0));
	node = data->hash[hashkey % data->capacity];

	//Already deleted
	if(node == NULL)
		return Qnil;
	if(RTEST(rb_equal(node->key, key))){
		VALUE temp = node->val;
		data->hash[hashkey % data->capacity] = node->next;
		update_size(hash, -1);
		xfree(node);
		return temp;
	}

	//while(node.next.key != key)
	while(!RTEST(rb_equal(node->next->key, key))){
			if(node->next == NULL)
				return Qnil;
			node = node->next;
	}
	struct node * temp_node = node->next;
	VALUE temp = temp_node->val;
	node->next = node->next->next;
	xfree(temp_node);
	update_size(hash, -1);
	return temp;
}

static VALUE
each(VALUE hash){
	struct chashdata * data;
	struct node * node;

	//Retrieve hashtable
	TypedData_Get_Struct(hash, struct chashdata, &chashdata_type, data);

	for(long i = 0; i < data->capacity; i++){
		node = data->hash[i];
		while(node){
			rb_yield_values(2, node->key, node->val);
			node = node->next;
		}
	}
}

static VALUE
alloc(VALUE klass){
	return TypedData_Wrap_Struct(klass, &chashdata_type, 0);
}

static void
dealloc(void *ptr){
	struct chashdata *data = ptr;
	if(data){
		if(data->hash){
			for(long i = 0; i < data->capacity; i++){
				struct node *node = data->hash[i];
				struct node *temp_node = data->hash[i];
				while(node){
					node = node->next;
					xfree(temp_node);
					temp_node = node;
				}
			}
			xfree(data->hash);
		}
		xfree(data);
	}
}

static size_t
memsize_chash(const void *ptr){
	size_t size = 0;
	const struct chashdata *data = ptr;
	if (data) {
		size += sizeof(*data);
		if (data->hash) size += (sizeof(struct node *)*data->capacity);
	}
	return size;
}

Init_mychash(){
	/* define MyHash class */
	c_hash = rb_define_class("MyCHash", rb_cData);
	/* MyHash includes Enumerate module */
	rb_include_module(c_hash, rb_mEnumerable);

	rb_define_alloc_func(c_hash, alloc);

	/* MyHash instance method initialize(): variable (0 or 1) arguments */
	rb_define_method(c_hash, "initialize", init, -1);
	/* MyHash instance method fetch(): 1 argument */
	rb_define_method(c_hash, "fetch", fetch, 1);
	/* MyHash instance method []: alias for fetch */
	rb_define_alias(c_hash, "[]", "fetch");
	/* MyHash instance method store(): 2 arguments */
	rb_define_method(c_hash, "store", store, 2);
	/* MyHash instance method []=: alias for store */
	rb_define_alias(c_hash, "[]=", "store");
	/* MyHash instance method delete(): 1 argument */
	rb_define_method(c_hash, "delete", delete, 1);
	/* MyHash instance method size(): 0 arguments */
	rb_define_method(c_hash, "size", get_size, 0);
	/* MyHash instance method each(): 0 arguments */
	rb_define_method(c_hash, "each", each, 0);
}
