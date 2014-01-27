import os
import os.path

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
            self.workingFile = h5py.File(self.h5tempFileName)
        else:
            self.workingFile = h5py.File(self.h5tempFileName)
            self.workingFile.create_group('devices')

        print self.workingFile
        self.workingFile.copy(self.originalFile['Devices'], self.workingFile)

    def cleanUp(self):
        self.originalFile.close()
        self.workingFile.close()

    def returnModelsInFile(self):
        """takes in an path to an h5file. If the file exists construct a model for each device in the h5file, and then
        returns a list with all the models for the devices in the file.
        If the path doesn't exist, create a new h5file with the path name"""
        dict_of_devices = {}

        for device in self.workingFile:
            group_name = device
            model = GroupTableModel.GroupTableModel(self.workingFile, group_name, parent=None)
            dict_of_devices[device] = model
        else:   #the file doesn't exist
            self.create_group('devices')
            group_name = 'devices'
            #model = GroupTableModel.GroupTableModel(h5file, group_name, parent=None)
            #dict_of_devices['no name'] = model
        return dict_of_devices


if __name__ == '__main__':

    #todo: impliemnt a saving and loading feaure
    #todo: impliment a tab view, so that we can check each device in tab (maybe not in this file)
    #done: the ability to open a new window for each device connected.

    app = QtGui.QApplication([])
    h5pathname = 'teststuff.h5'
    test = ShotPrepToolModel(h5pathname)
    devices = test.returnModelsInFile()
    print devices

    for device in devices:
        print device


    '''
    for device in h5file['devices']:
        group_name = 'devices/' + device
        model = GroupTableModel.GroupTableModel(h5file, group_name, parent=None)
        list_of_devices.append(model)
        view = QtGui.QTableView()
        view.setModel(model)
        list_of_views.append(view)
        view.show()
    '''

    app.exec_()
    h5file.close()

