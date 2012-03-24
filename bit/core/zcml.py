import zope
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('bit.core')

import bit


class IServiceDirective(zope.interface.Interface):
    """
    Define a service
    """

    name = zope.schema.TextLine(
        title=_("Name"),
        description=_("The service name"),
        required=True,
        )

    parent = zope.schema.TextLine(
        title=_("Name"),
        description=_("The service parent"),
        required=True,
        )

    service = zope.configuration.fields.GlobalObject(
        title=_("Service"),
        description=_("The service"),
        required=True,
        )

    port = zope.configuration.fields.GlobalObject(
        title=_("Port"),
        description=_("The service port"),
        required=True,
        )

    factory = zope.configuration.fields.GlobalObject(
        title=_("Service factory"),
        description=_("The service factory"),
        required=True,
        )

    context = zope.configuration.fields.GlobalObject(
        title=_("Service context"),
        description=_("The service context"),
        required=False,
        )


def service(_context, parent, name, service, port, factory, context=None):
    services = zope.component.getUtility(bit.core.interfaces.IServices)
    _services = {}

    if context:
        _services[name] = service(port(), factory(), context())
    else:
        _services[name] = service(port(), factory())
    _context.action(
        discriminator=None,
        callable=services.add,
        args=(parent, _services)
        )


class ICommandDirective(zope.interface.Interface):
    """
    Define a command
    """

    name = zope.schema.TextLine(
        title=_("Name"),
        description=_("The command name"),
        required=True,
        )

    factory = zope.configuration.fields.GlobalObject(
        title=_("Command factory"),
        description=_("The command factory"),
        required=True,
        )

    for_ = zope.configuration.fields.GlobalInterface(
        title=_("Command request interface"),
        description=_("The request interface that I provide commands for"),
        required=False,
        )


def command(_context, name, factory, for_=bit.core.interfaces.IRequest):
    _context.action(
        discriminator=None,
        callable=zope.component.provideAdapter,
        args=(factory, [for_], bit.core.interfaces.ICommand, name),
        )
