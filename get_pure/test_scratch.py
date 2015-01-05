"""
# At root I want to be able to do this
MyClass.show_defaults(OtherClass)
MyClass.show_data(myobj)

Note: 'OtherClass'/'otherobj' are ~ another class that meets the 'interface'
    of MyClass (required to call show_data & show_defaults)


In Python 3, this works natively:
    MyClass.show_data(myobj)        # GOOD

Note: in Python 3, this does NOT work:
    MyClass.__dict__['show_defaults'](MyClass)
IE classmethods cannot be called directly from the dict

What DOES work, in Python 3, for instance methods:
    MyClass.show_data(myobj)
    MyClass.show_data(otherobj)
    type(myobj).show_data(myobj)
    type(myobj).show_data(otherobj)

? Now.... how to do this for classmethods
"""
#!/bin/python3

import types
import unittest


class Parentz(object):
    inherited = {'bing': 'bang'}
    def show_inherited(self):
        return self.inherited

class MyClass(Parentz):
    defaults = {'myclass_defaults': 'foo'}
    def __init__(self, data):
        self.data = data

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = None
        return self._data
    @data.setter
    def data(self, value):
        self._data = value

    yoodle_lambda = lambda self: "yoodle"

    # MyClass.show_data     --> function
    #
    # myobj.show_data       --> method (bound)
    #                           __self__ = Myclass
    def show_data(self):
        return self.data

    # MyClass.show_defaults --> method (bound)
    #                       __self__ = Myclass
    # myobj.show_defaults   --> method (bound)
    #                       __self__ = myobj
    @classmethod
    def show_defaults(cls):
        return cls.defaults


class OtherClass(object):

    def __init__(self, data):
        self.data = data
    defaults = {'otherclass_defaults': 'baz'}



def get_pure_function(method):
    """
    Retreive pure function, for a method.
    Depends on features specific to Python 2 CPython
    And hence does not work in Python 3 or non-CPython 2
    """
    # Already a pure function
    # 'instancemethod' pulled from class is this. Ex MyClass.method
    if isinstance(method, types.FunctionType):
        return method
    # Bound method  (~instance method on an instance)
    # requires shinanagins
    elif isinstance(method, types.MethodType):
        if isinstance(method, types.LambdaType):
            # Need to look for the name explicitly
            self = method.__self__
            # @todo: @refactor: This to seperate function
            for _name in dir(self):
                _method = getattr(self, _name)
                if _method == method:
                    name = _name
                    break
            # @todo: If this finds nothing -- add fallthrough error raise
            # Is a class
            if isinstance(self, type):
                cls = self
            # Is an instance
            else:
                cls = type(self)

            return getattr(cls, name)

        else: # not a lambda
            # NOTE - PROBLEM: This does not work for inherited methods
            self = method.__self__
            name = method.__name__

            # Is a class
            if isinstance(self, type):
                cls = self
            # Is an instance
            else:
                cls = type(self)

            return getattr(cls, name)


        self = method.__self__
        # This fails for lambdas
        name = method.__name__

    raise RuntimeError(str.format(
        "This fallthrough condition should never occur."
    ))



myobj = MyClass({'a':1})
otherobj = OtherClass({'b':2})

funcs = [
    MyClass.show_data,          # not method        pure function
    myobj.show_data,            # method

    MyClass.show_defaults,      # method
    myobj.show_defaults,        # method
]



def info(method):
    print(str.format(
        "'{name}', '{func}'\n"
        "    {ismethod} == is(MethodType)\n"
        "    {isfunction} == is(FunctionType)",
        func=method, name=method.__qualname__,
        ismethod=isinstance(method, types.MethodType),
        isfunction=isinstance(method, types.FunctionType)
    ))

for func in funcs:
    info(func)




import pdb
pdb.set_trace()
print()


# At root I want to be able to do this
MyClass.show_defaults(OtherClass)
MyClass.show_data(myobj)


class SurrogateTests(unittest.TestCase):

    def test_classmethod_non_surrogate(self):
        self.assertEqual(MyClass.show_defaults(), {'myclass_defaults':'foo'})
        self.assertEqual(myobj.show_defaults(), {'myclass_defaults':'foo'})

    def test_instance_non_surrogate(self):
        self.assertRaises(TypeError, lambda: MyClass.show_data)
        self.assertEqual(myobj.show_data(), {'a':1})
