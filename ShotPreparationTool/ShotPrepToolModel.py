import os
import os.path
import shutil

from PyQt4 import QtGui
import h5py
import GroupTableModel

class ShotPrepToolModel(object):
    def __init__(self, h5pathName):
        self.h5pathName = h5pathName
        if os.path.exists(self.h5pathName):
            self.originalFile = h5py.File(self.h5pathName)
        else:
            self.originalFile = h5py.File(self.h5pathName)
            self.originalFile.create_group('devices')

        self.h5tempFileName = h5pathName + '.tmp'
        if os.path.exists(self.h5tempFileName):
            os.remove(self.h5tempFileName)
        shutil.copy2(self.h5pathName, self.h5tempFileName)
        self.workingFile = h5py.File(self.h5tempFileName)
        self.__buildModelsInFile()

    def cleanUp(self):
        self.originalFile.close()
        self.workingFile.close()
        os.remove(self.h5tempFileName)

    def __buildModelsInFile(self):
        self.dict_of_devices = {}
        for device in self.workingFile['devices']:
            model = GroupTableModel.GroupTableModel(self.workingFile['devices'], device, parent=None)
            self.dict_of_devices[device] = model

    def returnModelsInFile(self):
        return self.dict_of_devices

    def discardCharges(self):
        del self.workingFile['devices']
        self.originalFile.copy('devices', self.workingFile)
        self.__buildModelsInFile()

    def saveChanges(self):
        del self.originalFile['devices']
        self.workingFile.copy('devices', self.originalFile)

    def removeDevice(self, deviceName):
        del self.workingFile[deviceName]

    def addDevice(self, deviceName):
        self.workingFile.create_group(deviceName)


if __name__ == '__main__':

    h5pathname = 'devices.h5'
    test = ShotPrepToolModel(h5pathname)
    devices = test.returnModelsInFile()
    print devices['RGA'].h5file['RGA']['test data point'][()]
    devices['RGA'].h5file['RGA']['test data point'][()] = 'this has been changed'
    print devices['RGA'].h5file['RGA']['test data point'][()]

    test.cleanUp()

