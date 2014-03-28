from PMDTestSettings import updatePackage
from PATController import PATController, defaultSettings, overwriteSettings
from time import sleep

# Test of PMD Recording capabilities whilst utilizing hardware trigger.
updatedSettings = overwriteSettings(defaultSettings, updatePackage)

PATCtrl = PATController('PMD_Recorder', updatedSettings)
PATCtrl.start()
PATCtrl.triggerPMD()	# Triggers the PMD

PATCtrl.startDevices()
PATCtrl.end()
dataCollectionFailed = PATCtrl.stopDevices()

if dataCollectionFailed:
    print "!!!!! DATA COLLECTION FAILED !!!!!"
else:
    PATCtrl.save()
    PATCtrl.processData()

PATCtrl.closeClient()

