"""
# At root I want to be able to do this
MyClass.show_defaults(OtherClass)
MyClass.show_data(myobj)
"""
#!/bin/python3

import pprint
import types
import unittest

class MyClass(object):
    defaults = {'myclass_defaults': 'foo'}
    def __init__(self, data):
        self.data = data

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = data
        return self._data
    @data.setter
    def data(self, value):
        self._data = value

    yoodle_lambda = lambda self: "yoodle"

    def show_data(self):
        return self.data

    @classmethod
    def show_defaults(cls):
        return cls.defaults

    @staticmethod
    def show_values():
        return {'static_values': 'bazinga'}


class OtherClass(object):

    def __init__(self, data):
        self.data = data
    defaults = {'otherclass_defaults': 'baz'}



def get_pure_function(method):
    """
    Retreive pure function, for a method.
    Depends on features specific to CPython
    """
    assert(isinstance(method, types.MethodType))
    assert(hasattr(method, 'im_func'))

    return method.im_func



myobj = MyClass({'a':1})
otherobj = OtherClass({'b':2})

from_class = MyClass.show_data
from_instance = myobj.show_data

classmethod_from_class = MyClass.show_defaults
classmethod_from_instance = myobj.show_defaults

staticmethod_from_class = MyClass.show_values
staticmethod_from_instance = myobj.show_values

funcs = [
    from_class,
    from_instance,
    classmethod_from_class,
    classmethod_from_instance,
    staticmethod_from_class,
    staticmethod_from_instance
]

for func in funcs:
    print(func.__name__, hasattr(func, 'im_func'))

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
