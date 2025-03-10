#Main Button Triggered Script
#This Script can run any python logic and can also run a TPass Test Application
#TPass Objects Passed In/Returned
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

#########################################################################################################################################
# Application Engineer:  Specific constant variables to maintain
#
testApplicationScriptFileName = "IAC Arlington Left Front Door 01.json"
optionCodeFileName = "Options.json"
#
#########################################################################################################################################

TPassLogger.Debug("Retest Button Script Begin")

try:
    TPassLogger.Info("Retest Button Script: Run a Retest")
    # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true, bool useCurrentProductIdentification = false, bool bypassOverrideTestAppScript = false)
    if MainTPassScripting.RunTestCycle(testApplicationScriptFileName, optionCodeFileName, "", False, True, True, False):
        isSuccess = True
    else:
        isSuccess = False
        TPassLogger.Warn("Retest Button Script:  Error Running Test Cycle")

except Exception as inst:
    TPassLogger.Warn("Retest Button Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Retest Button Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Retest Button Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 07182022
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################

