from zope.interface import implements
from zope.component import provideUtility

# this is necessary to activate the event architecture
import zope.component.event
# and this is for pyflakes
zope.component.event

from bit.core.interfaces import IPlugin


class BitPlugin(object):

    implements(IPlugin)
    _services = {}
    _utils = []

    @property
    def name(self):
        return '%s.%s' % (self.__module__, self.__class__.__name___)

    @property
    def utils(self):
        return self._utils

    def load_utils(self):
        for util, iface in self.utils:
            if isinstance(iface, list):
                name, iface = iface
                provideUtility(util, iface, name=name)
            else:
                provideUtility(util, iface)

    @property
    def services(self):
        return self._services

    def load_sockets(self):
        pass

    def load_adapters(self):
        pass
