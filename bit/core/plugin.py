
from zope.interface import implements
from zope.component import getUtility, provideAdapter, provideUtility

from bit.bot.common.interfaces import IPlugin, IApplication, INameResolver

from bit.bot.base.plugin import BotPlugin

from bit.name.coins.interfaces import INamecoin
from bit.name.coins.names import Namecoin

class BitNamecoins(BotPlugin):
    implements(IPlugin)
    name = 'bit.name.coins'

    def load_adapters(self):
        provideAdapter(Namecoin,[IApplication,],INamecoin)       

    def load_utils(self):
        app = getUtility(IApplication)
        nmc=INamecoin(app)
        provideUtility(nmc, INamecoin)
        provideUtility(nmc, INameResolver, 'bit')

