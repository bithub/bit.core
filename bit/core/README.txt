bit.core
========

create a bit.core app
---------------------

First we need to load an application

  >>> import bit

  >>> test_configuration = """
  ... [bot]
  ... name = testapp
  ... plugins = bit.core
  ... """
		
  >>> configuration = bit.core.configuration.Configuration()
  >>> configuration.register(
  ...    bit.core.configuration.StringConfiguration(test_configuration))

  >>> runner = bit.core.interfaces.IApplicationRunner(configuration)


The runner contains a variable service which is the app's service collection

  >>> runner.service
  <twisted.application.service.MultiService ...> 


We can now get the application

  >>> import zope
  >>> app = zope.component.getUtility(bit.core.interfaces.IApplication)
  >>> app
  <twisted.python.components.Componentized instance ...>


zcml directives
---------------

This helper will let us easily execute ZCML snippets:

  >>> from cStringIO import StringIO
  >>> from zope.configuration.xmlconfig import xmlconfig
  >>> def runSnippet(snippet):
  ...     template = """\
  ...     <configure xmlns='http://namespaces.zope.org/zope'
  ...                i18n_domain="zope">
  ...     %s
  ...     </configure>"""
  ...     xmlconfig(StringIO(template % snippet))


services
--------

Services are registered as with the IServices utility using zcml

  >>> services = zope.component.getUtility(bit.core.interfaces.IServices)
  >>> services
  <bit.core.services.Services ...>


Let's check there are none registered so far

  >>> services.services
  {}


register a service
------------------

Lets add a service using a zcml service directive

  >>> runSnippet('''
  ... <service
  ...	parent="bit.core"
  ...	name="test-service"
  ... 	service="twisted.application.internet.TCPServer"
  ...  	port="bit.core.testing.getTestPort"
  ...  	factory="twisted.manhole.telnet.ShellFactory"
  ...   /> ''')


All services belong to a multi-service whose name is specified by parent in the service directive

  >>> 'bit.core' in services.services
  True

  >>> multiservice = services.services['bit.core']
  >>> multiservice
  <twisted.application.service.MultiService ...>

  >>> testservice = multiservice.getServiceNamed('test-service')
  >>> testservice
  <twisted.application.internet.TCPServer ...>

  >>> testservice.args
  (23232, <twisted.manhole.telnet.ShellFactory instance ...>)
