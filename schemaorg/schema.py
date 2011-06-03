
class Boolean(bool):
    pass

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

class Base(object):
    _properties = {}
    _own_properties = {}
    def __init__(self, **kwargs):
        super(Base, self).__init__()
        self._properties.update(self._own_properties)
        for (k, v) in kwargs.items():
            setattr(self, k, self._properties.get(k, unicode)(v))
    
    def __repr__(self):
        return "{0}({1})".format(type(self).__name__, ', '.join(["%s=%s" % kv for kv in vars(self).items()]))

class Thing(Base):
    _own_properties = {'description': Text,
                       'image': URL,
                       'name': Text,
                       'url': Text}
    schema_url = 'http://schema.org/Thing'

class NumberedThing(Thing):
    _own_properties = {'number': Float, 'age': Integer}
