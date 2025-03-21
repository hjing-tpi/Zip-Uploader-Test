#Override Test Application - Parse the build data passed in from the request script and set the product attribute variables
#This Script is expected to set the out parameter below
#
#TPass Objects Passed In/Returned
#   in - string "currentTestApplicationScriptFileName"
#   in - string "primaryId"
#   in - string "secondaryId"
#   in - string "tertiaryId"
#   in - string "quaternaryId"
#   in - string "quinaryId"
#   in - string "buildData"
#   in - List<string> "activeOptionCodes" 'All options are upper case
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
#   out - string "newTestApplicationScriptFileName"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();
from System.Text.RegularExpressions import Regex

production = False
version = "5.0"

TPassLogger.Debug("Override Test Application Script:  Product ID = {0}", primaryId)

try:

    # Set new test application script file name
    TPassLogger.Info("Override Test Application Script:  Current Test Application Script File Name = {0}", currentTestApplicationScriptFileName )
    TPassLogger.Info("Override Test Application Script:  secondary ID = {0}", secondaryId)

    if activeOptionCodes.Contains("L233") or activeOptionCodes.Contains("L234"):
        newTestApplicationScriptFileName = "GM_L23X_IP_01.json"
    elif activeOptionCodes.Contains("6NA"): 
        newTestApplicationScriptFileName = currentTestApplicationScriptFileName # GM_C1xx_IP_01.json from Autostart script
    else:
        newTestApplicationScriptFileName = "GM_S233_IP_01.json"

    # if activeOptionCodes.Contains("L234") and activeOptionCodes.Contains("EN0"):
        # newTestApplicationScriptFileName = "GM_L23X_IP_01.json"
    # elif activeOptionCodes.Contains("L233") and activeOptionCodes.Contains("EN0"):
        # newTestApplicationScriptFileName = "GM_L233_IP_01.json"
    # elif activeOptionCodes.Contains("EN0"):
        # newTestApplicationScriptFileName = "GM_S233_IP_01.json"
    # else:
        # newTestApplicationScriptFileName = currentTestApplicationScriptFileName

    # if len(secondaryId) >= 2: 
    #     if secondaryId.strip()[1] == 'G' and activeOptionCodes.Contains("EN0"):
    #         newTestApplicationScriptFileName = "GM_L23X_IP_01.json"
    #     elif activeOptionCodes.Contains("EN0"):
    #         newTestApplicationScriptFileName = "GM_S233_IP_01.json"
    #     else:
    #         newTestApplicationScriptFileName = currentTestApplicationScriptFileName
    # else:
    #       newTestApplicationScriptFileName = currentTestApplicationScriptFileName

    MainTPassScripting.InterfaceUiLogger("MES", newTestApplicationScriptFileName + " " + secondaryId, False, False)

    TPassLogger.Debug("Override Test Application Script:  New Test Application Script File Name = {0}", newTestApplicationScriptFileName )
    isSuccess = True

except Exception as inst:
    TPassLogger.Warn("Override Test Application Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Override Test Application Script:  Processing Failed.")
    isSuccess = False
    
TPassLogger.Info("Override Test Application Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 12232024
#   Version: 5.0
#   Change: Separated L23X, S233 and C1XX test apps
#   Date: 05232024
#   Version: 4.0
#   ChangeBy: LM
#   Change: Changed to look at passed option codes from Option parser L233 or L234 with EN0, if just EN0 then run S233, if not EN0 at all then run the original 
#   Date: 11042023
#   Version: 3.0
#   ChangeBy: LM
#   Change: Added Fix for Steven 
############################################################

