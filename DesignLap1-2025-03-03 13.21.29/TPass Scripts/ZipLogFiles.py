#Main Button Triggered Script - ZipLogFiles
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
from System.Diagnostics import Process

version = "1.0"
production = False

#####################  Application Engineer
usb = False
#####################  Application Engineer

try:
    if usb:
        # Zip to USB Drive
        TPassLogger.Info("Main Button Script Begin - ZipLogFiles to USB")
 
        p = Process()
        p.StartInfo.UseShellExecute = False
        p.StartInfo.RedirectStandardOutput = False
        p.StartInfo.FileName = "powershell.exe"
        p.StartInfo.Arguments = "-ExecutionPolicy Bypass -File \"c:\TPass\TPass Scripts\ZipFiles2Usb.ps1\""
        p.Start()
        p.WaitForExit()

        isSuccess = True
    else :
        # Zip to Desktop
        TPassLogger.Info("Main Button Script Begin - ZipLogFiles to Desktop")
 
        p = Process()
        p.StartInfo.UseShellExecute = False
        p.StartInfo.RedirectStandardOutput = False
        p.StartInfo.FileName = "powershell.exe"
        p.StartInfo.Arguments = "-ExecutionPolicy Bypass -File \"c:\TPass\TPass Scripts\ZipFiles2Desktop.ps1\""
        p.Start()
        p.WaitForExit()

        isSuccess = True
        
except Exception as inst:
    TPassLogger.Warn("Main Button Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Main Button Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Main Button Script - ZipLogFiles:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 08312021
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################
