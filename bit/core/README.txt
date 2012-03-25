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


If the parent is specified, a multi-service will be added

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


using the ICommand interface
----------------------------

Commands are asynchronous, they also may respond using the IRequest.speak interface before the command has completed

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


The help will provide you with a list of commands for the given IRequest object

   >>> HELP = u'list of commands:\nhelp'
   >>> def print_help(resp):
   ... 	   if not resp == HELP:
   ... 	      print 'ERROR: no list of commands!'

   >>> def help(resp):
   ...     return commands.load(None, 'help').addCallback(print_help)

   >>> d.addCallback(help)
   <DeferredList at ...>	   


registering a command in python
-------------------------------

We can provide a commmand explicitly using zope.component.provideAdapter

   >>> class TestCommand(object):
   ... 	     """ This is an example of a command object """
   ...	     
   ... 	     zope.interface.implements(bit.core.interfaces.ICommand)
   ...
   ...	     def __init__(self, request):
   ...	     	 self.request = request
   ...
   ...	     def load(self, session, args):
   ...	     	 return twisted.internet.defer.maybeDeferred(lambda: 'test complete!')

   >>> zope.component.provideAdapter(TestCommand,
   ...				[bit.core.interfaces.IRequest],
   ...				bit.core.interfaces.ICommand,
   ...			  	name='test-command')


The command is now available in the help menu

   >>> def print_help(resp):
   ... 	   if not 'test-command' in resp:
   ... 	      print 'ERROR: test-command missing: %s' %resp

   >>> def help(resp):
   ...     return commands.load(None, 'help')

   >>> _d = d.addCallback(help).addCallback(print_help)


We can also get help for the command, which returns its docstring

   >>> def print_help_test(resp):
   ... 	   if not 'This is an example of a command object' in resp:
   ... 	      print 'ERROR: help did not return the docstring: %s' %resp

   >>> def help_test(resp):
   ...     return commands.load(None, 'help test-command')

   >>> _d = d.addCallback(help_test).addCallback(print_help_test)


We can run the command using commands.load

   >>> def print_test_command(resp):
   ... 	   if not 'test complete!' == resp:
   ... 	      print 'ERROR: help did not return the docstring: %s' %resp

   >>> def test_command(resp):
   ...     return zope.component.getAdapter(
   ...			request, bit.core.interfaces.ICommand,
   ...			'test-command').load(None, '')


   >>> _d = d.addCallback(test_command).addCallback(print_test_command)


registering a command with zcml
-------------------------------

   >>> runSnippet('''
   ... <command
   ...	name="test-command-2"
   ...  factory="bit.core.testing.TestCommand2"
   ...   /> ''')

   >>> def print_test_command_2(resp):
   ... 	   if not 'another test complete!' == resp:
   ... 	      print 'ERROR: command did not return correct response: %s' %resp

   >>> def test_command_2(resp):
   ...     return zope.component.getAdapter(
   ...			request, bit.core.interfaces.ICommand,
   ...			'test-command-2'
   ...			).load(None, '')

   >>> _d = d.addCallback(test_command_2).addCallback(print_test_command_2)

Lets get ready to stop twisted, 8)

   >>> _d = d.addCallbacks(lambda x: None)
   >>> _d = d.addCallbacks(lambda x: twisted.internet.reactor.stop())

And start it!

   >>> twisted.internet.reactor.run()
