class classproperty(property):
    """Provides a getter-property for classmethods. Due to complicated reasons,
    there is no way to make classmethod setter-properties work in Python
    """
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()
