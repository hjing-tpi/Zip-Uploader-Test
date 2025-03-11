# Process Product Input Data sent to TPass, either by Scanner, File Drop, Serial etc.
# This Script is expected to call RunTestCycle() passing in the appropriate parameters and setting the out parameters below
#
# TPass Objects Passed In and expected Returned
#   in  - string "StartCycleInputData" - This is the data that triggered this script by either a bar code scan, file drop, etc...
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application Detail log file
#   in  - object "SystemConfigurationValue" - This is the object to get values set in the System Configuration file
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

import clr
version = "1.0"
production = False

#########################################################################################################################################
# Application Engineer:  Specific constant variables to maintain
#
testApplicationScriptFileName = "Dakkota_WD_IP_01.json"
optionCodeFileName = "WD_WL_Options.json"
#
#########################################################################################################################################
TPassLogger.Debug("Start Test Cycle Script:  Product Input Data = {0}", StartCycleInputData)

try:

    TPassLogger.Debug("Start Test Cycle Script: Request and processing build data, run a Test Application and process the results")

    # If required to parse the StartCycleInputData differently based on what input type triggered the script to run (Scan, Manual Entry, File Drop...)
    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Scan):
        TPassLogger.Debug("StartTestCycle - Trigger Type is Scan")
        StartCycleInputData = StartCycleInputData[4:]
    elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ManualEntry):
        TPassLogger.Debug("StartTestCycle - Trigger Type is ManualEntry")
    elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.FileDrop):
        TPassLogger.Debug("StartTestCycle - Trigger Type is FileDrop")
    elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Udp):
        TPassLogger.Debug("StartTestCycle - Trigger Type is UDP")

    # If required, parse the StartCycleInputData and pass in to the RunTestCycle() method.  This data will be used by the Request Script for build data retrieval
    runTestCycleId = StartCycleInputData

    # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true, bool useCurrentProductIdentification = false)
    if MainTPassScripting.RunTestCycle(testApplicationScriptFileName, optionCodeFileName, runTestCycleId):
        isSuccess = True
    else:
        isSuccess = False
        TPassLogger.Warn("Start Test Cycle Script:  Error Running Test Cycle")

except Exception as inst:
    TPassLogger.Warn("Start Test Cycle Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Start Test Cycle Script:  Processing Failed.")
    isSuccess = False

TPassLogger.Info("Start Test Cycle Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 05022022
#   Version: 2.0
#   ChangeBy: RMM
#   Change: If Scanned, stript first 4 characters (CSN,)
#   Date: 10052021
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################
