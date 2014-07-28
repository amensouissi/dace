from persistent.list import PersistentList

from dace.descriptors import Descriptor

_marker = object()


class CompositeMultipleProperty(Descriptor):
    def __init__(self, propertyref='', opposite=None, isunique=False):
        self.propertyref = propertyref
        self.opposite = opposite
        self.isunique = isunique
        self.key = propertyref + '_contents_keys'

    def _get(self, obj):
        contents_keys = obj.__dict__.get(self.key, None)
        if contents_keys is not None:
            return [obj[key] for key in contents_keys]

        return []

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        return self._get(obj)

    def add(self, obj, value, initiator=True):
        if value is None:
            return

        self.init(obj)
        contents_keys = obj.__dict__[self.key]

        current_values = self._get(obj)
        if self.isunique and value in current_values:
            return

        value_name = value.__name__
        if getattr(value, '__property__', None) is not None:
            getattr(value.__parent__.__class__, value.__property__).remove(value.__parent__, value)
        elif getattr(value, '__parent__', None) is not None:
            value.__parent__.remove(value_name)

        obj.add(value_name, value)
        value.__property__ = self.propertyref
        contents_keys.append(value.__name__)
        setattr(obj, self.key, contents_keys)

        if initiator and self.opposite is not None:
            opposite_property = getattr(value.__class__, self.opposite, _marker)
            if opposite_property is not _marker:
                opposite_property.add(value, obj, False)

    def __set__(self, obj, values, initiator=True):
        if not isinstance(values, (list, tuple, set)):
            values = [values]

        oldvalues = self._get(obj)
        toremove = []
        toadd = []
        if values is None:
            toremove = oldvalues
        else:
            toremove = [v for v in oldvalues if v not in values]
            toadd = [v for v in values if v not in oldvalues]

        # FIXME should iterate over toremove and call self.remove
        self.remove(obj, toremove)
        for v in toadd:
            self.add(obj, v)

    # FIXME not the same signature as compositeunique
    def remove(self, obj, values, initiator=True):
        self.init(obj)
        contents_keys = obj.__dict__[self.key]
        if not isinstance(values, (list, tuple, set)):
            values = [values]

        for value in values:
            if initiator and self.opposite is not None:
                opposite_property = getattr(value.__class__, self.opposite, _marker)
                if opposite_property is not _marker:
                    opposite_property.remove(value, obj, False)

            value_name = value.__name__
            if value_name is not None and value_name in obj:
                contents_keys.remove(value_name)
                obj.remove(value_name)

    def init(self, obj):
        if getattr(obj, self.key, _marker) is _marker:
            setattr(obj, self.key, PersistentList())