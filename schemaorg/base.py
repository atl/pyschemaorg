import collections
import logging

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

def get_itemtype_mapping_from_classes(classlist):
    mapping = {}
    for cl in classlist:
        try:
            mapping[cl().schema_url] = cl
        except AttributeError:
            pass
    return mapping

def get_type_mapping_from_classes(classlist):
    mapping = {}
    for cl in classlist:
        mapping[cl.__name__] = cl
    return mapping

def resolve_from_candidates(propertylist, classlist):
    propertyset = set(propertylist)
    class_properties = {}
    for cl in classlist:
        class_properties[cl] = set(cl.properties.keys())
    class_mapper = []
    for cl in classlist:
        rest = list(classlist)
        rest.remove(cl)
        other_properties = [class_properties[r] for r in rest]
        unique_props = class_properties[cl].difference(*other_properties)
        class_mapper.append((cl,unique_props))
    class_mapper.sort(key=lambda x: len(x[1]))
    cm_score = []
    for (cl, uniqs) in class_mapper:
        score = len(uniqs.intersection(propertyset)) / float(len(uniqs) or 1)
        print("%s, %f" % (cl.__name__, score))
        cm_score.append((cl, score))
    cm_score.sort(key=lambda x: x[1], reverse=True)
    winner = cm_score[0]
    if winner[1] == 0:
        winner = class_mapper[0]
    return winner[0]
