import imp
import h5py

SETTINGS_TEMPLATE = 'settingsTemplate.py'
PATH_DIRECTORY = 'C:\PAT\PATFramework\Client\Settings\settingsTemplate.py'
OUTPUT_FILE_NAME = 'default_settings.h5'

settingsTemplate = imp.load_source(SETTINGS_TEMPLATE, PATH_DIRECTORY)
updatePackage = settingsTemplate.updatePackage
h5file = h5py.File(OUTPUT_FILE_NAME,'w')
deviceGroup = h5file.create_group('devices')
for device in settingsTemplate.updatePackage:
    newDevice = deviceGroup.create_group(device)
    for setting in updatePackage[device]:
        newDevice[setting] = updatePackage[device][setting]
        newDevice[setting].attrs['source_expression'] = str(updatePackage[device][setting])

h5file.close()

