import settingsTemplate
import h5py

"""
create an h5 file
read all elements from the settings template
filter out all non-custom dicts
make a list of all remaining objects in the file
iterate thru the list:
for each device in the list create a dict in the h5 file
fill that dict with the default settings from the read file
"""

h5file = h5py.File('default_name.h5','w')
deviceNames = filter(lambda x: type(getattr(settingsTemplate,x)) == dict and x != '__builtins__', dir(settingsTemplate))

for deviceString in deviceNames:
    device = getattr(settingsTemplate, deviceString)
    h5device = h5file.create_group(deviceString)
    for key in device.keys():
        h5device[key] = device[key]
        
h5file.close()

