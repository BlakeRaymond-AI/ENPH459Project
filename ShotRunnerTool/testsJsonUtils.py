__author__ = 'Jeff'

import unittest
import os

import JsonUtils


class testJsonUtils(unittest.TestCase):

    def setUp(self):
        data = {'test': 'things'}
        JsonUtils.JsonUtils.saveJsonFileByPath('test_JsonUtils.json', data)

    def tearDown(self):
        os.remove('test_JsonUtils.json')

    def test_saveToFileByName(self):
        data = {'test': 'things'}
        JsonUtils.JsonUtils.saveJsonFileByPath('test_saveJsonFile.json', data)
        fileCreated = os.path.exists('test_saveJsonFile.json')
        self.assertTrue(fileCreated)
        os.remove('test_saveJsonFile.json')

    def test_loadFromFileByName(self):
        data = JsonUtils.JsonUtils.getDataFromJsonFile('test_JsonUtils.json')
        key = data.keys()[0]
        value = data[key]
        self.assertEqual(key, 'test')
        self.assertEqual(value, 'things')
