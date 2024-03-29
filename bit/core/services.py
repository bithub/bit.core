from zope.interface import implements

from twisted.python import log
from twisted.application.service import IServiceCollection, MultiService

from bit.core.interfaces import IServices


class Services(object):

    implements(IServices)

    def __init__(self, app):
        self.app = app
        self.collect = IServiceCollection(self.app)

    _multi = []
    _services = []

    def add(self, name, services):
        log.msg(
            'bit.core.services: Services.add %s, %s' % (name, services))
        if not isinstance(services, dict):
            services.setName(name)
            services.setServiceParent(self.collect)
            self._services.append(name)
            return

        add = True
        if name in self._multi:
            plug_services = self.collect.getServiceNamed(name)
            add = False
        else:
            plug_services = MultiService()
            plug_services.setName(name)
            self._multi.append(name)
        for sid, s in services.items():
            s.setName(sid)
            s.setServiceParent(plug_services)
        if add:
            plug_services.setServiceParent(self.collect)

    @property
    def services(self):
        _services = {}
        for service in (self._services + self._multi):
            _services[service] = self.collect.getServiceNamed(service)
        return _services
