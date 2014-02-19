from zope.interface import Interface, implements, Declaration
from pyramid.threadlocal import get_current_registry

from substanced.util import get_oid
from substanced.catalog import (
    catalog_factory,
    Field,
    Keyword,
    Text,
    indexview,
    indexview_defaults,
    )
from dace.util import Adapter, adapter

from ..interfaces import IBusinessAction

class ISearchableBusinessAction(Interface):
    def process_id():
        pass
    def node_id():
        pass
    def process_inst_uid():
        pass
    def context_id():
        pass

@indexview_defaults(catalog_name='searchablebusinessaction')
class SearchableBusinessActionViews(object):
    def __init__(self, resource):
        self.resource = resource

    @indexview()
    def process_id(self, default):
        adapter = get_current_registry().queryAdapter(self.resource,ISearchableBusinessAction)
        if adapter is None:
            return default
        return adapter.process_id()

    @indexview()
    def node_id(self, default):
        adapter = get_current_registry().queryAdapter(self.resource,ISearchableBusinessAction)
        if adapter is None:
            return default
        return adapter.node_id()

    @indexview()
    def process_inst_uid(self, default):
        adapter = get_current_registry().queryAdapter(self.resource,ISearchableBusinessAction)
        if adapter is None:
            return default
        return adapter.process_inst_uid()

    @indexview()
    def context_id(self, default):
        adapter = get_current_registry().queryAdapter(self.resource,ISearchableBusinessAction)
        if adapter is None:
            return default
        return adapter.context_id()


@catalog_factory('searchablebusinessaction')
class SearchableBusinessActionFactory(object):
    #grok.context(ISearchableWorkItem)

    process_id = Field()
    node_id = Field()
    process_inst_uid = Keyword()
    context_id = Keyword()


@adapter(context = IBusinessAction, name = u'businessactionsearch' )
class BusinessActionSearch(Adapter):
    implements(ISearchableBusinessAction)

    def process_id(self):
        return self.context.process_id

    def node_id(self):
        return self.context.node_id

    def process_inst_uid(self):
        return [get_oid(self.context.__parent__.__parent__, None)]

    def context_id(self):
        return [i.__identifier__ for i in Declaration(self.context.context).flattened()]
