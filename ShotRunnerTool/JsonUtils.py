import json
import os

class JsonUtils(object):
    @staticmethod
    def getDataFromJsonFile(filename):
        if os.path.exists(filename):
            with open(filename, 'r') as jsonFile:
                jsonData = json.loads(jsonFile.read())
                return jsonData
        raise IOError, "Couldn't import data from the file '%s'" %(filename)

    @staticmethod
    def saveJsonFileByPath(jsonPathName, jsonData):
            with open(jsonPathName, 'w') as jsonFile:
                jsonFile.write(json.dumps(jsonData))


def main():
    JsonUtils.getDataFromJsonFile('test io error.json')

if __name__ == '__main__':
    main()