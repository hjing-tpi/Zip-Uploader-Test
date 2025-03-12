# Process Product Input Data sent to TPass, either by Keyboard, Scanner, File Drop, Serial etc.
# This Script is expected to call RunTestCycle() passing in the appropriate parameters
#
# TPass Objects Passed In and expected Returned
#   in  - string StartCycleInputData - This is the data that triggered this script by either manual entry, a bar code scan, file drop, etc...
#   in  - object MainTPassScripting - Exposed all methods and properties for the scripts to use
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

import clr
version = "1.0"
production = False

TPassLogger.Debug("Start Test Cycle Script:  Product Input Data = {0}", StartCycleInputData)

try:

    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Scan):
        TPassLogger.Debug("StartTestCycle - Trigger Type is Scan")
    elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ContinuousMode):
        TPassLogger.Debug("StartTestCycle - Trigger Type is ContinuousMode")

    TPassLogger.Debug("Start Test Cycle Script: Request and processing build data, run a Test Application and process the results")
    #MainTPassScripting.InterfaceUiLogger("MES", "Start Test Cycle Script", True, True)

    # If required parse the StartCycleInputData and pass in to the RunTestCycle() method.  This data will be used by the Request Script Data for build data retrieval
    runTestCycleId = StartCycleInputData

    # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true)
    if MainTPassScripting.RunTestCycle("2020TeslaRoadster-GlassRoof.json", "OptionCodes-Tesla.json", runTestCycleId, False, True):
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
#   Date: 01172021
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################
