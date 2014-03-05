__author__ = 'Jeff'

import unittest
import JsonUtils
import os

class testJsonUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_saveToFileByName(self):
        data = {'test' : 'things'}
        JsonUtils.JsonUtils.saveJsonFileByPath('test_JsonUtils.json', data)
        fileCreated = os.path.exists('test_JsonUtils.json')
        self.assertTrue(fileCreated)

    def test_loadFromFileByName(self):
        data = JsonUtils.JsonUtils.getDataFromJsonFile('test_JsonUtils.json')
        key = data.keys()[0]
        value = data[key]
        self.assertEqual(key, 'test')
        self.assertEqual(value, 'things')

