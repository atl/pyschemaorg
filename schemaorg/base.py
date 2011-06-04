import collections

from schemaorg.multidict import UnorderedMultiDict

class BaseMetaClass(type):
    def __new__(meta, classname, bases, class_dict):
        properties = {}
        for b in reversed(bases):
            properties.update(getattr(b, 'properties', {}))
        properties.update(class_dict.get('properties', {}))
        class_dict['properties'] = properties
        return type.__new__(meta, classname, bases, class_dict)

class Base(UnorderedMultiDict):
    properties = {}
    
    __metaclass__ = BaseMetaClass
    
    _base_URL = ''
    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__()
        if len(args) == 1:
            if hasattr(args[0], '__getitem__'):
                for (k, v) in args[0].items():
                    self[k] = self.properties.get(k, unicode)(v)
            else:
                raise TypeError("%s expected a Mapping type as the positional argument" % (type(self).__name__,))
        elif args:
            raise TypeError("%s expected at most arguments, got %d" % (type(self).__name__, len(args)))
        for (k, v) in kwargs.items():
            action = self.properties.get(k, unicode)
            if isinstance(action, collections.Callable):
                self[k] = action(v)
            else:
                self[k] = self.import_class(action)(v)
    
    def __repr__(self):
        return "<%s %s>" % (type(self).__name__, self.data)
    
    def update(self, *args, **kwargs):
        if len(args) == 1:
            if hasattr(args[0], '__getitem__'):
                for (k, v) in args[0].items():
                    self[k] = self.properties.get(k, unicode)(v)
            else:
                raise TypeError("update expected a Mapping type as the positional argument")
        elif args:
            raise TypeError("update expected at most arguments, got %d" % (len(args),))
        for (k, v) in kwargs.items():
            self[k] = self.properties.get(k, unicode)(v)
    
    @property
    def schema_url(self):
        return "%s%s" % (self._base_URL, type(self).__name__)
    
    # http://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname/3610097#3610097
    def import_class(self, class_string):
        """Returns class object specified by a string.

        Args:
            class_string: The string representing a class.

        Raises:
            ValueError if module part of the class is not specified.
        """
        module_name, _, class_name = class_string.rpartition('.')
        if module_name == '':
            module_name = self.__module__
        return getattr(
            __import__(module_name, globals(), locals(), [class_name], -1),
            class_name)
    
