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
#   out - dictionary<string,string> "PartNumbers"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

#from System.Text.RegularExpressions import Regex

production = False
version = "1.0"
isSuccess = True

TPassLogger.Debug("Override Test Application Script:  Product ID = {0}", primaryId)
#MainTPassScripting.InterfaceUiLogger("MES", "Override Test Application", True, True)

try:

    newTestApplicationScriptFileName = currentTestApplicationScriptFileName
    #if the user manually selected options
    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ManualEntry):
        if activeOptionCodes.Contains("KTB1S1B1"):
            if (PartNumbers.ContainsKey("KTB1BUCKLES") == False):
                PartNumbers.Add("KTB1BUCKLES", "1") 
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Override Script:  Added Part: KTB1BUCKLES=1", False, False)
        elif activeOptionCodes.Contains("KTB1S1B2"):
            if (PartNumbers.ContainsKey("KTB1BUCKLES") == False):
                PartNumbers.Add("KTB1BUCKLES", "2") 
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Override Script:  Added Part: KTB1BUCKLES=2", False, False)
        elif activeOptionCodes.Contains("KTB1S1B3"):
            if (PartNumbers.ContainsKey("KTB1BUCKLES") == False):
                PartNumbers.Add("KTB1BUCKLES", "3") 
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Override Script:  Added Part: KTB1BUCKLES=3", False, False)
        if activeOptionCodes.Contains("KTB2S2B1"):
            if (PartNumbers.ContainsKey("KTB2BUCKLES") == False):
                PartNumbers.Add("KTB2BUCKLES", "1") 
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Override Script:  Added Part: KTB2BUCKLES=1", False, False)
        elif activeOptionCodes.Contains("KTB2S2B2"):
            if (PartNumbers.ContainsKey("KTB2BUCKLES") == False):
                PartNumbers.Add("KTB2BUCKLES", "2") 
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Override Script:  Added Part: KTB2BUCKLES=2", False, False)
        elif activeOptionCodes.Contains("KTB2S2B3"):
            if (PartNumbers.ContainsKey("KTB2BUCKLES") == False):
                PartNumbers.Add("KTB2BUCKLES", "3") 
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Override Script:  Added Part: KTB2BUCKLES=3", False, False)
        if activeOptionCodes.Contains("KTB3S3B1"):
            if (PartNumbers.ContainsKey("KTB3BUCKLES") == False):
                PartNumbers.Add("KTB3BUCKLES", "1") 
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Override Script:  Added Part: KTB3BUCKLES=1", False, False)
        elif activeOptionCodes.Contains("KTB3S3B2"):
            if (PartNumbers.ContainsKey("KTB3BUCKLES") == False):
                PartNumbers.Add("KTB3BUCKLES", "2") 
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Override Script:  Added Part: KTB3BUCKLES=2", False, False)
        elif activeOptionCodes.Contains("KTB3S3B3"):
            if (PartNumbers.ContainsKey("KTB3BUCKLES") == False):
                PartNumbers.Add("KTB3BUCKLES", "3") 
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Override Script:  Added Part: KTB3BUCKLES=3", False, False)


except Exception as inst:
    TPassLogger.Warn("Override Test Application Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Override Test Application Script:  Processing Failed.")
    isSuccess = False
    
TPassLogger.Info("Override Test Application Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 04202023
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################

