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
version = "4.0"


try:

    #########################################################################################################################################
    # Application Engineer:  Set Unique Body Style characters that if match the VIN 4 character TPass will override the test application name
    #
    bodyStyle = ["G","P","H","R"]
    overrideAppName = "GM_31xx_EoT_01.json"
    #
    #########################################################################################################################################

    TPassLogger.Debug("Override Test Application Script:  Product ID = {0}", primaryId)
    #MainTPassScripting.InterfaceUiLogger("MES", "Override Test Application", True, True)

    # Set new test application script file name
    TPassLogger.Info("Override Test Application Script:  Current Test Application Script File Name = {0}", currentTestApplicationScriptFileName )
    TPassLogger.Info("Override Test Application Script:  VIN = {0}", secondaryId)

    newTestApplicationScriptFileName = currentTestApplicationScriptFileName

    # Compare 4th position of VIN
    if secondaryId[3] in bodyStyle:
        newTestApplicationScriptFileName = overrideAppName
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
#Date: 02132022
#   Version: 4.0
#   ChangeBy: RMM
#   Change: Simplified and correct logic.  Now uses the VIN 4th character for overriding test app
#Date: 02132022
#   Version: 2.0
#   ChangeBy: MAH
#   Change: Updated for Wentzville
#Date: 11042021
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
#
############################################################

