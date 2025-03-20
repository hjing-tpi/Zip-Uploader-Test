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

TPassLogger.Debug("Main Button Script Begin")

try:
        TPassLogger.Info("Main Button Script: Run a Quick Test Application with default options only and don't process results")
        input = "123456"
        if input != "":
            # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true)
            if MainTPassScripting.RunTestCycle("adient.json", "WD_WL_Options.json", input, True, True):
                isSuccess = True
            else:
                isSuccess = False
                TPassLogger.Warn("Main Button Script:  Error Running Quick Test Cycle")
        else:
            isSuccess = True
            TPassLogger.Info("GetInputKeyPad() No Job Entered by Operator")

except Exception as inst:
    TPassLogger.Warn("Main Button Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Main Button Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Main Button Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 01172021
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
# 
#  Date: 05122022
#   Version: 1.0
#   ChangeBy: GS
#   Change: Change option code
############################################################

