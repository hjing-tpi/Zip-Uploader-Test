#Parse build data passed in and populate IDs, options and part numbers
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in - string "RunTestCycleId" - Id passed into the RunTestCycle() method
#   in - string "BuildData" - Build data sent from the option retrieval script
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application log file
#   in  - method "GetConfigurationValue" - This is the method to get values set in the System Configuration file
#   out - string "primaryId"
#   out - string "secondaryId"
#   out - string "tertiaryId"
#   out - string "quaternaryId"
#   out - string "quinaryId"
#   out - list<string> "OptionCodesInBuildData"
#   out - dictionary<string,string> "PartNumbers"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

production = False
version = "0.1"

from System.Text.RegularExpressions import Regex

#########################################################################################################################################
# Application Engineer:  
#

#########################################################################################################################################
# Application Engineer:  Set Option number, Option Tag Name and Part Number Tag Name required for Test Application
#
#            #, SeatDataName
seatMatrixColumnNames = ["Plant","Vehicle","Trim","Heater","PwrMan","DelphiPN","Suffix","OemPN","Threshold","PVMTestString","Breakin","OverMin","OverMax","InSeatAngle","ForceStable","BreakinDwell","EmptyTrigger","SmcPrg", "SmcSP", "XaxisRef", "EmptyPreLearn", "AllowMult", "EmptyLow", "EmptyHigh", "AllowLow", "AllowHigh"]
#
#########################################################################################################################################

try:

    #BuildData = "Magna Louisville,U553,22_53_XLT_CLOTH,None,2 Way Manual,28752190.0,  ,NL1B-14B422-AB                      ,53.0,-test 1.0.1.7F -rec,90.0,85.0,95.0,16.0,1.0,1.0,1.2,1.0,0.0,0.0,0.0,128.0,35.0,70.0,62.0,96.0"
    primaryId = RunTestCycleId
    secondaryId = ""
    tertiaryId = ""
    quaternaryId = ""
    quinaryId = ""
    TPassLogger.Debug("Option Parsing Script:  Product Id = {0}", primaryId)
    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)
    MainTPassScripting.InterfaceUiLogger("Magna", "Option Parsing Script:  Build Data = " + BuildData, False, False)

    seatMatrixData = BuildData.Split(',')
    index = 0
    for seatMatrixField in seatMatrixData:
        if len(seatMatrixData) < index + 1:
            TPassLogger.Error("Option Parsing Script:  Field {0} not found in SeatMatrix file", seatMatrixColumnNames[index])
            MainTPassScripting.InterfaceUiLogger("Magna", "Option Parsing Script:  Field " + seatMatrixColumnNames[index] + " not found in SeatMatrix file", true, true)
            isSuccess = False
            break
        key = seatMatrixColumnNames[index].Trim()
        value = seatMatrixData[index]

        # Example ways of setting different IDs
        if (key == "Vehicle"):
            secondaryId = value

        # Set Seat Parts that are in the SeatMatrix Build Data
        TPassLogger.Info("Option Parsing Script: Added Seat Part ({0}, {1}) found in build data", key, value);
        PartNumbers.Add(key, value)                
        MainTPassScripting.InterfaceUiLogger("Magna", "Option Parsing Script:  Added Seat Part: " + key + "=" + value, False, False)
        index += 1

    TPassLogger.Info("Option Parsing Script:  Product Primary ID = {0}", primaryId)
    isSuccess = True

except Exception as inst:
    TPassLogger.Warn("Option Parsing Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Parsing Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Parsing Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 02282023
#   Version: 0.1
#   Change: Initial Version
############################################################

