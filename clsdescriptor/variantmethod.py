from __future__ import absolute_import
import types

__all__ = ['variantmethod']

class variantmethod(object):
    def __init__(self, func):
        self.func = func
        if hasattr(func, '__name__'):
            self.name = func.__name__
        else:
            self.name = repr(func)

    def __get__(self, obj, objtype=None):
        if obj is None: #classmethod
            return types.MethodType(self.func, objtype)
        else:  #instancemthod
            return types.MethodType(self.func, obj)
