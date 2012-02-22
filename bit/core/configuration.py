
from ConfigParser import ConfigParser

from zope.component import getUtilitiesFor
from zope.interface import implements

from bit.core.interfaces import IConfiguration, IFileConfiguration

class Configuration(object):
    implements(IConfiguration)
    def sections(self):
        utils = getUtilitiesFor(IConfiguration)
        for utilid,util in utils:
            if not utilid: continue
            try:                    
                for section in util.sections():
                    yield section
            except:
                pass        

    def get(self,section,name=None):
        utils = getUtilitiesFor(IConfiguration)
        for utilid,util in utils:
            if utilid:
                try:
                    res = util.get(section,name)
                    if res: return res
                except:
                    pass


class FileConfiguration(object):
    implements(IFileConfiguration)
    def __init__(self,filename):
        self.filename = filename
        self.config = ConfigParser()
        self.config.read(filename)
    def sections(self):
        for section in self.config.sections():
            yield section
    def get(self,section,name=None):
        if not name:
            return [x for x,y in self.config.items(section)]
        results = self.config.get(section,name,raw=False)
        if '\n' in results.strip():
            results = [r.strip() for r in results.split('\n')]
        return results
