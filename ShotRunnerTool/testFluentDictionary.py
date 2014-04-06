import unittest
from ShotRunnerTool.FluentDictionary import FluentDictionary


class TestFluentDictionary(unittest.TestCase):
    def test_DictionaryItemsConvertedToAttributes(self):
        fluentDict = FluentDictionary({'Foo': 'Bar'})
        Foo = getattr(fluentDict, 'Foo')
        self.assertEqual('Bar', Foo)

    def test_RecursivelyAddsFluentDictionaries(self):
        nestedDict = {'Foo': 'Bar'}
        parentDict = {'Baz': nestedDict}
        fluentDict = FluentDictionary(parentDict)
        Baz = getattr(fluentDict, 'Baz')
        Foo = getattr(Baz, 'Foo')
        self.assertEqual('Bar', Foo)
