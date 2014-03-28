'''
Default settings for PMD. Consult PMD API Specification for voltage range
and trigger specifications. Device model is PMD-1208FS (USB-1208FS in manual). 
'''

PMDSettings = dict()
PMDSettings['activeChannels'] = [0]	# Channels to sample.
PMDSettings['gainSettings'] = [0]	#This is no longer used !!!!  # Gain to use on each channel. Should have same
									# size as activeChannels array.
PMDSettings['sampleRatePerChannel'] = 200	# Samples per channel per second. Aggregate
											# rate should not exceed 40000.
PMDSettings['scanDuration'] = 5	# Seconds
#PMDSettings['vRange'] = 'BIP10VOLTS'	# Voltage range being measured.
PMDSettings['trigger'] = True
PMDSettings['trigType'] = 'TRIG_POS_EDGE'	# Trigger type to use
PMDSettings['boardNum'] = 0

PMDSettings['takeData'] = False
PMDSettings['processData'] = False
PMDSettings['dataFolderName'] = "PMDData"
 
PrismaPlusSettings = dict()

PrismaPlusSettings['persistent'] = False
PrismaPlusSettings['takeData'] = True
PrismaPlusSettings['processData'] = True
PrismaPlusSettings['dataFolderName'] = "RGAData"

PrismaPlusSettings['scanDuration'] = 120

updatePackage = {
	'PMD' : PMDSettings,
        'RGA' : PrismaPlusSettings,
	}
