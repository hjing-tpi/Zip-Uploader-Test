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

from System.Text.RegularExpressions import Regex

production = False
version = "1.0"

#########################################################################################################################################
# Application Engineer:  Set Part Number Tag Names required for Test Application and the Test Application Script File Name
#
partNumberTags = set(["IPC","TCM","AMP","SDM","UPA","AOS","FCM","VPM","BCM","CGM","CSM","ONS","SIB","DTC","HFP","RAD","PEPS","HVAC"])
#
#########################################################################################################################################

try:

    primaryId = RunTestCycleId
    secondaryId = ""
    tertiaryId = ""
    quaternaryId = ""
    quinaryId = ""
    TPassLogger.Debug("Option Parsing Script:  Product Id = {0}", primaryId)
    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    keyValuePairs = BuildData.Split(',')
    if keyValuePairs[0] != BuildData:
        for keyValuePair in keyValuePairs:
            key = keyValuePair.Split('=')[0].Trim().ToUpper()
            value = keyValuePair.Split('=')[1].ToUpper()

            # Example ways of setting different IDs
            #if (key == "VIN"):
            #    secondaryId = value
            #elif (key == "MDYR"):
            #    tertiaryId = value
            #elif (key == "PDYR"):
            #    quaternaryId = value
            #elif (key == "CSN"):
            #    quinaryId = value

            # Populate Option Codes found in broadcasted build data
            if Regex.IsMatch(key, "\\ARP\\d") and value != "":
                TPassLogger.Debug("Option Parsing Script: RPO Found, RPO = {0}, Value = {1}", key, value)
                OptionCodesInBuildData.Add(value)
                TPassLogger.Debug("Option Parsing Script: Added Configured Option Code ({0}) found in build data", value);

            # Populate interested Part Numbers that are in the Broadcasted Build Data
            if key in partNumberTags:
                PartNumbers.Add(key, value)
                TPassLogger.Info("Option Parsing Script: Added Part ({0}, {1}) found in build data", key, value);

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
#	Date: 04152021
#	Version: 1.0
#	Change: Initial Version
############################################################

