from twisted.manhole import telnet



def getTestPort():
    return 23232



def getTestFactory():
    return telnet.ShellFactory()
