import imp
import h5py

SETTINGS_TEMPLATE = 'settingsTemplate.py'
PATH_DIRECTORY = 'C:\Users\School\GIT\ENPH459Project\TestFolder\settingsTemplate.py'
OUTPUT_FILE_NAME = 'default_settings.h5'

settingsTemplate = imp.load_source(SETTINGS_TEMPLATE, PATH_DIRECTORY)
h5file = h5py.File(OUTPUT_FILE_NAME,'w')
deviceNames = filter(lambda x: type(getattr(settingsTemplate,x)) == dict and x != '__builtins__', dir(settingsTemplate))
deviceGroup = h5file.create_group('devices')
for deviceString in deviceNames:
    device = getattr(settingsTemplate, deviceString)
    h5device = deviceGroup.create_group(deviceString)
    for key in device.keys():
        try:
            h5device[key] = device[key]
            h5device[key].attrs['source_expression'] = str(device[key])
        except:
            h5file.close()
            raise Exception, "Error importing data for device %s, data %s" %(deviceString, key)

h5file.close()

