#Parse Attributes - Parse the build data passed in from the request script and set the product attribute variables
#This Script is expected to set the out parameter below
#
#TPass Objects Passed In/Returned
#   in - string "RunTestCycleId" - Id passed into the RunTestCycle() method
#   in - string "BuildData" - Build data sent from the attribute retrieval script
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
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

#System.Diagnostics.Debugger.Break();

from System.Text.RegularExpressions import Regex

production = False
version = "1.0"

#########################################################################################################################################
# Application Engineer:  Set Part Number Tag Names required for Test Application and the Test Application Script File Name
#
partNumberTags = set(["IPC","TCM","AMP","SDM","UPA","AOS","FCM","VPM","BCM","CGM","CSM","ONS","SIB","DTC","HFP","RAD","PEPS","HVAC"])
#########################################################################################################################################

TPassLogger.Debug("Product Attribute Parsing Script:  Product Build Data = {0}", BuildData)
#MainTPassScripting.InterfaceUiLogger("MES", "Attribute Parsing", True, True)

try:

    # Parse the build data and set the attributes
    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Scan):
        TPassLogger.Debug("OptionParsing - Trigger Type is Scan")
    elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ContinuousMode):
        TPassLogger.Debug("OptionParsing - Trigger Type is ContinuousMode")
    primaryId = RunTestCycleId
    secondaryId = "2"
    tertiaryId = "3"
    quaternaryId = "4"
    quinaryId = "5"
    
    PartNumbers.Add("BcM", "12345678")

    TPassLogger.Debug("Product Attribute Parsing Script:  Primary ID = {0}, Secondary ID = {1}, Tertiary ID = {2}, Quaternary ID = {3}, Quinary ID = {4}", primaryId, secondaryId, tertiaryId, quaternaryId, quinaryId )
    isSuccess = True

except Exception as inst:
    TPassLogger.Warn("Product Attribute Parsing Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Product Attribute Parsing Script:  Processing Failed.")
    isSuccess = False
    
TPassLogger.Info("Product Attribute Parsing Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 01012019
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################

