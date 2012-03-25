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
            if len(args.strip().split(' ')) > 1:
                command_name = args.strip().split(' ')[1]
                command = queryAdapter(self.request, ICommand, command_name)
                if command:
                    self.request.speak("%s:" % command_name)
                    self.request.speak(
                        command.__doc__ or '...is currently undocumented')
                else:
                    self.request.speak(
                        'unrecognized command: %s' % command_name)
                    self.request.speak(
                        'type > or >help for a list of commands')
                return

            _commands = ['list of commands:']
            commands = getAdapters((self.request, ), ICommand)
            for command, adapter in commands:
                if not command:
                    continue
                _commands.append(command)
            return '\n'.join(_commands)

        return defer.maybeDeferred(_commands)
