#Parse Attributes and specify the Test Application File Name for TPass to Execute
#This Script is expected to set the out parameter below
#TPass Objects Passed In/Returned
#   in - string "productPrimaryId"
#   in - string "productBuildData"
#   in - Function "TPassLogger"
#   out - string "productSecondaryId"
#   out - string "productTertiaryId"
#   out - string "productQuaternaryId"
#   out - string "productQuinaryId"
#   out - string "productCurrentSequenceNumber"
#   out - string "productVin"
#   out - string "productModelYear"
#   out - string "productProductionYear"
#   out - list<string> "optionCodesInBuildData"
#   out - dictionary<string,string> "partNumbers"
#   out - string "testApplicationScriptFileName"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

from System.Text.RegularExpressions import Regex

production = False
version = "1.0"

#########################################################################################################################################
# Application Engineer:  Set Part Number Tag Names required for Test Application and the Test Application Script File Name
#
partNumberTags = set(["IPC","TCM","AMP","SDM","UPA","AOS","FCM","VPM","BCM","CGM","CSM","ONS","SIB","DTC","HFP","RAD","PEPS","HVAC"])
#testApplicationScriptFileName = "2020TeslaRoadster-GlassRoof.json"
#testApplicationScriptFileName = "PAPR Main Tester 01.json"
#testApplicationScriptFileName = "PassOrFail.json"
#testApplicationScriptFileName = "2020PAPR.json"
#testApplicationScriptFileName = "IoBoardPerfTest.json"
testApplicationScriptFileName = "PAPR Battery Pack Tester.json"
#
#########################################################################################################################################

TPassLogger.Debug("Product Attribute Parsing Script:  Test App Script File Name = {0}", testApplicationScriptFileName)

productSecondaryId = "2ndID"
productTertiaryId = "3rdID"
productQuaternaryId = "4thID"
productQuinaryId = "5thID"
productVin = ""
productModelYear = ""
productProductionYear = ""
productCurrentSequenceNumber = ""

TPassLogger.Debug("Product Attribute Parsing Script:  Product Id = {0}", productPrimaryId)
TPassLogger.Debug("Product Attribute Parsing Script:  Product Build Data = {0}", productBuildData)

try:
    keyValuePairs = productBuildData.Split(',')
    if keyValuePairs[0] != productBuildData:
        for keyValuePair in keyValuePairs:
            key = keyValuePair.Split('=')[0].Trim().ToUpper()
            value = keyValuePair.Split('=')[1].ToUpper()
            if (key == "VIN"):
                productVin = value
            elif (key == "MDYR"):
                productModelYear = value
            elif (key == "PDYR"):
                productProductionYear = value
            elif (key == "CSN"):
                productCurrentSequenceNumber = value

            # Populate Option Codes found in broadcasted build data
            if Regex.IsMatch(key, "\\ARP\\d") and value != "":
                TPassLogger.Debug("Product Attribute Parsing Script: RPO Found, RPO = {0}, Value = {1}", key, value)
                optionCodesInBuildData.Add(value)
                TPassLogger.Debug("Product Attribute Parsing Script: Configured Option Code ({0}) found in build data", value);

            # Populate interested Part Numbers that are in the Broadcasted Build Data
            if key in partNumberTags:
                partNumbers.Add(key, value)
                TPassLogger.Info("Product Attribute Parsing Script: Added Part ({0}, {1}) found in build data", key, value);

    TPassLogger.Info("Product Attribute Parsing Script:  Product Primary ID = {0}, CSN = {1}, VIN = {2}, MY = {3}, PY = {4}", productPrimaryId, productCurrentSequenceNumber, productVin, productModelYear, productProductionYear )
    isSuccess = True

except Exception as inst:
    TPassLogger.Warn("Product Attribute Parsing Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Product Attribute Parsing Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Product Attribute Parsing Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 01012019
#	Version: 1.0
#	Change: Initial Version
############################################################

