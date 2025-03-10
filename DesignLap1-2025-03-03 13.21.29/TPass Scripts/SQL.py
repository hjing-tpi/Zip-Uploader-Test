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
#clr.AddReferenceToFileAndPath('.\\Tpi.TPass.Common.dll')
#clr.AddReferenceToFileAndPath('.\\IronPython.Modules.dll')
clr.AddReferenceToFileAndPath('.\\IronPython.SQLite.dll')
import sys
#sys.path.append(r"C:\Program Files\IronPython 2.7\Lib")
#sys.path.append(r"C:\Program Files\IronPython 2.7\Lib\sqlite3")
#import os
version = "1.0"
production = False

from _sqlite3 import *

TPassLogger.Debug("Main Button Script Begin")

try:
        TPassLogger.Info("Main Button Script: Run a Quick Test Application with default options only and don't process results")
        db = Connection("C:\\TPass\\bin\\DataBase\\Tpi.Tpass.Db")
        cursor = db.execute("""SELECT * FROM TestCycle""")
        records = cursor.fetchall() 
        
        for row in records:
            TPassLogger.Info("Results: {0}", str(row))

#        MainTPassScripting.InterfaceUiLogger("MES", "AllTestStepCommands Script", True, True)
#        if MainTPassScripting.RunTestCycle("PassOrFail.json", "OptionCodes-Tesla.json", "987654", True, False):
#            isSuccess = True
#        else:
#            isSuccess = False
#            TPassLogger.Warn("Main Button Script:  Error Running Quick Test Cycle")

        TPassLogger.Info("Main Button Script: Run a Test Application, requesting and processing options and results")
        isSuccess = True

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
