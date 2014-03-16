import unittest

from FluentDictionary import FluentDictionary


__author__ = 'Blake'


class TestFluentDictionary(unittest.TestCase):
    def test_DictionaryItemsConvertedToAttributes(self):
        fluentDict = FluentDictionary({'Foo': 'Bar'})
        self.assertEqual('Bar', fluentDict.Foo)

    def test_RecursivelyAddsFluentDictionaries(self):
        nestedDict = {'Foo': 'Bar'}
        parentDict = {'Baz': nestedDict}
        fluentDict = FluentDictionary(parentDict)
        self.assertEqual('Bar', fluentDict.Baz.Foo)
