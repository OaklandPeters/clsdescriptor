"""
Attempts to get a pure function, for a given method.

@todo: ADd error message for case that method exists on object, but not on class. EX Monkey patching
"""
import types
import sys

__all__ = [
    'get_pure'
]


def get_pure(method):
    """
    Dispatches based on Python version - since implementation
    must vary between Python 2 and Python 3.
    @type: method: types.Function or types.MethodType
    @rtype: types.Function
    """
    if sys.version[0] == 2:
        return get_pure_py2(method)
    elif sys.version[0] == 3:
        return get_pure_py3(method)
    else:
        raise PythonVersionError(str.format(
            "Do not know how to "
        ))

def get_pure_py2(method):
    #
    # This need filled in for Python 2
    # Not sure that .im_func exists for both instance and classmethods
    #
    #
    return method.im_func

def get_pure_py3(method):
    """
    Retreive pure function, for a method.
    This version works only for Python 3, but should be version
    independent (CPython, PyPy, JPython, etc).

    @type: method: types.Function or types.MethodType
    @rtype: types.Function
    """
    # Already a pure function
    # 'instancemethod' pulled from class is this. Ex MyClass.method
    if isinstance(method, types.FunctionType):
        return method
    # Bound method  (~instance method on an instance)
    # requires shinanagins
    elif isinstance(method, types.MethodType):
        self = method.__self__
        name = get_name(self, method)
        cls = ensure_is_class(self)

        if hasattr(cls, name):
            return getattr(cls, name)
        else:
            if hasattr(self, name):
                raise MethodNameNotFoundError(str.format(
                    "Method named '{0}' found on instance, but not on class '{1}'",
                    name, cls
                ))
            else:
                raise MethodNameNotFoundError(str.format(
                    "This fallthrough condition should never occur."
                ))

    raise RuntimeError(str.format(
        "This fallthrough condition should never occur."
    ))


def get_name(self, method):
    if hasattr(self, method.__name__):
        return method.__name__
    else:
        # Such as for Lambdas attached to a class or object
        for name in dir(self):
            if getattr(self, name) == method:
                return name

    raise MethodNameNotFoundError(str.format(
        "This fallthrough condition should never occur."
    ))

def ensure_is_class(self):
    if isinstance(self, type):
        return self
    else:
        return type(self)


class GetPureFunctionError(Exception):
    """Base class for all exceptions raised by this package."""
    pass

class MethodNameNotFoundError(GetPureFunctionError, AttributeError):
    pass

class PythonVersionError(GetPureFunctionError, EnvironmentError):
    pass
