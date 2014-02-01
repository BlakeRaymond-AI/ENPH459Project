import json
import os

class JsonUtils(object):

    @staticmethod
    def newJsonFilePath(self, filename):
        self.jsonPathName = filename
        #if the file doesn't exit, create a new file
        if not os.path.exists(filename):
            with open(filename, 'w') as self.jsonFile:
                #todo: if the file exists open a dialog box asking if the user wants to overwrite it or not
                self.jsonData = {}
                return self.jsonPathName
        raise IOError, "The file %s already exists." %(filename)

    @staticmethod
    def newJsonFile(self, filename):
        self.jsonPathName = filename
        #if the file doesn't exit, create a new file
        if not os.path.exists(filename):
            with open(filename, 'w') as self.jsonFile:
                #todo: if the file exists open a dialog box asking if the user wants to overwrite it or not
                self.jsonData = {}
                return self.jsonFile
        raise IOError, "The file %s already exists." %(filename)

    @staticmethod
    def getDataFromJsonFile(self, filename):
        #load a json file into memory (update path and file)
        #grab the file contents and add it into memory
        self.jsonPathName = filename
        #if the file exists open the file
        if os.path.exists(filename):
            with open(filename, 'r') as self.jsonFile:
                self.jsonData = json.loads(self.jsonFile.read())
                return self.jsonData
        raise IOError, "Couldn't import data from the file"

    @staticmethod
    def saveJsonFile(self):
        #save the json data to the json file
        if self.jsonFile != None:
            with open(self.jsonPathName, 'w') as self.jsonFile:
                self.jsonFile.write(json.dumps(self.jsonData))

    @staticmethod
    def saveJsonFileAs(self, filename):
        #save the data to another json file
        with open(filename, 'w') as self.jsonFile:
            self.jsonFile.write(json.dumps(self.jsonData))

def main():
    test = JsonUtils()
    test.openJsonFile('test.json')
    print test.jsonData
    test.jsonData['cruux'] = 'garply'
    test.saveJsonFile()
    test.saveJsonFileAs('test_save_as.json')


if __name__ == '__main__':
    main()