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
from System import String
version = "1.0"
production = False

TPassLogger.Debug("Main Button Script Begin")

try:

        TPassLogger.Info("Main Button Script: Run a Test Application, requesting and processing options and results")
        
        # returned_value, errorMsgOut = MainTPassScripting.IncomingSerialClient.Send("Data from PassOrFail Script", String(""))
        # if (SystemConfigurationValue.Hardware.Scanners.Serial.Enabled):
            # if (not returned_value):
                # MainTPassScripting.InterfaceUiLogger("Serial", "Error Sending results to Serial Scanner device: " + errorMsgOut, True, True)
            # else:
                # MainTPassScripting.InterfaceUiLogger("Serial", "Results sent to Serial Scanner device", False, False)
            
        # else:
            # MainTPassScripting.InterfaceUiLogger("Serial", "Serial Scanner not enabled", True, True)
        
#        if MainTPassScripting.RunTestCycle("GM_BV1HX_IP_01E.json", "OptionCodes-Tesla.json", "987654", False, True):
        # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true, bool useCurrentProductIdentification = false)
        if MainTPassScripting.RunTestCycle("PassOrFailAudit.json", "OptionCodes-Tesla.json", "008712", False, True, False):
#        if MainTPassScripting.RunTestCycle("Current Draw Test.json", "OptionCodes-Tesla.json", "987654", False, True):
#        if MainTPassScripting.RunTestCycle("Dakkota_WL_IP_01.json", "OptionCodes-Tesla.json", "987654", False, True):
            isSuccess = True
        else:
            isSuccess = False
            TPassLogger.Warn("Main Button Script:  Error Running Test Cycle")

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
############################################################
