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
from System.IO import File

lineRelease = "C:\TPass\Data Outgoing\PLC_Release.txt"

try:
    TPassLogger.Debug("Main Button Script: Run Line Release")
    if not File.Exists(lineRelease):
        if File.Exists(lineRelease + "TMP"):
            try:
                File.Delete(lineRelease + "TMP")
            except Exception as inst:
                TPassLogger.Debug("Option Retrieval Script:  File.Delete Exception Occurred :{0}", inst)            
        File.WriteAllText(lineRelease + "TMP", "Release")
        File.Move(lineRelease + "TMP", lineRelease)
        TPassLogger.Info("Main Button Script: Creating Line Release File")
        MainTPassScripting.InterfaceUiLogger("Line Release", "Created Line Release File", False, False)
        isSuccess = True
    else:
        TPassLogger.Info("Main Button Script: Line Release File Already Exists")
        MainTPassScripting.InterfaceUiLogger("Line Release", "Line Release File Already Created", True, True)
        isSuccess = False

except Exception as inst:
    TPassLogger.Warn("Main Button Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Main Button Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Main Button Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 07212023
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Fixed file contingency issue 
#   Date: 07112023
#   Version: 1.0
#   ChangeBy: LM
#   Change: Initial Verison
############################################################

