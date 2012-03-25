import io
import os
from ConfigParser import ConfigParser

from zope.component import getUtilitiesFor, provideUtility
from zope.interface import implements

from bit.core.interfaces import IConfiguration,\
    IFileConfiguration, IStringConfiguration


class Configuration(object):

    implements(IConfiguration)

    def __init__(self):
        provideUtility(self, IConfiguration)

    def register(self, configuration, name):
        if not IConfiguration.providedBy(configuration):
            return
        provideUtility(configuration, IConfiguration, name=name)

    def sections(self):
        utils = getUtilitiesFor(IConfiguration)
        for utilid, util in utils:
            if not utilid:
                continue
            try:
                for section in util.sections():
                    yield section
            except:
                pass

    def get(self, section, name=None):
        utils = getUtilitiesFor(IConfiguration)
        for utilid, util in utils:
            if utilid:
                try:
                    res = util.get(section, name)
                    if res:
                        return res
                except:
                    pass


class BaseConfiguration(object):

    def sections(self):
        for section in self.config.sections():
            yield section

    def get(self, section, name=None):
        if not name:
            return [x for x, y in self.config.items(section)]
        results = self.config.get(section, name, raw=False)
        if '\n' in results.strip():
            results = [r.strip() for r in results.split('\n')]
        return results


class StringConfiguration(BaseConfiguration):

    implements(IStringConfiguration)

    def __init__(self, string_config):
        self.config = ConfigParser(allow_no_value=True)
        self.config.readfp(io.BytesIO(string_config))

    def set(self, section, k, v):
        raise NotImplementedError


class FileConfiguration(BaseConfiguration):

    implements(IFileConfiguration)

    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser()
        self.config.read(filename)


class FileConfigurationLoader(object):

    def __init__(self, config):
        self.config = config

    def load(self):
        configuration = Configuration()
        file_configuration = FileConfiguration(self.config['config'])
        provideUtility(configuration, IConfiguration)
        provideUtility(file_configuration, IConfiguration, name='default')
        for extension in [x.strip() for x
                          in configuration.get('bit', 'extends')]:
            provideUtility(FileConfiguration(extension),
                           IConfiguration, name=os.path.basename(extension))
        return configuration


class StringConfigurationLoader(object):

    def __init__(self, config):
        self.config = config

    def load(self):
        configuration = Configuration()
        string_configuration = StringConfiguration(self.config)
        provideUtility(configuration, IConfiguration)
        provideUtility(string_configuration, IConfiguration, name='default')
        for extension in [x.strip() for x
                          in configuration.get('bit', 'extends') or []]:
            provideUtility(FileConfiguration(extension),
                           IConfiguration, name=os.path.basename(extension))
        return configuration
