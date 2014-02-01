import json
import os

class JsonUtils(object):

    @staticmethod
    def newJsonFilePath(filename):
        jsonPathName = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as jsonFile:
                return jsonPathName
        raise IOError, "The file %s already exists." %(filename)

    @staticmethod
    def newJsonFile(filename):
        jsonPathName = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as jsonFile:
                return jsonFile
        raise IOError, "The file %s already exists." %(filename)

    @staticmethod
    def getDataFromJsonFile(filename):
        jsonPathName = filename
        if os.path.exists(filename):
            with open(filename, 'r') as jsonFile:
                jsonData = json.loads(jsonFile.read())
                return jsonData
        raise IOError, "Couldn't import data from the file"

    @staticmethod
    def saveJsonFileByPath(jsonPathName, jsonData):
            with open(jsonPathName, 'w') as jsonFile:
                jsonFile.write(json.dumps(jsonData))

    @staticmethod
    def saveJsonFile(jsonFile, jsonData):
        jsonFile.write(json.dumps(jsonData))

def main():
    jsonDict = {'foo': 'bar'}
    JsonUtils.saveJsonFileByPath('testStuff.json', jsonDict)
    print JsonUtils.getDataFromJsonFile('testStuff.json')


if __name__ == '__main__':
    main()