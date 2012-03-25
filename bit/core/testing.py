import zope

import twisted

import bit


def getTestPort():
    return 23232


def getTestPort2():
    return 23233


class TestCommand2(object):
    """ This is another example of a command object """
    zope.interface.implements(bit.core.interfaces.ICommand)

    def __init__(self, request):
        self.request = request
    
    def load(self, session, args):
        return twisted.internet.defer.maybeDeferred(lambda: 'another test complete!')
