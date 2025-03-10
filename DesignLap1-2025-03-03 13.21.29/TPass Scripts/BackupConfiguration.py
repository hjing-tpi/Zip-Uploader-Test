#Hamburger Menu Button - BackupConfiguration
#This Script can run any python logic in order to backup the configuration as a zip file to the desktop
#TPass Objects Passed In/Returned
#   in  - object MainTPassScripting - Exposed all methods and properties for the scripts to use
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

import clr
from System.Diagnostics import Process

version = "1.0"
production = False

#####################  Application Engineer

#####################  Application Engineer

try:

    # Zip to Desktop
    TPassLogger.Info("Hamburger Button Script Begin - ZipLogFiles to Desktop")

    p = Process()
    p.StartInfo.UseShellExecute = False
    p.StartInfo.RedirectStandardOutput = False
    p.StartInfo.FileName = "powershell.exe"
    p.StartInfo.Arguments = "-ExecutionPolicy Bypass -File \"c:\TPass\TPass Scripts\BackupConfiguration.ps1\""
    p.Start()
    p.WaitForExit()

    isSuccess = True
        
except Exception as inst:
    TPassLogger.Warn("Hamburger Button Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Hamburger Button Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Hamburger Button Script - BackupConfiguration:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 02032025
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################
