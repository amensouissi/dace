# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from zope.interface.interfaces import IObjectEvent


class IRelationAdded(IObjectEvent):
    """A relation has been added.
    """


class IRelationDeleted(IObjectEvent):
    """A relation has been deleted.
    """


class IRelationModified(IObjectEvent):
    """A relation has been modified.
    """


class IRelationSourceDeleted(IObjectEvent):
    """The source of a relation has been deleted.
    """
    relation = Attribute(u"Relation")


class IRelationTargetDeleted(IObjectEvent):
    """The target of a relation has been deleted.
    """
    relation = Attribute(u"Relation")


class IRelationValue(Interface):
    """A simple relation One to One.
    """
    source_id = Attribute("oid of the source object")
    target_id = Attribute("oid of the target object")
    source = Attribute("The source object of the relation.")
    target = Attribute("The target object of the relation.")
    state = Attribute("State of the relation")
    from_interfaces_flattened = Attribute(
        "Interfaces of the from object, flattened. "
        "This includes all base interfaces.")
    to_interfaces_flattened = Attribute(
        "The interfaces of the to object, flattened. "
        "This includes all base interfaces.")
    tags = Attribute("List of tags (unicode).")
