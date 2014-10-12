from __future__ import absolute_import
import unittest
from variantmethod import variantmethod

class Testvariantmethod(unittest.TestCase):
    def setUp(self):
        class MyClass(object):
            def __init__(self):
                pass
            @variantmethod
            def variant(self, first):
                return "self: {0}, first: {1}".format(type(self).__name__, first)
        self.MyClass = MyClass
    
    def test_classmethod(self):
        self.assertEqual(
            self.MyClass.variant('foo'), "self: type, first: foo"
        )
    def test_instancemethod(self):
        inst = self.MyClass()
        self.assertEqual(
            inst.variant('bar'), "self: MyClass, first: bar"
        )
        inst.variant = 'things'
        self.assertEqual(inst.variant, 'things')

if __name__ == "__main__":
    unittest.main()
