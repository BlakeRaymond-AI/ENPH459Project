import os
import imp
import os.path
import h5py
from ShotPreparationTool.DeviceImporter import DeviceImporter
from ShotPreparationTool import GroupTableModel
from ShotPreparationTool import VariableNameValidator


DEVICES_GROUP_NAME = 'devices'
SETTINGS_FILE_DIRECTORY = 'C:\\Users\\School\\GIT\\PAT\\PATFramework\\Client\\Settings\\DefaultSettings'


FILE_TO_DEVICE_NAMES_MAP = {'LabJackSettings': 'LabJack',
           'MKS_SRG3_Settings': 'MKS_SRG3',
           'Stabil_Ion_Settings': 'Stabil_Ion',
           'PixeLinkSettings': 'PixeLink',
           'OptimizerSettings': 'Optimizer',
           'PMDSettings': 'PMD'}  # all default devices from currently in the lab


class ShotPrepToolModel(object):
    def __init__(self, h5pathName):
        self.h5pathName = h5pathName
        self.dict_of_devices = {}
        if os.path.exists(self.h5pathName):
            self.originalFile = h5py.File(self.h5pathName)
        else:
            self.originalFile = h5py.File(self.h5pathName)
            self.originalFile.create_group(DEVICES_GROUP_NAME)
            self.originalFile.flush()

        self.h5tempFileName = h5pathName + '.tmp'
        self.workingFile = h5py.File(self.h5tempFileName, driver='core', backing_store=False)  # memory-only
        self.originalFile.copy(DEVICES_GROUP_NAME, self.workingFile)
        self.__buildModelsInFile()

    def cleanUp(self):
        self.originalFile.close()
        self.workingFile.close()

    def __buildModelsInFile(self):
        self.dict_of_devices = {}
        for deviceName, device in self.workingFile[DEVICES_GROUP_NAME].items():
            model = GroupTableModel.GroupTableModel(device, parent=None)
            self.dict_of_devices[deviceName] = model

    def returnModelsInFile(self):
        return self.dict_of_devices

    def discardCharges(self):
        del self.workingFile[DEVICES_GROUP_NAME]
        self.originalFile.copy(DEVICES_GROUP_NAME, self.workingFile)
        self.__buildModelsInFile()

    def saveChanges(self):
        del self.originalFile[DEVICES_GROUP_NAME]
        self.workingFile.copy(DEVICES_GROUP_NAME, self.originalFile)
        for device in self.originalFile[DEVICES_GROUP_NAME].values():
            if GroupTableModel.EMPTY_ROW_STRING in device:
                del device[GroupTableModel.EMPTY_ROW_STRING]
        self.originalFile.flush()

    def removeDevice(self, deviceName):
        del self.workingFile[DEVICES_GROUP_NAME][deviceName]
        self.__buildModelsInFile()

    def addDevice(self, deviceName):
        if deviceName in self.workingFile[DEVICES_GROUP_NAME]:
            raise KeyError('Device with name \"%s\" already exists.' % deviceName)
        if not VariableNameValidator.isValidVariableName(deviceName):
            raise SyntaxError('Device name \"%s\" is not a valid Python variable name.' % deviceName)
        self.workingFile[DEVICES_GROUP_NAME].create_group(deviceName)
        self.__buildModelsInFile()

    @staticmethod
    def getListOfDevices(h5File):
        if not DEVICES_GROUP_NAME in h5File:
            return []
        devicesGroup = h5File[DEVICES_GROUP_NAME]
        return devicesGroup.keys()

    def importDevices(self, devices, h5file):
        devicesGroup = h5file[DEVICES_GROUP_NAME]
        importer = DeviceImporter(self.workingFile[DEVICES_GROUP_NAME])
        importer.importFromH5File(devicesGroup, devices)
        self.__buildModelsInFile()

    def importFromDefaults(self, directoryPath=SETTINGS_FILE_DIRECTORY):
        for f in os.listdir(directoryPath):
            if f.endswith('.py'):
                module = imp.load_source(f, os.path.join(directoryPath, f))
                settingsFile = [f for f in module.__dict__.keys() if f in FILE_TO_DEVICE_NAMES_MAP.keys()]
                for device in settingsFile:
                    newDevice = self.workingFile[DEVICES_GROUP_NAME].create_group(FILE_TO_DEVICE_NAMES_MAP[device])
                    for name in getattr(module, device).keys():
                        newDevice[name] = getattr(module, device)[name]
        self.__buildModelsInFile()



    def saveAs(self, filename):
        newFile = h5py.File(filename)
        self.workingFile.copy(DEVICES_GROUP_NAME, newFile)
