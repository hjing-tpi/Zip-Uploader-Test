#Main Button Triggered Script
#This Script can run any python logic and can also run a TPass Test Application
#TPass Objects Passed In/Returned
#   in  - object MainTPassScripting - Exposed all methods and properties for the scripts to use
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
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
testApplicationScriptFileName = "HBPO_RU-LB_FEM.json"
optionCodeFileName = "Options.json"
#
#########################################################################################################################################

#TPassLogger.Debug("Start Test Cycle Script:  Product Input Data = {0}", StartCycleInputData)
try:

    TPassLogger.Debug("HBPO Retest: Retest Main Button Pressed")

    # If required, parse the StartCycleInputData and pass in to the RunTestCycle() method.  This data will be used by the Request Script for build data retrieval
    runTestCycleId = ""

    # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true, bool useCurrentProductIdentification = true)
    if MainTPassScripting.RunTestCycle(testApplicationScriptFileName, optionCodeFileName, runTestCycleId, False, True, True):
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
#   Date: 07112023
#   Version: 1.0
#   ChangeBy: LM
#   Change: Initial Version
############################################################
