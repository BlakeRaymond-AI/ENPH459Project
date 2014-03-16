__author__ = 'Blake'


class DeviceImporter:
    def __init__(self, targetH5File):
        self.targetH5File = targetH5File

    def _shouldIncludeDevice(self, deviceName, devicesToInclude):
        return devicesToInclude is None or deviceName in devicesToInclude

    def importFromDict(self, newDevices, devicesToInclude=None):
        for deviceName, device in newDevices.items():
            if self._shouldIncludeDevice(deviceName, devicesToInclude):
                if deviceName in self.targetH5File:
                    del self.targetH5File[deviceName]
                deviceGroup = self.targetH5File.create_group(deviceName)
                for key, value in device.items():
                    deviceGroup[key] = value

    def importFromH5File(self, sourceH5File, devicesToInclude=None):
        for deviceName, device in sourceH5File.items():
            if self._shouldIncludeDevice(deviceName, devicesToInclude):
                if deviceName in self.targetH5File:
                    del self.targetH5File[deviceName]
                sourceH5File.copy(device, self.targetH5File)
