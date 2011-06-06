import collections
import logging
import itertools
import abc

from schemaorg.multidict import UnorderedMultiDict

def is_nonstring_iterable(thing):
    return isinstance(thing, collections.Iterable) and not isinstance(thing, basestring)

noop = lambda x: x

class MultiDict(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        # super(MultiDict, self).__init__(*args, **kwargs)
        super(MultiDict, self).__init__()
        self.data = collections.defaultdict(list)
        if len(args) == 1:
            if isinstance(args[0], collections.Mapping):
                for (k, v) in args[0].items():
                    if is_nonstring_iterable(v):
                        self.data[k].extend(v)
                    else:
                        self.data[k].append(v)
            else:
                raise TypeError("%s expected a Mapping type as the positional argument" % (type(self).__name__,))
        elif args:
            raise TypeError("%s expected at most arguments, got %d" % (type(self).__name__, len(args)))
        for (k, v) in kwargs.items():
            if is_nonstring_iterable(v):
                self.data[k].extend(v)
            else:
                self.data[k].append(v)
    
    def __getitem__(self, key):
        val = self.data[key]
        if len(val) == 1:
            return val[0]
        else:
            return val
    
    def __delitem__(self, key):
        self.data.__delitem__(key)
    
    def __setitem__(self, key, value):
        if is_nonstring_iterable(value):
            self.data[key].extend(value)
        else:
            self.data[key].append(value)
    
    def __len__(self):
        return sum(map(len, self.data.values()))
    
    def __iter__(self):
        return self.data.__iter__()
    
    def getall(self, key):
        return self.data[key]
    
    def getone(self, key):
        return self.data[key][-1]
    
    def values(self):
        return list(self.itervalues())
    
    def itervalues(self):
        return itertools.chain.from_iterable(self.data.values())
    

class BaseMetaClass(abc.ABCMeta):  
    def __new__(meta, classname, bases, class_dict):
        properties = {}
        parents = []
        for b in bases:
            properties.update(getattr(b, 'properties', {}))
        properties.update(class_dict.get('properties', {}))
        class_dict['properties'] = properties
        klass = super(BaseMetaClass, meta).__new__(meta, classname, bases, class_dict)
        klass.parents = [k.__name__ for k in klass.__mro__ if hasattr(k, 'properties')]
        return klass

class Base(MultiDict):
    properties = {}
    
    __metaclass__ = BaseMetaClass
    
    _base_URL = ''
    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        for k in self.data:
            action = self.properties.get(k, noop)
            if not isinstance(action, collections.Callable):
                action = self.import_class(action)
            self.data[k] = map(action, self.data[k])
    
    def __repr__(self):
        return "<%s %s>" % (type(self).__name__, self.data)
    
    def items(self):
        normal_items = super(Base, self).items()
        # normal_items.append(('itemtype', self.schema_url))
        # normal_items.append(('type', type(self).__name__))
        return normal_items
    
    def __iter__(self):
        normal_items = super(Base, self).__iter__()
        additional = ('itemtype', 'type')
        return itertools.chain(normal_items, additional)
    
    def __getitem__(self, key):
        if key in self.data:
            return super(Base, self).__getitem__(key)
        elif key == 'type':
            return type(self).__name__
        elif key == 'itemtype':
            return self.schema_url
    
    def __setitem__(self, key, value):
        action = self.properties.get(key, noop)
        if not isinstance(action, collections.Callable):
            action = self.import_class(action)
        if is_nonstring_iterable(value):
            value = map(action, value)
        else:
            value = action(value)
        super(Base, self).__setitem__(key, value)
    
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
