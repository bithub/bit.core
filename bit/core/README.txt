bit.core
========

loading configuration
---------------------

Once registered the IConfiguration utility provides access to configuration variables

  >>> import zope
  >>> import bit.core
  >>> zope.component.provideUtility(
  ...     bit.core.configuration.Configuration(),
  ... 	  bit.core.interfaces.IConfiguration)

  >>> config = zope.component.getUtility(bit.core.interfaces.IConfiguration)
  >>> config 
  <bit.core.configuration.Configuration ...>

  >>> [x for x in config.sections()]
  []

Now if we register a named configuration utility the IConfiguration utility will use it

  >>> test_configuration = """
  ... [bit]
  ... name = testapp
  ... plugins = bit.core
  ... """

  >>> zope.component.provideUtility(
  ...     bit.core.configuration.StringConfiguration(test_configuration),
  ... 	  bit.core.interfaces.IConfiguration,
  ...	  name='test_config')

Our config utility now has the bit section

  >>> [x for x in config.sections()]
  ['bit']

We can also register the config provider directly with the IConfiguration utility

  >>> test_configuration_2 = """
  ... [bit2]
  ... name = testapp2
  ... plugins = bit.core
  ... """
  >>> config.register(
  ...    bit.core.configuration.StringConfiguration(test_configuration_2))

  >>> sorted([x for x in config.sections()])
  ['bit', 'bit2']


create a bit.core app
---------------------

We can use our configuration to create an application runner

  >>> runner = bit.core.interfaces.IApplicationRunner(config)


The runner contains a variable "service" which is the app's service collection

  >>> runner.service
  <twisted.application.service.MultiService instance ...> 


We can now get the application

  >>> import zope
  >>> app = zope.component.getUtility(bit.core.interfaces.IApplication)
  >>> app
  <twisted.python.components.Componentized instance ...>


Lets check our service collection is the same as the one provided by the runner

  >>> import twisted
  >>> runner.service == twisted.application.service.IServiceCollection(app)
  True


services
--------

Services are registered as with the IServices utility using zcml

  >>> services = zope.component.getUtility(bit.core.interfaces.IServices)
  >>> services
  <bit.core.services.Services ...>


Let's check there are none registered so far

  >>> services.services
  {}


registering services
--------------------

We can add multiservices using a named dictionary

  >>> from twisted.application import internet
  >>> from twisted.manhole import telnet

  >>> foo_services = {}
  >>> foo_services['bar'] = internet.TCPServer(
  ...				9393, telnet.ShellFactory())
  >>> services.add('foo', foo_services)

  >>> 'foo' in services.services
  True

  >>> foo = services.services['foo']
  >>> foo
  <twisted.application.service.MultiService ...>

  >>> foo.name
  'foo'

  >>> foo.parent == runner.service
  True

  >>> foo.getServiceNamed('bar')
  <twisted.application.internet.TCPServer ...>


Lets create a helper for running zcml through

  >>> from cStringIO import StringIO
  >>> from zope.configuration.xmlconfig import xmlconfig
  >>> def runSnippet(snippet):
  ...     template = """\
  ...     <configure xmlns='http://namespaces.zope.org/zope'
  ...                i18n_domain="zope">
  ...     %s
  ...     </configure>"""
  ...     xmlconfig(StringIO(template % snippet))

We can add a service using a zcml service directive

  >>> runSnippet('''
  ... <service
  ...	parent="bit.core"
  ...	name="test-service"
  ... 	service="twisted.application.internet.TCPServer"
  ...  	port="bit.core.testing.getTestPort"
  ...  	factory="twisted.manhole.telnet.ShellFactory"
  ...   /> ''')


If the parent is specified, a mulit-service will be added

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


We can add another service to our multi-service by giving it the same parent

  >>> runSnippet('''
  ... <service
  ...	parent="bit.core"
  ...	name="test-service-2"
  ... 	service="twisted.application.internet.TCPServer"
  ...  	port="bit.core.testing.getTestPort2"
  ...  	factory="twisted.manhole.telnet.ShellFactory"
  ...   /> ''')

  >>> testservice2 = multiservice.getServiceNamed('test-service-2')
  >>> testservice2
  <twisted.application.internet.TCPServer ...>

