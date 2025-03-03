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

production = False
version = "1.0"
primaryId = ""
secondaryId = ""
tertiaryId = ""
quaternaryId = ""
quinaryId = ""
isSuccess = True

#########################################################################################################################################
# Application Engineer:  Set Min Build Data parameters required and are used below
#
numberOfFieldsRequired = 21
#
#########################################################################################################################################

try:

    #Debug
    BuildData = "0000000217260,4****************,0000003168655,84783489,0102,84624332,0202,84624328,0302,84258410,0402,84281472,0505,84852372,0607,84335461,0702,84686607,0802,84686610,0902,NO-PART*,1000,NO-PART*,1100,NO-PART*,1200,11111111,1301,NO-PART*,1400,NO-PART*,1500"
    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ManualEntry):
        primaryId = RunTestCycleId
    else:
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("Barcode Scan", "Option Parsing Script:  Product Build Data Scanned = " + BuildData, False, False)
        if BuildData == "":
            MainTPassScripting.InterfaceUiLogger("Barcode Scan", "Option Parsing Script:  No Product Build Data in Scan", True, True)
            TPassLogger.Info("Option Parsing Script:  No Product Build Data in Scan")
            isSuccess = False
        else:
            buildDataFields = BuildData.split(",")
            if len(buildDataFields) >= numberOfFieldsRequired:
                primaryId = buildDataFields[0]
                secondaryId = buildDataFields[1]
                #Populate Option Codes found in broadcasted build data
                option = buildDataFields[6]
                OptionCodesInBuildData.Add(option)
                TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", option)
                MainTPassScripting.InterfaceUiLogger("Barcode Scan", "Option Parsing Script:  Added Configured Option Code - " + option, False, False)
                option = buildDataFields[8]
                OptionCodesInBuildData.Add(option)
                TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", option)
                MainTPassScripting.InterfaceUiLogger("Barcode Scan", "Option Parsing Script:  Added Configured Option Code - " + option, False, False)
                option = buildDataFields[12]
                OptionCodesInBuildData.Add(option)
                TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", option)
                MainTPassScripting.InterfaceUiLogger("Barcode Scan", "Option Parsing Script:  Added Configured Option Code - " + option, False, False)
                option = buildDataFields[18]
                OptionCodesInBuildData.Add(option)
                TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", option)
                MainTPassScripting.InterfaceUiLogger("Barcode Scan", "Option Parsing Script:  Added Configured Option Code - " + option, False, False)
                option = buildDataFields[20]
                OptionCodesInBuildData.Add(option)
                TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", option)
                MainTPassScripting.InterfaceUiLogger("Barcode Scan", "Option Parsing Script:  Added Configured Option Code - " + option, False, False)
            else:
                TPassLogger.Info("Option Parsing Script:  Invalid number of fields for Product Build Data.  Must be at least " + str(numberOfFieldsRequired) + " fields")
                # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                MainTPassScripting.InterfaceUiLogger("Barcode Scan", "Option Parsing Script:  Invalid number of fields for Product Build Data.  Must be at least " + str(numberOfFieldsRequired) + " fields", True, True)
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
#	Date: 08192022
#	Version: 1.0
#	Change: Initial Version
############################################################

