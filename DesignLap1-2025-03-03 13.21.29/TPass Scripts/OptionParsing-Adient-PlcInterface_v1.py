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

from System.Collections.Generic import Dictionary, List

production = False
version = "1.0"
primaryId = ""
secondaryId = ""
tertiaryId = ""
quaternaryId = ""
quinaryId = ""
isSuccess = True

broadcastCode = ""

optionInfo = Dictionary[str, list]()

#########################################################################################################################################
# Application Engineer:  Set Option number, Option Tag Name and Part Number Tag Name required for Test Application
#
#               #Key        #Value1   #Value2    
optionInfo.Add("CONNECT", ["CONNECT", "CONNECT"])
optionInfo.Add("DISCONNECT", ["DISCONNECT", "DISCONNECT"])
optionInfo.Add("LASER", ["LASER", "LASER"])
optionInfo.Add("C", ["CAMRY", "CAMRY"])
## Note: Special Case, due to the usage of L and R both being used to key into whether the
## seat driver or passenger and the car's model, we will reserve the index of 1 here to reference Passenger or Driver. 
## The 0th index will be used for the car's model.
optionInfo.Add("A", ["AIRBAG", "AIRBAG"])
optionInfo.Add("R", ["RAV4", "PASSENGER"])  
optionInfo.Add("L", ["LEXUS", "DRIVER"])
################################################################################################
optionInfo.Add("INIT", ["INIT", "MEMORY INIT"])
optionInfo.Add("010B", ["010B", "010B"])
optionInfo.Add("POWER", ["POWER", "POWER"])
optionInfo.Add("MANUAL", ["MANUAL", "MANUAL"])
optionInfo.Add("BUCKLE", ["BUCKLE", "BUCKLE"])
optionInfo.Add("HEAT", ["HEAT", "HEAT"])
optionInfo.Add("CH060", ["CH060", "MANUAL SEAT"])
optionInfo.Add("CH06M", ["CH06M", "MANUAL SEAT"])
optionInfo.Add("CH06P", ["CH06P", "POWER DRIVER ONLY"])
optionInfo.Add("CH06B", ["CH06B", "POWER BOTH"])
optionInfo.Add("CH061", ["CH061", "POWER WITH CLA"])
optionInfo.Add("CH068", ["CH068", "POWER WITH 2LUM"])
optionInfo.Add("CH07H", ["CH07H", "HEATED"])
optionInfo.Add("CH07F", ["CH07F", "HEATED"])
optionInfo.Add("CH07V", ["CH07V", "VENTED SEAT"])
optionInfo.Add("CH07X", ["CH07X", "HEAT-VENT"])
optionInfo.Add("CH07L", ["CH07L", "LOW LEVEL HEAT"])
optionInfo.Add("M", ["MEMORY", "MEMORY"])
optionInfo.Add("D", ["MEMORY", "MEMORY"])
optionInfo.Add("CH12Y", ["CH12Y", "2W DRIVER LUMBAR"])
optionInfo.Add("CH12B", ["CH12B", "2W BOTH LUMBAR"])
optionInfo.Add("CH12P", ["CH12P", "4/2WAY LUMBAR"])
optionInfo.Add("CH12D", ["CH12D", "4WAY DRIVER LUMBAR"])
optionInfo.Add("CH125", ["CH125", "CH125"])
optionInfo.Add("LTH", ["LTH", "LTH"])
optionInfo.Add("FAB", ["FAB", "FAB"])
optionInfo.Add("HYB", ["HYB", "HYB"])
optionInfo.Add("STD", ["STD", "STD"])
optionInfo.Add("PRM", ["PRM", "PRM"])
optionInfo.Add("FHV", ["FHV", "FHV"])
optionInfo.Add("LWR", ["LWR", "LWR"])
optionInfo.Add("RSH", ["RSH", "RSH"])
optionInfo.Add("23", ["2023", "2023"])
optionInfo.Add("24", ["2024", "2024"])
optionInfo.Add("25", ["2025", "2025"])
optionInfo.Add("26", ["2026", "2026"])
optionInfo.Add("27", ["2027", "2027"])
optionInfo.Add("28", ["2028", "2028"])
optionInfo.Add("A15", ["A15", "A15"])
optionInfo.Add("C14", ["C14", "C14"])
optionInfo.Add("C17", ["C17", "C17"])


#
#########################################################################################################################################
#########################################################################################################################################
# Software Engineer Debugging 
# from System.Collections.Generic import List
# BuildData = """1\nSA12937182~A211RBXMDL2SA0MNYLTHE~0979~~070623~0003210153~RZPX6T"""
# OptionCodesInBuildData = List[str]()
# PartNumbers = Dictionary[str,str]()

#########################################################################################################################################

## OptionKey -- Key value of the optionInfo Dictionary
## OptionIndex -- Index of the list attached to the Dictionary
def AddOptionCode(optionKey, optionIndex):
    if optionInfo.ContainsKey(optionKey):
        optionName = optionInfo[optionKey][optionIndex]
        OptionCodesInBuildData.Add(optionName)
        TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
        MainTPassScripting.InterfaceUiLogger("PLCInterface", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)
        
def LoopLogger(optionCodeList):
    for optionName in optionCodeList:
        TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
        MainTPassScripting.InterfaceUiLogger("PLCInterface", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)

try:

    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    primaryId = "Unknown"
    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ManualEntry):
        TPassLogger.Info("Option Parsing Script:  No Product Build Data")
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        isSuccess = True
    else:
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
            optionRows = BuildData.splitlines()
            
            if len(optionRows) > 0:
                ## Parsing of the data fields into lists
                rowFields = optionRows[1].split("~")
                
                # ## Applying fields to TPass Ids
                primaryId = rowFields[0]
                ## Build Code
                secondaryId = rowFields[1]
                ## Recipe Number
                tertiaryId = optionRows[0] 
                quaternaryId = rowFields[2]
                quinaryId = rowFields[4]
                broadcastCode = rowFields[5]
                
                # Handling of Unknown Option Codes.
                if secondaryId[0:3] == "A15":
                    optionkey = secondaryId[0:3]
                    AddOptionCode(optionkey, 0)
                elif secondaryId[0:3] == "C14":
                    optionkey = secondaryId[0:3]
                    AddOptionCode(optionkey, 0)
                elif secondaryId[0:3] == "A17":
                    optionkey = secondaryId[0:3]
                    AddOptionCode(optionkey, 0)
                    
                # Adding of vehicle models.
                if secondaryId[0] == "A":
                    optionKey = secondaryId[0]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[0] == "C":
                    optionKey = secondaryId[0]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[0] == "R":
                    optionKey = secondaryId[0]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[0] == "L":
                    optionKey = secondaryId[0]
                    AddOptionCode(optionKey, 0)
                
                ## Model Year
                if secondaryId[1:3] == "23":
                    optionKey = secondaryId[1:3]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[1:3] == "24":
                    optionKey = secondaryId[1:3]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[1:3] == "25":
                    optionKey = secondaryId[1:3]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[1:3] == "26":
                    optionKey = secondaryId[1:3]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[1:3] == "27":
                    optionKey = secondaryId[1:3]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[1:3] == "28":
                    optionKey = secondaryId[1:3]
                    AddOptionCode(optionKey, 0)
                    
                ## Seat Type: Driver or Passenger
                if secondaryId[4] == "L":
                    optionKey = secondaryId[4]
                    AddOptionCode(optionKey, 1)
                elif secondaryId[4] == "R":
                    optionKey = secondaryId[4]
                    AddOptionCode(optionKey, 1)
                
                ## Power/Manual track
                if optionInfo.ContainsKey ( "CH06" + secondaryId[5] ):
                    optionName = optionInfo["CH06" + secondaryId[5]][0]
                    OptionCodesInBuildData.Add(optionName)
                    TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
                    MainTPassScripting.InterfaceUiLogger("PLCInterface", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)
                
                ## Heated/Cooled Seat or not
                if optionInfo.ContainsKey( "CH07" + secondaryId[6] ):
                    optionName = optionInfo["CH07" + secondaryId[6]][0]
                    OptionCodesInBuildData.Add(optionName)
                    TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
                    MainTPassScripting.InterfaceUiLogger("PLCInterface", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)
                
                ## Decides if we add Memory or not
                if secondaryId[7] == "M":
                    optionKey = secondaryId[7]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[7] == "D":
                    optionKey = secondaryId[7]
                    AddOptionCode(optionKey, 0)
                    
                ## Airbag is added or, could be deprecated due to airbag always being tested    
                if secondaryId[8] == "A":
                    optionKey = secondaryId[8]
                    AddOptionCode(optionKey, 1)
                
                ## Lumbar Option Parsing
                if optionInfo.ContainsKey( "CH12" + secondaryId[11] ):
                    optionName = optionInfo["CH12" + secondaryId[11]][0]
                    OptionCodesInBuildData.Add(optionName)
                    TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
                    MainTPassScripting.InterfaceUiLogger("PLCInterface", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)
                
                ## Trim Code
                if secondaryId[17:20] == "LTH":
                    optionKey = secondaryId[17:20]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[17:20] == "FAB":
                    optionKey = secondaryId[17:20]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[17:20] == "HYB":
                    optionKey = secondaryId[17:20]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[17:20] == "STD":
                    optionKey = secondaryId[17:20]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[17:20] == "PRM":
                    optionKey = secondaryId[17:20]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[17:20] == "FHV":
                    optionKey = secondaryId[17:20]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[17:20] == "LWR":
                    optionKey = secondaryId[17:20]
                    AddOptionCode(optionKey, 0)
                elif secondaryId[17:20] == "RSH":
                    optionKey = secondaryId[17:20]
                    AddOptionCode(optionKey, 0)
                    
                ##Recipe Number
                if tertiaryId == "1" and tertiaryId != "":
                    rcpCodes = List[str](["RANGE_OF_MOTION","AIRBAG","SPS","BUCKLE","SHORT_TO_GROUND","SHIP_POSITION"])
                    OptionCodesInBuildData.AddRange(rcpCodes)
                    LoopLogger(rcpCodes)
                elif tertiaryId == "2" and tertiaryId != "":
                    rcpCodes = List[str](["RANGE_OF_MOTION","AIRBAG","SPS","BUCKLE","HEAT","SHORT_TO_GROUND","SHIP_POSITION"])
                    OptionCodesInBuildData.AddRange(rcpCodes)
                    LoopLogger(rcpCodes)
                elif tertiaryId == "3" and tertiaryId != "":
                    rcpCodes = List[str](["RANGE_OF_MOTION","MOTOR_DRAW","AIRBAG","SPS","BUCKLE","SHORT_TO_GROUND","SHIP_POSITION"])
                    OptionCodesInBuildData.AddRange(rcpCodes)
                    LoopLogger(rcpCodes)
                elif tertiaryId == "4" and tertiaryId != "":
                    rcpCodes = List[str](["RANGE_OF_MOTION","MOTOR_DRAW","AIRBAG","SPS","BUCKLE","HEAT","SHORT_TO_GROUND","SHIP_POSITION"])
                    OptionCodesInBuildData.AddRange(rcpCodes)
                    LoopLogger(rcpCodes)
                elif tertiaryId == "5" and tertiaryId != "":
                    rcpCodes = List[str](["RANGE_OF_MOTION","AIRBAG","BUCKLE","SHORT_TO_GROUND","SHIP_POSITION"])
                    OptionCodesInBuildData.AddRange(rcpCodes)
                    LoopLogger(rcpCodes)
                elif tertiaryId == "6" and tertiaryId != "":
                    rcpCodes = List[str](["RANGE_OF_MOTION","AIRBAG","BUCKLE","HEAT","SHORT_TO_GROUND","SHIP_POSITION"])
                    OptionCodesInBuildData.AddRange(rcpCodes)
                    LoopLogger(rcpCodes)
                elif tertiaryId == "7" and tertiaryId != "":
                    rcpCodes = List[str](["RANGE_OF_MOTION","MOTOR_DRAW","AIRBAG","BUCKLE","HEAT","SHORT_TO_GROUND","SHIP_POSITION"])
                    OptionCodesInBuildData.AddRange(rcpCodes)
                    LoopLogger(rcpCodes)
                    
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
#	Date: 07112023
#	Version: 1.0
#	Change: Initial Version
#   Changed By: LM
############################################################

