from zope.interface import alsoProvides, implements
from zope.component import provideUtility, provideAdapter

from twisted.application import service
from twisted.internet import defer

from bit.core.interfaces import IApplication, IServices,\
    IConfiguration, IPlugins, IApplicationRunner
from bit.core.plugins import Plugins
from bit.core.services import Services


class ApplicationRunner(object):

    implements(IApplicationRunner)

    def __init__(self, config):
        self.config = config
        application = service.Application(
            self.config.get('bit', 'name').capitalize(), uid=1001, gid=1001)
        self.s = service.IServiceCollection(application)
        #self.s.setServiceParent(application)
        alsoProvides(application, IApplication)
        provideUtility(application, IApplication)
        provideUtility(Services(application), IServices)
        plugins = Plugins()
        provideUtility(plugins, IPlugins)
        plugins.loadPlugins()
        defer.setDebugging(True)

    @property
    def service(self):
        return self.s

    def start(self):
        self.service.startService()

    def stop(self):
        self.service.stopService()

provideAdapter(ApplicationRunner, [IConfiguration], IApplicationRunner)
