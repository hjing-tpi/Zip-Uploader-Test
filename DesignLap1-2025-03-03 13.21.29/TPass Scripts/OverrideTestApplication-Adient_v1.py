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
version = "1.0"

def LoopLogger(optionCodeList):
    for optionName in optionCodeList:
        TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
        MainTPassScripting.InterfaceUiLogger("SQLConnect", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)

TPassLogger.Debug("Override Test Application Script:  Tertiary ID = {0}", tertiaryId)

try:
    
    # Set new test application script file name
    if tertiaryId == "1" and tertiaryId != "":
        rcpCodes = List[str](["RANGE_OF_MOTION","AIRBAG","SPS","BUCKLE","SHORT_TO_GROUND","SHIP_POSITION"])
        OptionCodesInBuildData.AddRange(rcpCodes)
        LoopLogger(rcpCodes)
    elif tertiaryId == "2" and tertiaryId != "":
        rcpCodes = List[str](["RANGE_OF_MOTION","AIRBAG","SPS","BUCKLE","HEAT","SHORT_TO_GROUND","SHIP_POSITION"])
        OptionCodesInBuildData.AddRange(rcpCodes)
        LoopLogger(rcpCodes)
    elif tertiaryId == "3" and tertiaryId != "":
        rcpCodes = List[str](["RANGE_OF_MOTION","MOTOR_DRAW","AIRBAG","SPS","BUCKLE","SHORT_TO_GROUND","SHIP_POSITION"])
        OptionCodesInBuildData.AddRange(rcpCodes)
        LoopLogger(rcpCodes)
    elif tertiaryId == "4" and tertiaryId != "":
        rcpCodes = List[str](["RANGE_OF_MOTION","MOTOR_DRAW","AIRBAG","SPS","BUCKLE","HEAT","SHORT_TO_GROUND","SHIP_POSITION"])
        OptionCodesInBuildData.AddRange(rcpCodes)
        LoopLogger(rcpCodes)
    elif tertiaryId == "5" and tertiaryId != "":
        rcpCodes = List[str](["RANGE_OF_MOTION","AIRBAG","BUCKLE","SHORT_TO_GROUND","SHIP_POSITION"])
        OptionCodesInBuildData.AddRange(rcpCodes)
        LoopLogger(rcpCodes)
    elif tertiaryId == "6" and tertiaryId != "":
        rcpCodes = List[str](["RANGE_OF_MOTION","AIRBAG","BUCKLE","HEAT","SHORT_TO_GROUND","SHIP_POSITION"])
        OptionCodesInBuildData.AddRange(rcpCodes)
        LoopLogger(rcpCodes)
    elif tertiaryId == "7" and tertiaryId != "":
        rcpCodes = List[str](["RANGE_OF_MOTION","MOTOR_DRAW","AIRBAG","BUCKLE","HEAT","SHORT_TO_GROUND","SHIP_POSITION"])
        OptionCodesInBuildData.AddRange(rcpCodes)
        LoopLogger(rcpCodes)

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
#   Date: 11042021
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################

