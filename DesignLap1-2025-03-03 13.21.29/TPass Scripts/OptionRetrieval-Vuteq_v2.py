#Retrieve Build Data for Product Id
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - string "RunTestCycleId" - This is the data that was passed from the Start Test Cycle script via the RunTestCycle method.
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application Detail log file
#   in  - object "SystemConfigurationValue" - This is the object to get values set in the System Configuration file
#   out - string "productBuildData" - Build data retrieved to be processed by the Option Parsing script
#   out - bool "isSuccess" - Set to True if build data retrieval was successful.  Otherwise False
#   out - bool "production"
#   out - string "version"
#

from System.IO import File
from System import DateTime

version = "2.0"
production = False
productBuildData = ""
isSuccess = False


#########################################################################################################################################
# Application Engineer:  Specific constant variables to maintain
#
#
#########################################################################################################################################


# Main Logic
try:

    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ManualEntry):
        TPassLogger.Info("StartTestCycle - Trigger Type is ManualEntry no Retrieval is necessary")
        productBuildData = RunTestCycleId
        isSuccess = False
    else:
        TPassLogger.Info("Option Retrieval Script:  Data is received via Barcode scan so no Retrieval is necessary")
        productBuildData = RunTestCycleId
        isSuccess = True

except Exception as inst:
    TPassLogger.Warn("Option Retrieval Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Retrieval Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Retrieval Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 02172023
#   Version: 2.0
#   Change: Changed to allow for manual entry of part number
#   Date: 08192022
#   Version: 1.0
#   Change: Initial Version
############################################################
