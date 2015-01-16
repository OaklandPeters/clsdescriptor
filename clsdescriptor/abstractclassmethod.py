class abstractclassmethod(classmethod): #pylint: disable=invalid-name
    """A decorator indicating abstract classmethods, similar to abstractmethod.
    Requires that the class descend from abc.ABCMeta.
    This is a backport of the abstract-class-method from Python 3.2 to Python 2.6.
    """
    __isabstractmethod__ = True

    def __init__(self, a_callable):
        #assert(issubclass(callable, abc.ABCMeta)), "object is not a subclass of ABCMeta."
        #assert(callable(a_callable)), "object is not callable."
        a_callable.__isabstractmethod__ = True
        super(type(self), self).__init__(a_callable) #pylint: disable=bad-super-call
