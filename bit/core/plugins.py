import os
from StringIO import StringIO

from zope.dottedname.resolve import resolve
from zope.component import getUtility
from zope.interface import implements
from zope.configuration.xmlconfig import xmlconfig

from twisted.python import log

from bit.core.interfaces import IPlugins, IConfiguration

zcml_template = """\
       <configure xmlns='http://namespaces.zope.org/zope'
                  i18n_domain="zope">
       %s
       </configure>"""


class Plugins(object):

    implements(IPlugins)

    def loadPlugins(self):
        log.err('bit.core.plugins: loadPlugins')

        config = getUtility(IConfiguration)
        plugins = config.get('bot', 'plugins')

        snippet = "<include package='zope.component' />"
        zcml = zcml_template % snippet
        xmlconfig(StringIO(zcml))

        if isinstance(plugins, str):
            plugins = [plugins]

        for plugin in plugins:
            snippet = "<include package='%s' />" % plugin
            zcml = zcml_template % snippet
            zcml_path = os.path.join(
                resolve(plugin).__path__[0], 'configure.zcml')
            if os.path.exists(zcml_path):
                xmlconfig(StringIO(zcml))

        for plugin in plugins:
            snippet = "<include package='%s' file='meta.zcml' />" % plugin
            zcml = zcml_template % snippet
            zcml_path = os.path.join(resolve(plugin).__path__[0], 'meta.zcml')
            if os.path.exists(zcml_path):
                xmlconfig(StringIO(zcml))

        for plugin in plugins:
            snippet = "<include package='%s' file='plugin.zcml' />" % plugin
            zcml = zcml_template % snippet
            zcml_path = os.path.join(
                resolve(plugin).__path__[0], 'plugin.zcml')
            if os.path.exists(zcml_path):
                xmlconfig(StringIO(zcml))


