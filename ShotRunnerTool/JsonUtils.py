import json
import os

class JsonUtils(object):
    def __init__(self):
        self.jsonData = {}
        self.jsonPathName = None
        self.jsonFile = None

    def newJsonFile(self, filename):
        self.jsonPathName = filename
        #if the file doesn't exit, create a new file
        if not os.path.exists(filename):
            with open(filename, 'r+') as self.jsonFile:
                #todo: if the file exists open a dialog box asking if the user wants to overwrite it or not
                self.jsonData = {}

    def openJsonFile(self, filename):
        #load a json file into memory (update path and file)
        #grab the file contents and add it into memory
        self.jsonPathName = filename
        #if the file exists open the file
        if os.path.exists(filename):
            with open(filename, 'r+') as self.jsonFile:
                self.jsonData = json.loads(self.jsonFile.read())
            #should not be selectable if the the file doesn't exist. The qt dialog box shouldn't allow you to select a file
            #that doesn't exist.

    def saveJsonFile(self):
        #save the json data to the json file
        if self.jsonFile != None:
            with open(self.jsonPathName, 'r+') as self.jsonFile:
                self.jsonFile.write(json.dumps(self.jsonData))

    def saveJsonFileAs(self, filename):
        #save the data to another json file
        with open(filename, 'w') as self.jsonFile:
            self.jsonFile.write(json.dumps(self.jsonData))

def main():
    test = JsonTester()
    test.openJsonFile('test.json')
    print test.jsonData
    test.jsonData['cruux'] = 'garply'
    test.saveJsonFile()
    test.saveJsonFileAs('test_save_as.json')


if __name__ == '__main__':
    main()