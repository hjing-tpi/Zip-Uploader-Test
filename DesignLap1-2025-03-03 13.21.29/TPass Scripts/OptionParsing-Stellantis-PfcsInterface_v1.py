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

#from System.Collections.Generic import Dictionary, List

production = False
version = "1.0"
primaryId = "Unknown"
secondaryId = ""
tertiaryId = ""
quaternaryId = ""
quinaryId = ""
isSuccess = True


#########################################################################################################################################
# Application Engineer:  Set Part Number Tag Names in the order of how they are broad casted
partNumberName = ["RRM_PN","HVAC_PN","IPC_PN","PAM_PN","HCPM_PN","EMCM_PN","DCSD_PN","ESM_PN"]       #Guessed on ESM_PN position
#
################################################################################################

# pfcs format constants
optionLength = 3
partNumberLength = 10

#########################################################################################################################################
# Software Engineer: Debugging 
#BuildData = "E8NE10007263030472KZ0454340HAA000000BNBLNJ000RDG000RDZ000JLNJCJ000000RFVJKV000PAM000000XC4000000000R02:68508691AA68516124AA68521548AA68516315AA\r\n"
#########################################################################################################################################


try:

    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    if BuildData == "":
        TPassLogger.Info("Option Parsing Script:  No Product Build Data")
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Option Parsing Script:  Empty build data", True, True)
        primaryId = RunTestCycleId
    else:
        BuildData = BuildData.strip()
        pfcsHeader = BuildData[0:27]
        pfcsBuildRecord = BuildData[27:]
        primaryId = pfcsHeader[2:10]        #VIN
        secondaryId = pfcsHeader[10:18]     #AVI
        options = ""
        partNumbers = ""
        if pfcsBuildRecord.find(":") != -1:
            pvcsBuildArray = pfcsBuildRecord.split(":")
            options = pvcsBuildArray[0]
            partNumbers = pvcsBuildArray[1]
        else:
            options = pfcsBuildRecord
            MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Option Parsing Script:  No Part Numbers found in build data", True, True)
        
        # Add options
        i = 0
        while i < len(options):
            option = options[i:i+optionLength]
            if option != "000":
                OptionCodesInBuildData.Add(option)
                TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", option)
                MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Option Parsing Script:  Added Configured Option Code - " + option, False, False)
            i += optionLength
        
        # Add part numbers
        i = 0
        partNumberIndex = 0
        while i < len(partNumbers) and partNumberIndex < len(partNumberName):
            partNumber = partNumbers[i:i+partNumberLength]
            partName = partNumberName[partNumberIndex]
            if PartNumbers.ContainsKey(partName):
                TPassLogger.Warn("Option Parsing Script: Part Tag ({0}, {1}) found twice in build data.  First occurrence will be used", partName, partNumber)
                MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Option Parsing Script:  Part Tag found twice in the build data.  First occurrence will be used - " + partName + " = " + partNumber, True, False)
            else:
                TPassLogger.Info("Option Parsing Script: Added Part ({0}, {1}) found in build data", partName, partNumber)
                MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Option Parsing Script:  Added Configured Part - " + partName + " = " + partNumber, False, False)
                PartNumbers.Add(partName, partNumber)
            i += partNumberLength
            partNumberIndex += 1
                
        TPassLogger.Info("Option Parsing Script:  Product Primary ID = {0}", primaryId)
        TPassLogger.Info("Option Parsing Script:  Secondary ID = {0}", secondaryId)
        TPassLogger.Info("Option Parsing Script:  Tertiary ID = {0}", tertiaryId)
        TPassLogger.Info("Option Parsing Script:  Quaternary ID = {0}", quaternaryId)
        TPassLogger.Info("Option Parsing Script:  Quinary ID = {0}", quinaryId)

except Exception as inst:
    TPassLogger.Warn("Option Parsing Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Parsing Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Parsing Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 11282023
#	Version: 1.0
#	Change: Initial Version
#   Changed By: RMM
############################################################

