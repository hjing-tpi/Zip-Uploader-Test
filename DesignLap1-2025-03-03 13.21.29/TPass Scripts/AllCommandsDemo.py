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
clr.AddReference("System.Data.SQLite")
from System.Data.SQLite import SQLiteConnection

TPassLogger.Debug("Main Button Script Begin")

try:
        TPassLogger.Info("Main Button Script: Run a Quick Test Application with default options only and don't process results")
        db = SQLiteConnection("Data Source=C:\TPass\bin\DataBase\Tpi.Tpass.Db;Version=3")
        #db.Open()
#        MainTPassScripting.InterfaceUiLogger("MES", "AllTestStepCommands Script", True, True)
#        if MainTPassScripting.RunTestCycle("PassOrFail.json", "OptionCodes-Tesla.json", "987654", True, False):
#            isSuccess = True
#        else:
#            isSuccess = False
#            TPassLogger.Warn("Main Button Script:  Error Running Quick Test Cycle")

        TPassLogger.Info("Main Button Script: Run a Test Application, requesting and processing options and results")
        # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true, bool useCurrentProductIdentification = false, bool bypassOverrideTestAppScript = false)
        if MainTPassScripting.RunTestCycle("AllTestStepCommandsSeatDemo.json", "OptionCodes-Demo.json", "008712", False, True, False, False):
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
