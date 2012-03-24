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


class IConfiguration(I):

    def get(section, v):
        """ return variable v from section section """


class IFileConfiguration(IConfiguration):

    pass


class IStringConfiguration(IConfiguration):

    pass


class ISockets(I):

    pass


class IPluginExtender(I):

    pass
