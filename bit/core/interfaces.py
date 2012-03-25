from zope.interface import Interface as I


class IRequest(I):

    def load(session, body):
        """ load a request for session """


class ICommand(I):

    def load(session, body):
        """ load a request for session """


class IServices(I):

    def services():
        """ services """


class IApplication(I):

    def start():
        """ start the application """

    def stop():
        """ stop the application """


class IApplicationRunner(I):

    def start():
        """ start the application """

    def stop():
        """ stop the application """


class IPlugin(I):

    pass


class IPlugins(I):

    pass


class IPersistent(I):
    """ Marker interface for persistent entities """


class IConfiguration(I):

    def get(section, v):
        """ return variable v from section section """

    def set(section, k, v):
        """ set the k to v for section in whatever way we can"""


class IPersistentConfiguration(IConfiguration, IPersistent):
    """ Persistent configuration interface """

    def set(section, k, v):
        """ set the k to v for section """


class IFileConfiguration(IPersistentConfiguration):

    def set(section, k, v):
        """ set the k to v for section in the relevant file"""


class IStringConfiguration(IConfiguration):

    def set(section, k, v):
        """ raises NotImplementedError """


class IInMemoryConfiguration(IConfiguration):

    def set(section, k, v):
        """ set the k to v for section in RAM for the lifetime of this server """


class ISockets(I):

    pass


class IPluginExtender(I):

    pass
