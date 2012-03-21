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
        config = getUtility(IConfiguration)
        plugins = config.get('bot', 'plugins')

        snippet = "<include package='zope.component' />"
        zcml = zcml_template % snippet
        xmlconfig(StringIO(zcml))

        if isinstance(plugins, str):
            plugins = [plugins]

        log.msg('Loading interfaces and adapters')

        for plugin in plugins:
            snippet = "<include package='%s' />" % plugin
            zcml = zcml_template % snippet
            zcml_path = os.path.join(
                resolve(plugin).__path__[0], 'configure.zcml')
            if os.path.exists(zcml_path):
                log.msg('Loading configuration for: %s' % plugin)
                xmlconfig(StringIO(zcml))

        log.msg('Loading extensions')

        for plugin in plugins:
            snippet = "<include package='%s' file='meta.zcml' />" % plugin
            zcml = zcml_template % snippet
            zcml_path = os.path.join(resolve(plugin).__path__[0], 'meta.zcml')
            if os.path.exists(zcml_path):
                log.msg('Loading extensions for: %s' % plugin)
                xmlconfig(StringIO(zcml))

        log.msg('Loading plugins')

        for plugin in plugins:
            snippet = "<include package='%s' file='plugin.zcml' />" % plugin
            zcml = zcml_template % snippet
            zcml_path = os.path.join(
                resolve(plugin).__path__[0], 'plugin.zcml')
            if os.path.exists(zcml_path):
                log.msg('Loading plugin for: %s' % plugin)
                xmlconfig(StringIO(zcml))

        log.msg('Plugins loaded, loading legacy code')
