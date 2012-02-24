
import os
from zope.dottedname.resolve import resolve  
from zope.component import getUtility

from zope.interface import implements

from bit.core.interfaces import IPlugins, IPlugin, IConfiguration
from StringIO import StringIO
from zope.configuration.xmlconfig import xmlconfig

zcml_template = """\
       <configure xmlns='http://namespaces.zope.org/zope'
                  i18n_domain="zope">
       %s
       </configure>"""

class Plugins(object):
    implements(IPlugins)

    def loadPlugins(self):
        config = getUtility(IConfiguration)
        plugins = config.get('bot','plugins')
        snippet = "<include package='zope.component' />" 
        zcml = zcml_template % snippet
        xmlconfig(StringIO(zcml))
        if isinstance(plugins,str): plugins = [plugins]
        _plugins = []
        for plugin in plugins:
            plug = resolve(plugin.strip())()
            if IPlugin.providedBy(plug): _plugins.append(plug)
            package = plugin.strip().split('.plugin.')[0]
            snippet = "<include package='%s' />" %package
            zcml = zcml_template % snippet            
            zcml_path = os.path.join(resolve(package).__path__[0],'configure.zcml')
            if os.path.exists(zcml_path):
                xmlconfig(StringIO(zcml))

        for plugin in plugins:                    
            package = plugin.strip().split('.plugin.')[0]
            snippet = "<include package='%s' file='meta.zcml' />" %package
            zcml = zcml_template % snippet
            zcml_path = os.path.join(resolve(package).__path__[0],'meta.zcml')
            if os.path.exists(zcml_path):
                xmlconfig(StringIO(zcml))

        for plugin in plugins:        
            package = plugin.strip().split('.plugin.')[0]
            snippet = "<include package='%s' file='plugin.zcml' />" %package
            zcml = zcml_template % snippet
            zcml_path = os.path.join(resolve(package).__path__[0],'plugin.zcml')
            if os.path.exists(zcml_path):
                xmlconfig(StringIO(zcml))
                
        for auto in ['utils',]:
            for plug in _plugins:
                if hasattr(plug,'load_%s' %auto):
                    getattr(plug,'load_%s' %auto)()

