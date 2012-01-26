

from zope.interface import Interface as I


class INamecoin(I):
    def get_blockcount():
        """ return the blockcount of the current block """

    def get_name(name):
        """ return value for name """

    def get_dns(name,type='name'):
        """ return dns record for given name """

    def name_scan(first="",count=10):
        """ return $count names starting from $first """


class INamecoinDNS(I):
    pass
