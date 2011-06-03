from schemaorg.multidict import UnorderedMultiDict

Boolean = bool

class Date(object):
    pass

class Float(float):
    pass

class Integer(int):
    pass

class Text(unicode):
    pass

class URL(Text):
    pass

class BaseMetaClass(type):
    def __new__(meta, classname, bases, class_dict):
        properties = {}
        for b in reversed(bases):
            properties.update(getattr(b, '_properties', {}))
        properties.update(class_dict['_properties'])
        class_dict['_properties'] = properties
        return type.__new__(meta, classname, bases, class_dict)

class Base(UnorderedMultiDict):
    _properties = {}
    
    __metaclass__ = BaseMetaClass
    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__()
        if len(args) == 1:
            if hasattr(args[0], '__getitem__'):
                for (k, v) in args[0].items():
                    self[k] = self._properties.get(k, unicode)(v)
            else:
                raise TypeError("%s expected a Mapping type as the positional argument" % (type(self).__name__,))
        elif args:
            raise TypeError("%s expected at most arguments, got %d" % (type(self).__name__, len(args)))
        for (k, v) in kwargs.items():
            self[k] = self._properties.get(k, unicode)(v)
    
    def __repr__(self):
        return "<%s %s>" % (type(self).__name__, self.data)
    
    def update(self, *args, **kwargs):
        if len(args) == 1:
            if hasattr(args[0], '__getitem__'):
                for (k, v) in args[0].items():
                    self[k] = v
            else:
                raise TypeError("update expected a Mapping type as the positional argument")
        elif args:
            raise TypeError("update expected at most arguments, got %d" % (len(args),))
        for (k, v) in kwargs.items():
            self[k] = v
    

class Thing(Base):
    _properties = {'description': Text,
                         'image': URL,
                          'name': Text,
                           'url': Text}
    schema_url = 'http://schema.org/Thing'

class NumberedThing(Thing):
    _properties = {'number': Float, 
                      'age': Integer}
