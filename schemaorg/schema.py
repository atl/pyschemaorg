
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

class Base(object):
    _properties = {}
    __metaclass__ = BaseMetaClass
    def __init__(self, **kwargs):
        for (k, v) in kwargs.items():
            setattr(self, k, self._properties.get(k, unicode)(v))
    
    def __repr__(self):
        return "{0}({1})".format(type(self).__name__, ', '.join(["%s=%s" % kv for kv in vars(self).items()]))

class Thing(Base):
    _properties = {'description': Text,
                         'image': URL,
                          'name': Text,
                           'url': Text}
    schema_url = 'http://schema.org/Thing'

class NumberedThing(Thing):
    _properties = {'number': Float, 
                      'age': Integer}
