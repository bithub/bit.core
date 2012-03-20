

from zope.interface import Interface as I

class IServices(I):
    def services():
        """ services """

class IApplication(I):
    def start():
        """ start the application """

    def stop():
        """ stop the application """

class IPlugin(I):
    pass

class IPlugins(I):
    pass

class IConfiguration(I):
    def get(section,v):
        """ return variable v from section section """

class IFileConfiguration(IConfiguration):
    pass

class ISockets(I):
    pass

class IPluginExtender(I):
    pass


