
import os
import inspect
from zope.interface import implements
from zope.component import getUtility, provideUtility, provideHandler,provideAdapter

# this is necessary to activate the event architecture
import zope.component.event
# and this is for pyflakes
zope.component.event

from twisted.application.service import IServiceCollection
from twisted.web import static

from bit.core.interfaces import IPlugin, IServices

class BitPlugin(object):
    implements(IPlugin)
    _services = {}
    _utils = []

    @property
    def name(self):
        return '%s.%s' %(self.__module__,self.__class__.__name___)

    @property
    def utils(self):
        return self._utils

    def load_utils(self):
        for util,iface in self.utils:
            if isinstance(iface,list):
                name,iface = iface
                provideUtility(util,iface,name=name)
            else:
                provideUtility(util,iface)

    @property
    def services(self):
        return self._services


    def load_sockets(self): 
        pass

    def load_adapters(self):         
        pass

