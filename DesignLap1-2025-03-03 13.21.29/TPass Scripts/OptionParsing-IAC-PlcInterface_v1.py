#Parse build data passed in and populate IDs, options and part numbers
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - string "RunTestCycleId" - This is the data that was passed from the Start Test Cycle script via the RunTestCycle method.
#   in  - string "BuildData" - Build data sent from the option retrieval script which was set in the productBuildData out variable
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application Detail log file
#   in  - object "SystemConfigurationValue" - This is the object to get values set in the System Configuration file
#   out - string "primaryId"
#   out - string "secondaryId"
#   out - string "tertiaryId"
#   out - string "quaternaryId"
#   out - string "quinaryId"
#   out - list<string> "OptionCodesInBuildData"
#   out - dictionary<string,string> "PartNumbers"
#   out - bool "isSuccess" - Set to True if build data parsing was successful.  Otherwise False
#   out - bool "production"
#   out - string "version"
#

from System.Collections.Generic import Dictionary

production = False
version = "1.0"
primaryId = ""
secondaryId = ""
tertiaryId = ""
quaternaryId = ""
quinaryId = ""
isSuccess = True

optionInfo = Dictionary[str, str]()

#########################################################################################################################################
# Application Engineer:  Set Recipe number, Option Tag Names (comma delimited) that are required for Test Application 
#
#               #, OptionNames

optionInfo.Add("1", "CHEVY")
optionInfo.Add("2", "CHEVY")
optionInfo.Add("3", "CHEVY,MEMORY")
optionInfo.Add("4", "CHEVY,MEMORY")
optionInfo.Add("5", "CHEVY,MEMORY")
optionInfo.Add("6", "CHEVY")
optionInfo.Add("11", "DENALI")
optionInfo.Add("15", "DENALI")
optionInfo.Add("21", "CADILLAC,BASE")
optionInfo.Add("22", "CADILLAC,PREMIUM")
optionInfo.Add("23", "CADGMC,BASE")
optionInfo.Add("24", "CADGMC,PREMIUM")
optionInfo.Add("25", "CADILLAC,BASE")
optionInfo.Add("26", "CADILLAC,PREMIUM")

#
#########################################################################################################################################

try:

    #Debug
    #BuildData = "14645372;11"

    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    primaryId = "Unknown"
    if BuildData == "":
        if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.FileDrop):
            TPassLogger.Info("Option Parsing Script:  No Product Build Data")
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            MainTPassScripting.InterfaceUiLogger("PLCInterface", "Option Parsing Script:  Empty build data from file drop", True, True)
            isSuccess = False
        else:
            TPassLogger.Info("Option Parsing Script:  No Product Build Data")
            primaryId = RunTestCycleId
    else:
        buildDataFields = BuildData.split(";")
        recipeField = ""
        if len(buildDataFields) == 2:
            primaryId = buildDataFields[0]
            recipeField = buildDataFields[1]
            secondaryId = recipeField

            #Populate Option Codes found in broadcasted build data
            if optionInfo.ContainsKey(recipeField):
                optionField = optionInfo[recipeField]
                options = optionField.split(",")
                for optionName in options:
                    OptionCodesInBuildData.Add(optionName)
                    TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
                    MainTPassScripting.InterfaceUiLogger("PLCInterface", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)
            else:
                TPassLogger.Info("Option Parsing Script: Not a valid Recipe {0}.  Check Option Parsing Script", recipeField);
                MainTPassScripting.InterfaceUiLogger("PLCInterface", "Option Parsing Script: Not a valid Recipe " + recipeField + ".  Check Option Parsing Script Configuration", True, True)
                isSuccess = False
        else:
            TPassLogger.Info("Option Parsing Script:  Invalid number of fields for Product Build Data.  Must be 2 fields")
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            MainTPassScripting.InterfaceUiLogger("PLCInterface", "Option Parsing Script:  Invalid number of fields for Product Build Data.  Must be 2 fields", True, True)
            isSuccess = False
        
        TPassLogger.Info("Option Parsing Script:  Product Primary ID = {0}", primaryId)
        TPassLogger.Info("Option Parsing Script:  Secondary ID = {0}", secondaryId)

except Exception as inst:
    TPassLogger.Warn("Option Parsing Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Parsing Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Parsing Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 07182022
#	Version: 1.0
#	Change: Initial Version
############################################################

