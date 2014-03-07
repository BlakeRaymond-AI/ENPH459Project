import os
import os.path
import shutil

import h5py

import GroupTableModel


EMPTY_ROW_KEY = "<Click to add row>"


class ShotPrepToolModel(object):
    def __init__(self, h5pathName):
        self.h5pathName = h5pathName
        if os.path.exists(self.h5pathName):
            self.originalFile = h5py.File(self.h5pathName)
        else:
            self.originalFile = h5py.File(self.h5pathName)
            self.originalFile.create_group('devices')
            self.originalFile.flush()

        self.h5tempFileName = h5pathName + '.tmp'
        if os.path.exists(self.h5tempFileName):
            raise RuntimeError('The file \"%s\" appears to be in use by another instance of the tool.' % h5pathName)
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
            model = GroupTableModel.GroupTableModel(self.workingFile['devices'], device, parent=None,
                                                    empty_row_string=EMPTY_ROW_KEY)
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
        for device in self.originalFile['devices'].values():
            if EMPTY_ROW_KEY in device:
                del device[EMPTY_ROW_KEY]
        self.originalFile.flush()

    def removeDevice(self, deviceName):
        del self.workingFile['devices'][deviceName]
        self.__buildModelsInFile()

    def addDevice(self, deviceName):
        if deviceName in self.workingFile['devices']:
            raise KeyError('Device with name \"%s\" already exists.' % deviceName)
        self.workingFile['devices'].create_group(deviceName)
        self.__buildModelsInFile()

    def saveAs(self, filename):
        self.workingFile.flush()
        shutil.copy2(self.h5tempFileName, filename)


if __name__ == '__main__':

    h5pathname = 'devices.h5'
    test = ShotPrepToolModel(h5pathname)
    devices = test.returnModelsInFile()
    print devices['RGA'].h5file['RGA']['test data point'][()]
    devices['RGA'].h5file['RGA']['test data point'][()] = 'this has been changed'
    print devices['RGA'].h5file['RGA']['test data point'][()]

    test.cleanUp()

