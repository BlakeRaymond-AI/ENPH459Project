__author__ = 'Blake'


class DeviceImporter:
    def __init__(self, targetH5File):
        self.targetH5File = targetH5File

    def importFromDict(self, newDevices):
        for deviceName, device in newDevices.items():
            deviceGroup = self.targetH5File.create_group(deviceName)
            for key, value in device.items():
                deviceGroup[key] = value

    def importFromH5File(self, sourceH5File):
        for deviceName, device in sourceH5File.items():
            if not deviceName in self.targetH5File:
                sourceH5File.copy(device, self.targetH5File)
