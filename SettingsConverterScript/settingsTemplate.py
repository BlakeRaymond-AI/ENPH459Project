#'''Default settings for LabJack'''
LabJackSettings = dict()
LabJackSettings['activeChannels'] = [0]	# Array of size 1, 2 or 4 (# Valid Channels: 0-7)				
LabJackSettings['sampleRatePerChannel'] = 200 # Samples per channel per second. Aggregate rate should be between 200 and 1200.
LabJackSettings['scanDuration'] = 10	# Seconds
LabJackSettings['trigger'] = False		# Use trigger.
LabJackSettings['triggerChannel'] = 0	# Channel to use as trigger input.

LabJackSettings['takeData'] = False
LabJackSettings['processData'] = False
LabJackSettings['persistent'] = False
LabJackSettings['dataFolderName'] = "LabJackData"



# ----------------------------------- 
#'''
#Default settings for MKG SRG3. Consult device controller for 
#more information on gas type, pressure and temperature codes.
#'''
#
MKS_SRG3_Settings = dict()
MKS_SRG3_Settings['port'] = 2	# The COMx port the gauge is connected to.
MKS_SRG3_Settings['duration_s'] = 60	# Total data collection time.
MKS_SRG3_Settings['measurementTime_s'] = 20  # Time over which a single measurement will be made.							
MKS_SRG3_Settings['gType'] = 9	# Gas Type (Default: Air)
MKS_SRG3_Settings['pUnits'] = 3 # Pressure Units (Default: Torr)
MKS_SRG3_Settings['tUnits'] = 1 # Temperature Units (Default: Celsius)			

MKS_SRG3_Settings['takeData'] = False
MKS_SRG3_Settings['processData'] = False
MKS_SRG3_Settings['persistent'] = False
MKS_SRG3_Settings['dataFolderName'] = "MKS_SRG3_Data"

# ----------------------------------- 
#'''Default Optimizer Settings'''
OptimizerSettings = dict()
OptimizerSettings['fitnessEvalScript'] = 'C:\PAT\PATScripts\Optimizations\ScriptNameHere.py'
OptimizerSettings['numOfParticles'] = 0		# Number of particles in a generation.
OptimizerSettings['numOfGenerations'] = 0	# Number of generations.
OptimizerSettings['phiG'] = 1	# Velocity weight towards best global particle.
OptimizerSettings['phiP'] = 1	# Velocity weight towards best local particle.
OptimizerSettings['w'] = 1		# Velocity damping factor.
OptimizerSettings['alpha'] = 1 # Limits the max speed of a particle in any of it's dimensions to alpha * (upperBound - lowerBound)
OptimizerSettings['minimization'] = False	# Toggles minimization or maximization. 

#paramBounds is an n-tuple of 2-tuples representing the lower and upper bounds of paramaters.
paramBounds = (
	# (lowerBound1, upperBound1),
	# (lowerBound2, upperBound2),
	# ...
)
OptimizerSettings['paramBounds'] = paramBounds

OptimizerSettings['takeData'] = False	# Won't actually take data, but will enable optimizer.
OptimizerSettings['dataFolderName'] = "OptimizerData"
OptimizerSettings['persistent'] = True
# ----------------------------------- 
PATClientSettings = dict()
PATClientSettings['HOST'] = '10.1.137.1'
PATClientSettings['PORT'] = 15964

# ----------------------------------- 
PATSettings = dict()
#
## Coil current in Amperes
PATSettings['2D_I_1'] = 4.0445672330089026
PATSettings['2D_I_2'] = 4.8677651953079595
PATSettings['2D_I_3'] = -4.9063663215800446
PATSettings['2D_I_4'] = 4.2235519337272178
PATSettings['3D_coils_I'] = 1.1630532494522459
## Pump detuning in MHz
PATSettings['2DRb_pump_detuning'] = 12.014217918080053
PATSettings['3DRb_pump_detuning'] = 11.181703291771417
PATSettings['Rb_repump_detuning'] = 4.4578685047937929
PATSettings['Rb_push_detuning'] = 10.577814782792434
#
## Pump amplitude in ...
PATSettings['2DRb_pump_amplitude'] = 0.81403689617537489
PATSettings['3DRb_pump_amplitude'] = 0.9734310799923549     
PATSettings['Rb_repump_amplitude'] = 0.74128861551863034   
PATSettings['Rb_push_amplitude'] = 0.41064188475343033 


# ----------------------------------- 
#'''Default settings for PixeLink Camera'''
PixeLinkSettings = dict()
PixeLinkSettings['gain'] = 0 	# Image Gain. Possible values: 0, 1.5, 3.1, 4.6	
PixeLinkSettings['expTime_ms'] = 10.0 	# Image Exposure Time
PixeLinkSettings['ROI_width'] = 1280	
PixeLinkSettings['ROI_height'] = 1024
PixeLinkSettings['ROI_left'] = 0
PixeLinkSettings['ROI_top'] = 0
PixeLinkSettings['useROICenter'] = False	# Set region of interest based on center location and width and height settings.
PixeLinkSettings['ROI_center'] = (640, 512) # Location of center. (x, y)

PixeLinkSettings['takeData'] = False
PixeLinkSettings['processData'] = False
PixeLinkSettings['persistent'] = False
PixeLinkSettings['dataFolderName'] = "PixeLinkData"

# ----------------------------------- 
#'''
#Default settings for PMD. Consult PMD API Specification for voltage range
#and trigger specifications. Device model is PMD-1208FS (USB-1208FS in manual). 
#'''
PMDSettings = dict()
PMDSettings['activeChannels'] = [0]	# Channels to sample.
PMDSettings['gainSettings'] = [0]	# Gain to use on each channel. Should have same size as activeChannels array.
PMDSettings['sampleRatePerChannel'] = 200	# Samples per channel per second, aggregate rate should not exceed 50000.
PMDSettings['scanDuration'] = 10	# Seconds
PMDSettings['vRange'] = 'BIP10VOLTS'	# Voltage range being measured.
PMDSettings['trigger'] = False			# Use trigger.
PMDSettings['trigType'] = 'TRIG_POS_EDGE'	# Trigger type to use
PMDSettings['boardNum'] = 0

PMDSettings['takeData'] = False
PMDSettings['processData'] = False
PMDSettings['persistent'] = False
PMDSettings['dataFolderName'] = "PMDData"

# ----------------------------------- 
#'''Default settings for Stabil Ion Gauge'''
Stabil_Ion_Settings = dict()
Stabil_Ion_Settings['port'] = 3	# The COMx port the gauge is connected to.			
Stabil_Ion_Settings['duration_s'] = 10 # Duration of data collection.
Stabil_Ion_Settings['secondsPerSample'] = 1	# Max of 1 second per sample.

Stabil_Ion_Settings['takeData'] = False
Stabil_Ion_Settings['processData'] = False
Stabil_Ion_Settings['persistent'] = False
Stabil_Ion_Settings['dataFolderName'] = "Stabil_Ion_Data"

# ----------------------------------- 

#updatePackage = { 
#'LabJack'' :	,
#'MKS_SRG3'' :	,
#'Optimizer'' :	,
#'PixeLink'' :	,
#'PMD'' :	,
#'Stabil_Ion'' :	,
#}
