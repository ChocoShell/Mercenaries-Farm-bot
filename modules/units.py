class UnitCreator(type):
    """A sample metaclass without any functionality"""

    def __new__(cls, clsname, superclasses, attributedict):
        print("clsname:", clsname)
        print("superclasses:", superclasses)
        print("attrdict:", attributedict)
        return super(UnitCreator, cls).__new__(
            cls, clsname, superclasses, attributedict
        )


C = UnitCreator("C", (object,), {})
print("class type:", type(C))
