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
from System.IO import File
from System import DateTime
version = "1.0"
production = False

#########################################################################################################################################
# Application Engineer:  Specific constant variables to maintain
#
testApplicationScriptFileName = "MagnaFam.json"
optionCodeFileName = "OptionsFam.json"
#
#########################################################################################################################################


try:

    TPassLogger.Debug("Main Button Script: Run a Test Application")
#    keyPadData = MainTPassScripting.GetInputKeyPad("Enter Part Number")
#    if keyPadData != "":
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        #MainTPassScripting.InterfaceUiLogger("Magna", "Keypad Data = " + keyPadData, False, False)

        #determine if part number in the scan is a Front or Rear 
    runTestCycleId = "22_53_XLT_CLOTH"
            # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true, bool useCurrentProductIdentification = false, bool bypassOverrideTestAppScript = false)
    if MainTPassScripting.RunTestCycle(testApplicationScriptFileName, optionCodeFileName, runTestCycleId):
        isSuccess = True
    else:
        isSuccess = False
        TPassLogger.Warn("Main Button Script:  Error Running Test Cycle")
#    else:
#        isSuccess = True
#        TPassLogger.Info("GetInputKeyPad() No Job Entered by Operator")


except Exception as inst:
    TPassLogger.Warn("Main Button Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Main Button Script:  Processing Failed.")
    isSuccess = False

TPassLogger.Info("Main Button Script:  Is Success = {0}", isSuccess)


############################################################
# Change History
############################################################
#   Date: 02172023
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################


