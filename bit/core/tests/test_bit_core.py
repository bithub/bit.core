
from cStringIO import StringIO
import doctest

from zope.component import getUtility
from zope.configuration.xmlconfig import xmlconfig

from twisted.trial import unittest, runner
from twisted.test import proto_helpers
from twisted.internet import reactor

from bit.core.interfaces import IApplication, IServices, IApplicationRunner
from bit.core.configuration import Configuration, StringConfiguration


test_configuration = """
[bot]
name = testbot
plugins = bit.bot.core
"""


def setUp(self):
    pass

def test_suite():
    ts = runner.TestSuite()
    ts.name = "MyCustomSuite"
    ts.addTest(doctest.DocFileSuite("../README.txt", setUp=setUp,
                                    optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE))
    return ts
