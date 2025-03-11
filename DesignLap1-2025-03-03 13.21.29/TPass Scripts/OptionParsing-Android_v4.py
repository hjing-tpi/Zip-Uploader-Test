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
version = "4.0"
primaryId = ""
secondaryId = ""
tertiaryId = ""
quaternaryId = ""
quinaryId = ""
isSuccess = True

partNumberMatrix = Dictionary[str, str]()

#########################################################################################################################################
# Application Engineer:  Set parameters required used to process the build data and identify Part Number tag names
#
numberOfFieldsRequired = 3

#                    First two characters of the ModCode Number, PartName
partNumberMatrix.Add("62", "RCHVAC_PN")
partNumberMatrix.Add("63", "RCHVAC_PN")
partNumberMatrix.Add("64", "SIB_PN")
partNumberMatrix.Add("65", "WCM_PN")
partNumberMatrix.Add("67", "MFCM_PN")
partNumberMatrix.Add("78", "VKM_PN")    #???
partNumberMatrix.Add("82", "FPIM_PN")   #???

#
#########################################################################################################################################

try:

    #Debug
    BuildData = "0000000987860,112**************,0000000914301,2023****,0102,2024****,0103,84967266,0201,84967266,0323,NO-PART*,0400,85159594,0513,NO-PART*,0600,NO-PART*,0700,NO-PART*,1900,13549126,2004,86782314,2126,NO-PART*,2200,NO-PART*,2300,NO-PART*,2400,85595147,3326,NO-PART*,3700,NO-PART*,4200,NO-PART*,5300,NO-PART*,5400,84651488,5505,NO-PART*,5600,NO-PART*,5900,85599127,6002,84525839,6101,84186652,6201,NO-PART*,6400,13537143,6501,NO-PART*,6600,NO-PART*,6700,NO-PART*,6800,NO-PART*,6900"
    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    if str(MainTPassScripting.StartTestCycleTriggerType) != str(MainTPassScripting.TriggerType.ManualEntry):
        primaryId = RunTestCycleId
    else:
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("Scan", "Option Parsing Script:  Product Build Data Scanned = " + BuildData, False, False)
        if BuildData == "":
            MainTPassScripting.InterfaceUiLogger("Scan", "Option Parsing Script:  No Product Build Data in Scan", True, True)
            TPassLogger.Info("Option Parsing Script:  No Product Build Data in Scan")
            isSuccess = False
        else:
            buildDataFields = BuildData.split(",")
            if len(buildDataFields) >= numberOfFieldsRequired and (len(buildDataFields) % 2) != 0:      #must be odd in length
                primaryId = buildDataFields[0].lstrip("0")      #Sequence Number
                secondaryId = buildDataFields[1].rstrip("*")    #VIN
                tertiaryId = buildDataFields[2].lstrip("0")     #Rotation
                
                #Populate Option Codes and Part Numbers found in broad casted build data
                offset = 3
                while offset < len(buildDataFields):
                    if (offset % 2) == 0:   #Even offset which is the Option to be added
                        OptionCodesInBuildData.Add(buildDataFields[offset])
                        TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", buildDataFields[offset])
                        MainTPassScripting.InterfaceUiLogger("Scan", "Option Parsing Script:  Added Configured Option Code - " + buildDataFields[offset], False, False)
                        modCodeNumber = buildDataFields[offset][:2]
                        if (partNumberMatrix.ContainsKey(modCodeNumber)):
                            partTag = partNumberMatrix[modCodeNumber]
                            partNumber = buildDataFields[offset-1] # Part number is in front of the mod code
                            if (PartNumbers.ContainsKey(partTag)):
                                TPassLogger.Error("Option Parsing Script:  Duplicate Part Name found Mode Code {0}, Part Number will be ignored {1} = {2} ", buildDataFields[offset], partTag, partNumber)
                                MainTPassScripting.InterfaceUiLogger("Scan", "Option Parsing Script:  Duplicate Part Name found Mode Code " + buildDataFields[offset] + ", " + "Part Number will be ignored  "  + partTag + " = " + partNumber, True, False)
                            else:
                                PartNumbers.Add(partTag, partNumber) 
                                TPassLogger.Info("Option Parsing Script: Added Configured Part Number {0} = {1} found in build data", partTag, partNumber)
                                MainTPassScripting.InterfaceUiLogger("Scan", "Option Parsing Script:  Added Configured Part Number " + partTag + " = " + partNumber, False, False)
                    offset += 1
                # Set Model Year Options
                if (OptionCodesInBuildData.Contains("0102")):
                    OptionCodesInBuildData.Add("MY23")
                    TPassLogger.Info("Option Parsing Script: Added Configured Option Code MY23 found in build data")
                    MainTPassScripting.InterfaceUiLogger("Scan", "Option Parsing Script:  Added Configured Option Code - MY23", False, False)
                if (OptionCodesInBuildData.Contains("0103")):
                    OptionCodesInBuildData.Add("MY24")
                    TPassLogger.Info("Option Parsing Script: Added Configured Option Code MY24 found in build data")
                    MainTPassScripting.InterfaceUiLogger("Scan", "Option Parsing Script:  Added Configured Option Code - MY24", False, False)
            else:
                TPassLogger.Info("Option Parsing Script:  Invalid number of fields for Product Build Data.  Must be at least " + str(numberOfFieldsRequired) + " fields and odd in length")
                # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                MainTPassScripting.InterfaceUiLogger("Scan", "Option Parsing Script:  Invalid number of fields for Product Build Data.  Must be at least " + str(numberOfFieldsRequired) + " fields and odd in length", True, True)
                isSuccess = False
        
    TPassLogger.Info("Option Parsing Script:  Product Primary ID = {0}", primaryId)
    TPassLogger.Info("Option Parsing Script:  Secondary ID = {0}", secondaryId)
    TPassLogger.Info("Option Parsing Script:  TertiaryId ID = {0}", tertiaryId)

except Exception as inst:
    TPassLogger.Warn("Option Parsing Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Parsing Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Parsing Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 08172023
#	Version: 4.0
#	Change: Added logic for adding part numbers and fixed logic for adding options
#	Date: 04142023
#	Version: 3.0
#	Change: Removed NO-PART logic. Need no part modcodes for reverse logic presence.
#	Date: 08202022
#	Version: 2.0
#	Change: Wrote generic algorithm for adding options, that have corresponding parts that don't contain the string "NO-PART".  Serial scan must be odd number of parameters
#	Date: 08192022
#	Version: 1.0
#	Change: Initial Version
############################################################

