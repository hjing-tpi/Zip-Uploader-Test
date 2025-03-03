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
version = "1.0"
primaryId = ""
secondaryId = ""
tertiaryId = ""
quaternaryId = ""
quinaryId = ""
isSuccess = True

optionInfo = Dictionary[str, list]()

#########################################################################################################################################
# Application Engineer:  Set Option number, Option Tag Name and Part Number Tag Name required for Test Application
#
#               #, OptionName, PartName
optionInfo.Add("1", ["ICS", "ICS"])
optionInfo.Add("2", ["DCSD", "DCSD"])
optionInfo.Add("3", ["TBM", "TBM"])
optionInfo.Add("4", ["IPC", "IPC"])
optionInfo.Add("5", ["SCCM", "SCCM"])
optionInfo.Add("6", ["HVAC", "HVAC"])
optionInfo.Add("7", ["SGW", "SGW"])
optionInfo.Add("8", ["NVPM", "NVPM"])
optionInfo.Add("9", ["DMSM", "DMSM"])
optionInfo.Add("10", ["ESL", "ESL"])
optionInfo.Add("11", ["RC3", "RC3"])
optionInfo.Add("12", ["RCJ", "RCJ"])
optionInfo.Add("13", ["RCAM", "RCAM"])
optionInfo.Add("14", ["RDK", "RDK"])
optionInfo.Add("15", ["RS9", "RS9"])
optionInfo.Add("16", ["JLP", "JLP"])
optionInfo.Add("17", ["SUB", "SUB"])
optionInfo.Add("18", ["PHEV", "PHEV"])
optionInfo.Add("19", ["CSWSM", "CSWSM"])
optionInfo.Add("20", ["NVPM", "NVPM"])
optionInfo.Add("21", ["BCIM", "BCIM"])
optionInfo.Add("22", ["JMPR", "JMPR"])
optionInfo.Add("23", ["PEM", "PEM"])
optionInfo.Add("24", ["CELL", "CELL"])
optionInfo.Add("25", ["RCG", "RCG"])
optionInfo.Add("26", ["RCJ", "RCJ"])
optionInfo.Add("27", ["RCA", "RCA"])
optionInfo.Add("28", ["FPDM", "FPDM"])
optionInfo.Add("29", ["CMCM", "CMCM"])
optionInfo.Add("30", ["LHD", "LHD"])
optionInfo.Add("31", ["RHD", "RHD"])
optionInfo.Add("32", ["LCJ", "LCJ"])
optionInfo.Add("33", ["LBZ", "LBZ"])
optionInfo.Add("34", ["HUD", "HUD"])
optionInfo.Add("35", ["PBS", "PBS"])
optionInfo.Add("36", ["PAB3", "PAB3"])
optionInfo.Add("37", ["INCAR", "INCAR"])
optionInfo.Add("38", ["ECALL", "ECALL"])
optionInfo.Add("39", ["AMFM", "AMFM"])
optionInfo.Add("40", ["FCAM", "FCAM"])
optionInfo.Add("41", ["JLN", "JLN"])
optionInfo.Add("42", ["RSD", "RSD"])
#
#########################################################################################################################################

try:

    #Debug
    #BuildData = "20201004520~1~MOD_CODE~68489381AB~ICS - Integrated Center Stack~M8100519^^^20201004520~2~MOD_CODE~68375145AD~DCSD - Disassociated Center Stac~M8100519^^^20201004520~3~MOD_CODE~68436288AB~TBM  - Telematics Box Module~M8100519^^^20201004520~4~MOD_CODE~68381139AH~IPC - Instrument Panel Cluster~M8100519^^^20201004520~5~MOD_CODE~68351728AD~SCCM - Steering Column Control M~M8100519^^^20201004520~6~MOD_CODE~68459039AE~HVAC - HVAC Module Black Box~M8100519^^^20201004520~7~MOD_CODE~68449275AA~SGW - Security Gateway Module~M8100519^^^20201004520~8~MOD_CODE~04672599AD~NVPM - Night Vision Processing M~M8100519^^^20201004520~9~MOD_CODE~NOPART~DMSM - Driver Monitoring System~M8100519^^^20201004520~10~MOD_CODE~NOPART~ESL - Electronic Steering Lock~M8100519^^^20201004520~11~MOD_CODE~NOPART~RC3 - Premium Speaker~M8100519^^^20201004520~12~MOD_CODE~NOPART~PURPLE RCJ - CMCM/ETM Purple Con~M8100519^^^20201004520~13~MOD_CODE~NOPART~RCAM - REAR CAMERA COAX~M8100519^^^20201004520~14~MOD_CODE~NOPART~FM2 - FM2 COAX~M8100519^^^20201004520~15~MOD_CODE~NOPART~DAB - DAB Coax to Radio~M8100519^^^20201004520~16~MOD_CODE~JLP~GPS2 - GPS to Body Coax~M8100519^^^20201004520~17~MOD_CODE~SUB~STEER - STEERING TILT & Telescop~M8100519^^^20201004520~18~MOD_CODE~NOPART~PHEV - DRIVER MODE SWITCH~M8100519^^^20201004520~19~MOD_CODE~68414987AD~CSWSM - Comfort Steering Wheel a~M8100519^^^20201004520~20~MOD_CODE~04672599AD~NVPM - Y1311A 6 Way Gray LVDS to~M8100519^^^20201004520~21~MOD_CODE~NOPART~BCIM - Battery  Charge Indicator~M8100519^^^20201004520~22~MOD_CODE~NOPART~JMPR - TBM Jumper Bracket~M8100519^^^20201004520~23~MOD_CODE~68509799AA~PEM - PASSIVE ENTRY MODULE~M8100519^^^20201004520~24~MOD_CODE~68436288AB~CELL -  CELL COAX~M8100519^^^20201004520~25~MOD_CODE~NOPART~RCG - RCG Speaker Configuration~M8100519^^^20201004520~26~MOD_CODE~NOPART~RCJ - RCJ Speaker Configuration~M8100519^^^20201004520~27~MOD_CODE~RCA~RCA - RCA Speaker Speaker Config~M8100519^^^20201004520~28~MOD_CODE~NOPART~FPDM - Front Passenger Display M~M8100519^^^20201004520~29~MOD_CODE~68426027AC~CMCM - CMCM Radio~M8100519^^^20201004520~30~PART~68376610AC~LHD - Left Hand Drive~M8100519^^^20201004520~31~PART~NOPART~RHD - Right Hand Drive~M8100519^^^20201004520~32~MOD_CODE~NOPART~WHITE - Spear Lamp No Lin~M8100519^^^20201004520~33~MOD_CODE~LBZ~RGB - Spear Lamp With Lin~M8100519^^^20201004520~34~MOD_CODE~68379061AB~HUD - Heads up Display~M8100519^^^20201004520~35~MOD_CODE~6XN031X7AB~PBS - Park Brake Switch~M8100519^^^20201004520~36~PART~68462716AD~PAB3 - Third Passenger Airbag~M8100519^^^20201004520~37~MOD_CODE~55111178AC~INCAR - In Car Temp Sensor~M8100519^^^20201004520~38~MOD_CODE~NOPART~ECALL - Ecall Speaker~M8100519^^^20201004520~39~MOD_CODE~68426027AC~AMFM - X1300A AM/FM Antenna~M8100519^^^20201004520~40~MOD_CODE~68467253AB~FCAM - Family Camera Coax~M8100519^^^20201004520~41~MOD_CODE~NOPART~GPS1 to TBM  (JLN)~M8100519^^^20201004520~42~MOD_CODE~NOPART~GPS2 - GPS to Body Coax(RSD)~M8100519^^^^^^"

    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    primaryId = "Unknown"
    if BuildData == "":
        if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.FileDrop):
            TPassLogger.Info("Option Parsing Script:  No Product Build Data")
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            MainTPassScripting.InterfaceUiLogger("SQLConnect", "Option Parsing Script:  Empty build data from file drop", True, True)
            isSuccess = False
        else:
            TPassLogger.Info("Option Parsing Script:  No Product Build Data")
            primaryId = RunTestCycleId

    else:
        optionRows = BuildData.split("^^^")
        for optionRow in optionRows:

            # Handle the last row which will be blank
            if optionRow == "":
                break

            rowFields = optionRow.split("~")
            if len(rowFields) != 6:
                TPassLogger.Error("Option Parsing Script:  Invalid data format from DB, must be 6 fields separated by the ~ delimiter. Data = {0}", optionRow)
                # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                MainTPassScripting.InterfaceUiLogger("SQLConnect", "Option Parsing Script:  Invalid data format from DB, must be 6 fields separated by the ~ delimiter. Data = " + optionRow, True, True)
                isSuccess = False
                break
            primaryId = rowFields[0]
            secondaryId = rowFields[5]
 
            if rowFields[3] != "NOPART":
            
                # Populate Option Codes found in broadcasted build data
                if optionInfo.ContainsKey(rowFields[1]):
                    optionName = optionInfo[rowFields[1]][0]
                    OptionCodesInBuildData.Add(optionName)
                    TPassLogger.Info("Option Parsing Script: Added Configured Option Code ({0}) found in build data", optionName)
                    MainTPassScripting.InterfaceUiLogger("SQLConnect", "Option Parsing Script:  Added Configured Option Code - " + optionName, False, False)

                    # Populate Part Numbers that are in the broadcasted Build Data
                    partName = optionInfo[rowFields[1]][1]
                    partNumber = rowFields[3]
                    if PartNumbers.ContainsKey(partName):
                        TPassLogger.Warn("Option Parsing Script: Part Tag ({0}, {1}) found twice in build data.  First occurrence will be used", partName, partNumber);
                        MainTPassScripting.InterfaceUiLogger("SQLConnect", "Option Parsing Script:  Part Tag found twice in the build data.  First occurrence will be used - " + partName + " = " + partNumber, True, False)
                    else:
                        TPassLogger.Info("Option Parsing Script: Added Part ({0}, {1}) found in build data", partName, partNumber);
                        PartNumbers.Add(partName, partNumber)                
                        MainTPassScripting.InterfaceUiLogger("SQLConnect", "Option Parsing Script:  Added Configured Part - " + partName + " = " + partNumber, False, False)

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
#	Date: 10062021
#	Version: 1.0
#	Change: Initial Version
############################################################

