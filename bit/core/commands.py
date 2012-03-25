from zope.component import getAdapters, queryAdapter

from twisted.python import log
from twisted.internet import defer

from bit.core.interfaces import ICommand


class Commands(object):

    def __init__(self, request):
        self.request = request

    def load(self, sessionid, args):
        log.msg('bit.bot.xmpp.commands: Commands.load: ',
                sessionid)
        def _commands():
            log.msg('bit.bot.http.request: Commands.load._commands: ',
                    sessionid)
            response = []
            if len(args.strip().split(' ')) > 1:
                command_name = args.strip().split(' ')[1]
                command = queryAdapter(self.request, ICommand, command_name)
                if command:
                    response.append( "%s:" % command_name)
                    response.append(command.__doc__ or '...is currently undocumented')
                else:
                    response.append('unrecognized command: %s' % command_name)
                    response.append('type > or >help for a list of commands')
            else:
                response.append('list of commands:')
                commands = getAdapters((self.request, ), ICommand)
                for command, adapter in commands:
                    if not command:
                        continue
                    response.append(command)
            return '\n'.join(response)

        return defer.maybeDeferred(_commands)
