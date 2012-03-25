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


registering services with python
--------------------------------

First lets grab the IServices utility

  >>> services = zope.component.getUtility(bit.core.interfaces.IServices)
  >>> services
  <bit.core.services.Services ...>


Let's check there are none registered so far

  >>> services.services
  {}


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

  >>> bar = foo.getServiceNamed('bar')
  >>> bar
  <twisted.application.internet.TCPServer ...>

  >>> bar.name
  'bar'


registering a service with zcml
-------------------------------

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

  >>> sorted(services.services['bit.core'].namedServices.keys())
  [u'test-service', u'test-service-2']

  >>> testservice2 = multiservice.getServiceNamed('test-service-2')
  >>> testservice2
  <twisted.application.internet.TCPServer ...>

As per twisted, services can be controlled by their parents

  >>> multiservice.running
  1
	
  >>> testservice2.running
  1

  >>> def _stopped(resp):
  ...	  if not testservice2.running == 0:
  ...		print 'ERROR: testservice2 is not running'
  ...	  multiservice.startService()
  ...	  if not testservice2.running == 1:
  ...		print 'ERROR: testservice2 is not running'

  >>> d = multiservice.stopService()
  >>> d.addCallback(_stopped)
  <DeferredList at ...>


registering a command with python
---------------------------------

Commands are named registered adapters against IRequest interfaces

   >>> class DummyRequest(object):
   ... 	   zope.interface.implements(bit.core.interfaces.IRequest)
   ...
   ...	   def speak(self, msg):
   ...	       print msg
   
   >>> request = DummyRequest()
   >>> commands = zope.component.getAdapter(request, bit.core.interfaces.ICommand)
   >>> commands
   <bit.core.commands.Commands ...>

Commands are asynchronous, they also may respond using the IRequest.speak interface before the command has completed

Adapters registered without a name provide helpful info about available commands

   >>> def print_help(resp):
   ... 	   if not resp == u'list of commands:\nhelp':
   ... 	      print 'ERROR: no list of commands!'

   >>> def help(resp):
   ...     return commands.load(None, 'help').addCallback(print_help)

   >>> d.addCallback(help)
   <DeferredList at ...>	   
 
   >>> d.addCallbacks(lambda x: twisted.internet.reactor.stop())
   <DeferredList ...>

   >>> twisted.internet.reactor.run()
