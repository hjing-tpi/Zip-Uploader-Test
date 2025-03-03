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

from System.IO import File
from System.Collections.Generic import Dictionary

production = False
version = "1.0"
primaryId = ""
secondaryId = ""
tertiaryId = ""
quaternaryId = ""
quinaryId = ""
isSuccess = True


#########################################################################################################################################
# Application Engineer:  
#
#
partNumberFile = "C:\TPass\Data Incoming\PartNumbers.txt"

#########################################################################################################################################

try:

    #Debug
    #BuildData = "070NMPJ50387971AAHAHMAPABABBCSBGGBHCBNBBNGBNPBNSBNTBRFCDPCDWCFNCGDCGNCGUCGYCG3CG6CHKCJ1CJ2CKKCKNCKTCK6CLECM6CSHCSMCSNCSRCSWCUNCU7CVBCGYCUNDBADFHDHDDMEDBAEDEGNCGXWGX4HAFJHBJKVJLPJPMLAZLBCLMGNHSRCGRDGRSDRTFXAKXBMXGAXGDXHZX83YAA"
    #partNumbers = "6WJ38DX9AJCLUST,0000000000HFM  ,68446608ACHVAC ,0000000000RADIO,6XC76LXHABSCCM  ,68497538AFBCM  ,0000000000SCL_PN,56029921AFTBM_PN,68512086AASGW_PN,68458795AFBLACKBOX,0000000000ICS  ,68441666AECPVM_PN,0000000000DISPLAY_PN"
    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    primaryId = RunTestCycleId

    if BuildData == "":
        TPassLogger.Info("Option Parsing Script:  No Product Build Data")
        primaryId = RunTestCycleId
    else:
        # Process part numbers
        #6WJ38DX9AJCLUST,0000000000HFM  ,68446608ACHVAC ,0000000000RADIO,6XC76LXHABSCCM  ,68497538AFBCM  ,0000000000SCL_PN,56029921AFTBM_PN,68512086AASGW_PN,68458795AFBLACKBOX,0000000000ICS  ,68441666AECPVM_PN,0000000000DISPLAY_PN
        if File.Exists(partNumberFile):
            MainTPassScripting.InterfaceUiLogger("Blade", "Part Number File Received - " + partNumberFile, False, False)

            #Read contents and delete file
            partNumbers = File.ReadAllText(partNumberFile)
            MainTPassScripting.InterfaceUiLogger("Blade", "Part Numbers Received - " + partNumbers, False, False)

            parts = partNumbers.split(",")
            for part in parts:
                    if len(part) < 11:
                        TPassLogger.Warn("Option Parsing Script: Part field not at least 11 characters log and will be discarded - {0}", part);
                        MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Part field not at least 11 characters log and will be discarded - " + part, True, False)
                        continue
                    part = part.replace(' ', '')
                    partNumber = part[:10]
                    partName = part[10:]
                    if PartNumbers.ContainsKey(partName):
                        TPassLogger.Warn("Option Parsing Script: Part Tag ({0}, {1}) found twice in build data.  First occurrence will be used", partName, partNumber);
                        MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Part Tag found twice in the build data.  First occurrence will be used - " + partName + " = " + partNumber, True, False)
                    else:
                        TPassLogger.Info("Option Parsing Script: Added Part ({0}, {1}) found in build data", partName, partNumber);
                        PartNumbers.Add(partName, partNumber)                
                        MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Part - " + partName + " = " + partNumber, False, False)
            try:
                File.Delete(partNumberFile)
            except Exception as inst:
                TPassLogger.Debug("Option Retrieval Script:  File.Delete Exception Occurred :{0}", inst)            
        
        optionCount = int(BuildData[:3])
        secondaryId = BuildData[3:15]   #model
        options = BuildData[15:]

        if secondaryId[0:1] == 'N':
            OptionCodesInBuildData.Add("2022")
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", "2022")
            MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Option Code - " + "2022", False, False)
        if secondaryId[0:1] == 'P':
            OptionCodesInBuildData.Add("2023")
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", "2023")
            MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Option Code - " + "2023", False, False)
        if secondaryId[0:1] == 'R':
            OptionCodesInBuildData.Add("2024")
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", "2024")
            MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Option Code - " + "2024", False, False)
        if secondaryId[0:1] == 'S':
            OptionCodesInBuildData.Add("2025")
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", "2025")
            MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Option Code - " + "2025", False, False)
        if secondaryId[0:1] == 'T':
            OptionCodesInBuildData.Add("2026")
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", "2026")
            MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Option Code - " + "2026", False, False)
        if secondaryId[0:1] == 'V':
            OptionCodesInBuildData.Add("2027")
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", "2027")
            MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Option Code - " + "2027", False, False)
        if secondaryId[0:1] == 'W':
            OptionCodesInBuildData.Add("2028")
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", "2028")
            MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Option Code - " + "2028", False, False)
        if secondaryId[0:1] == 'X':
            OptionCodesInBuildData.Add("2029")
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", "2029")
            MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Option Code - " + "2029", False, False)

        #070NMPJ50387971AAHAHMAPABABBCSBGGBHCBNBBNGBNPBNSBNTBRFCDPCDWCFNCGDCGNCGUCGYCG3CG6CHKCJ1CJ2CKKCKNCKTCK6CLECM6CSHCSMCSNCSRCSWCUNCU7CVBCGYCUNDBADFHDHDDMEDBAEDEGNCGXWGX4HAFJHBJKVJLPJPMLAZLBCLMGNHSRCGRDGRSDRTFXAKXBMXGAXGDXHZX83YAA
        
        index = 0
        while index < optionCount*3:
            # Populate Option Codes found in broadcasted build data
            optionName = options[index:index+3]
            OptionCodesInBuildData.Add(optionName)
            TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
            MainTPassScripting.InterfaceUiLogger("Blade", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)
            index += 3
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
#	Date: 09182023
#	Version: 1.0
#	Change: Initial Version
############################################################

