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


try:

    #Debug
    #BuildData = "0184964290;42786792_IPC,85572148_RAD,84579083_HVACBB,85546373_AUDDSP,84684288_HVACDSP,00000000_HMI,00000000_ONSTAR,13533478_CGM,00000000_CLM,00000000_CSM,86804753_TCP;E2SC,AUDDSP,HVACDSP,HVG,KNEE,CGM,PEP,RAD,TCP,WIFI,ETHERNET,XMA,MY22"

    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    primaryId = "Unknown"
    if BuildData == "":
        if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.FileDrop):
            TPassLogger.Info("Option Parsing Script:  No Product Build Data")
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            MainTPassScripting.InterfaceUiLogger("TCPInterface", "Option Parsing Script:  Empty build data from file drop", True, True)
            isSuccess = False
        else:
            TPassLogger.Info("Option Parsing Script:  No Product Build Data")
            primaryId = RunTestCycleId

    else:
        buildDataFields = BuildData.split(";")
        optionField = ""
        partField = ""
        if len(buildDataFields) == 3:
            primaryId = buildDataFields[0]
            secondaryId = primaryId
            partField = buildDataFields[1]
            optionField = buildDataFields[2]
        elif len(buildDataFields) >= 6:
            primaryId = buildDataFields[2]
            secondaryId = buildDataFields[0]
            partField = buildDataFields[4]
            optionField = buildDataFields[5]
        else:
            TPassLogger.Info("Option Parsing Script:  Invalid number of fields for Product Build Data.  Must be 3 fields or 6 or more")
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            MainTPassScripting.InterfaceUiLogger("TCPInterface", "Option Parsing Script:  Invalid number of fields for Product Build Data.  Must be 3 fields or 6 or more", True, True)
            isSuccess = False
        
        #Populate Option Codes found in broadcasted build data
        options = optionField.split(",")
        for optionName in options:
            OptionCodesInBuildData.Add(optionName)
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
            MainTPassScripting.InterfaceUiLogger("TCPInterface", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)
        
        #Populate Part Numbers that are in the broadcasted Build Data
        parts = partField.split(",")
        for part in parts:
            partNameValue = part.split("_")
            partName = partNameValue[1]
            partNumber = partNameValue[0]
            if PartNumbers.ContainsKey(partName):
                TPassLogger.Warn("Option Parsing Script: Part Tag ({0}, {1}) found twice in build data.  First occurrence will be used", partName, partNumber);
                MainTPassScripting.InterfaceUiLogger("TCPInterface", "Option Parsing Script:  Part Tag found twice in the build data.  First occurrence will be used - " + partName + " = " + partNumber, True, False)
            else:
                TPassLogger.Info("Option Parsing Script: Added Part ({0}, {1}) found in build data", partName, partNumber);
                PartNumbers.Add(partName, partNumber)                
                MainTPassScripting.InterfaceUiLogger("TCPInterface", "Option Parsing Script:  Added Configured Part - " + partName + " = " + partNumber, False, False)

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
#	Date: 06222022
#	Version: 1.0
#	Change: Initial Version
############################################################

