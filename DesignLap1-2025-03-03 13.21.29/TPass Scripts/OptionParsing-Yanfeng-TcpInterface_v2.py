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
#################################################################################################################################################################################################################
# Software Developer Comment Out When Done For Debugging Purposes
# from System.Collections.Generic import Dictionary, List

BuildData = "=SB0000241CZ0390006 231089511???????????000000180446ZE26       T20230328133433        428287038465381584653816428584024280931242809290********23366469843009448460788084939681851350298455353584710010----************4283124284787586428505292327629523276323846538242327632723276328135529678483869613552357427971414280929885534596****************13545621428497918457821342831095865389151354532613550912********----************849604082341292884825986----****84653822********LSY 2.0      ********23420285234202864280931084534437428092944280930384945238********4283335184626747----****8457821185644252846145478494637342786518428242898652909242809309----****4280930542809307********************************4283710242837104428095664283712842856151----****135527868559483884653821----****----****----**** 0ST 1NF 1SF 1SZ 2NF 2ST 3ST 4G7 4JF 4ST 5FC 5ST 6X1 7X1 8BA 9BA A2X A45 A7K AEF AEQ AF6 AHE AHH AJC AKE AKO AL0 AR9 AS1 AS2 ASV ATH AVK AVU AXG AXP AYR AYX B72 BB4 BTM BTV C25 C59 CE1 CJ2 CKK CTB D42 D75 DCP DD8 DYX EF7 ENL EPH F45 FAI FE9 FHB FJW FWD GGC GNA GNQ GNT HS1 HSP ISA IVD J24 J61 J71 JF5 JJ2 K6L KA1 KA6 KBC KI3 KL9 KRV KSG KU9 LHD LSY M3H MAH MFI MM1 N37 NAM NE8 NK4 NKC NKD NTB OAR PAN PAP PPW PXD QCS R6C R9N RSR SLM T4L T7E T8Z TB8 TC2 TDM TQ5 TSQ TTW TUJ U2K U5G UD7 UE1 UE4 UEU UFB UG1 UGC UGN UH5 UHG UJN UKI UKK UKM UKT UL5 UMN UOW UQG URB URT USS UST UUA UVX UVZ UXP V33 V8D VAB VDZ VGP VH9 VHM VRF VRG VRH VRJ VRK VRL VRM VRN VRR VT7 VTI VV4 WMY WPC XD7 XL8 XVR Y19                                                                                                                                                                                                                                                                                                                        ^^^"

# OptionCodesInBuildData = List[str]()
# PartNumbers = Dictionary[str, str]()

#################################################################################################################################################################################################################

#################################################################################################################################################################################################################

## Applications Engineer, Add and Modify when needed.

## PartMatrix Dictionary
PartMatrix = {}
## Please follow this Format
## PartMatrix["Name of Module"] = BuildData[Start Position - 1 : (Start Position - 1) + Length]
## To find the Start Position and Length please reference this Excel File Located here: Y:\Yanfeng\Riverside\IP Tester (MY24+)\Site Info\ULv2String.xlsx 
if len(BuildData) >= 1798:
    PartMatrix["CGM"] = BuildData[278 : 286]
    PartMatrix["SCL"] = BuildData[318 : 326]
    PartMatrix["Radio"] = BuildData[326 : 334]
    PartMatrix["HFPF"] = BuildData[587 : 595]
    PartMatrix["DMS"] = BuildData[771 : 779]
else:
    TPassLogger.Info("Option Parsing Script: Invalid Build Data Length")
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("TCPInterface", "Invalid Build Data Length", True, True)
    isSuccess = False

#################################################################################################################################################################################################################
## Note: This script specially requires the YanFeng-Translation.csv to be in the same directory as it, which is the TPass Scripts Folder
## This is does use an absolute path.

import re

production = False
version = "2.0"
primaryId = ""
secondaryId = ""
tertiaryId = ""
quaternaryId = ""
quinaryId = ""
isSuccess = True

## Logs and Adds each part
def LogAndAddPart(partName, partNumber):
    TPassLogger.Info("Option Parsing Script: Added Part ({0}) found in build data", partNumber)
    MainTPassScripting.InterfaceUiLogger("TCPInterface", "Option Parsing Script:   Added Configured Part - " + partName + " = " + partNumber, False, False)
    PartNumbers.Add(partName, partNumber)
    
## Main Execution Code
try:

    #Debug
    TPassLogger.Info("Option Parsing Script:  Product Build Data = {0}", BuildData)

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
        
        if len(BuildData) >= 1798:
            ## Add the PartNumbers based off what is in the PartMatrix
            for key in PartMatrix:
                if( "*" not in PartMatrix[key] and "-" not in PartMatrix[key] ):
                    LogAndAddPart(key, PartMatrix[key])
                
            # ## Sets the Primary Id , Secondary Id, Tertiary Id to the CSN, PVIF and VIN.
            primaryId = BuildData[10:20]
            secondaryId = BuildData[20:30]
            tertiaryId = BuildData[30:47]   
            
            ## Option Codes Get found and added starting here
            optionCodesString = BuildData[797:]
            optionCodes = optionCodesString.split()
            
            # ## Start adding all those option codes.         
            for optionCode in optionCodes:
                ## End delimter do not add.
                if(optionCode == "^^^"):
                    continue
                TPassLogger.Info(optionCode)
                OptionCodesInBuildData.Add(optionCode)
                MainTPassScripting.InterfaceUiLogger("TCPInterface", "Option Parsing Script:  Added Configured OptionCode - " + optionCode, False, False)
        else:
            TPassLogger.Info("Option Parsing Script: Invalid Build Data Length")
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            MainTPassScripting.InterfaceUiLogger("TCPInterface", "Invalid Build Data Length", True, True)
            isSuccess = False
            
except Exception as inst:
    TPassLogger.Warn("Option Parsing Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Parsing Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Parsing Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 09112023
#	Version: 2.0
#   Changed By: LM
#	Change: Changed to new YanFeng BuildData String Format. 
############################################################