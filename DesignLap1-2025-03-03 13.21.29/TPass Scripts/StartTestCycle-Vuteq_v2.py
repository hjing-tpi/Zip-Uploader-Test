# Process Product Input Data sent to TPass, either by Scanner, File Drop, Serial etc.
# This Script is expected to call RunTestCycle() passing in the appropriate parameters and setting the out parameters below
#
# TPass Objects Passed In and expected Returned
#   in  - string "StartCycleInputData" - This is the data that triggered this script by either a bar code scan, file drop, etc...
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application Detail log file
#   in  - object "SystemConfigurationValue" - This is the object to get values set in the System Configuration file
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

import clr
from System.IO import File
from System import DateTime

version = "2.0"
production = False

#########################################################################################################################################
# Application Engineer:  Specific constant variables to maintain
#
testApplicationScriptFileNameFrontLeft = "Vuteq SLP D2Ux-2 Door Pad LF.json"
testApplicationScriptFileNameFrontRight = "Vuteq SLP D2Ux-2 Door Pad RF.json"
optionCodeFileName = "Options.json"
leftPartNumbersFile = "C:\TPass\Support Files\LeftPartNumbers.txt"
rightPartNumbersFile = "C:\TPass\Support Files\RightPartNumbers.txt"
#
#########################################################################################################################################

partNumberFound = ""
optionsFound = ""
testApplicationScriptFileName = ""

# Internal Functions
def GetPartNumber():
    global partNumberFound
    global optionsFound
    global testApplicationScriptFileName
    global testApplicationScriptFileNameFrontLeft
    global testApplicationScriptFileNameFrontRight
    
    #Read Front part number file 
    try:
        partNumberLines = File.ReadAllLines(leftPartNumbersFile)
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Reading Part Number File - " + leftPartNumbersFile + "  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Vuteq Start Test Cycle Script:  Error Reading Part Number File - " + leftPartNumbersFile + "  File.ReadLines Exception Occurred :{0}", inst)
        return False
    try:
        for partNumberLine in partNumberLines: 
            if (partNumberLine and partNumberLine.isspace() == False):
                partNumberLine = partNumberLine.strip()
                partNumberFields = partNumberLine.split(";")
                if len(partNumberFields) > 0:
                    currentPartNumber = partNumberFields[0]
                    if StartCycleInputData.find(currentPartNumber) != -1:
                        partNumberFound = currentPartNumber
                        testApplicationScriptFileName = testApplicationScriptFileNameFrontLeft
                        MainTPassScripting.InterfaceUiLogger("Vuteq", "Front Part Number found in Scan - " + partNumberFound, False, False)
                        if len(partNumberFields) > 1:
                            optionsFound = partNumberFields[1].Trim().ToUpper()
                            MainTPassScripting.InterfaceUiLogger("Vuteq", "Front Part Number Options found in Scan - " + optionsFound, False, False)
                        return True
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Processing Part Number File - " + leftPartNumbersFile + "  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Vuteq Start Test Cycle Script:  Error Processing Part Number File - " + leftPartNumbersFile + "  File.ReadLines Exception Occurred :{0}", inst)
        return False

   #Read Rear part number file 
    try:
        partNumberLines = File.ReadAllLines(rightPartNumbersFile)
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Reading Part Number File - " + rightPartNumbersFile + "  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Vuteq Start Test Cycle Script:  Error Reading Part Number File - " + rightPartNumbersFile + "  File.ReadLines Exception Occurred :{0}", inst)
        return False
    try:
        for partNumberLine in partNumberLines: 
            if (partNumberLine and partNumberLine.isspace() == False):
                partNumberLine = partNumberLine.strip()
                partNumberFields = partNumberLine.split(";")
                if len(partNumberFields) > 0:
                    currentPartNumber = partNumberFields[0]
                    if StartCycleInputData.find(currentPartNumber) != -1:
                        partNumberFound = currentPartNumber
                        testApplicationScriptFileName = testApplicationScriptFileNameFrontRight
                        MainTPassScripting.InterfaceUiLogger("Vuteq", "Rear Part Number found in Scan - " + partNumberFound, False, False)
                        if len(partNumberFields) > 1:
                            optionsFound = partNumberFields[1].Trim().ToUpper()
                            MainTPassScripting.InterfaceUiLogger("Vuteq", "Rear Part Number Options found in Scan - " + optionsFound, False, False)
                        return True
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Processing Part Number File - " + rightPartNumbersFile + "  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Vuteq Start Test Cycle Script:  Error Processing Part Number File - " + rightPartNumbersFile + "  File.ReadLines Exception Occurred :{0}", inst)
        return False
         
    return False

#Debug
#StartCycleInputData = "[)>06Y4321000000000XP8514909912V247641970T4D21165124137348"
try:

    TPassLogger.Debug("Start Test Cycle Script:  Product Input Data = {0}", StartCycleInputData)
    TPassLogger.Debug("Start Test Cycle Script: Request and processing build data, run a Test Application and process the results")
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("Vuteq", "Scan Data = " + StartCycleInputData, False, False)

    # If required to parse the StartCycleInputData differently based on what input type triggered the script to run (Scan, Manual Entry, File Drop, Serial...)
    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Scan):
        TPassLogger.Debug("StartTestCycle - Trigger Type is Scan")
    elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ManualEntry):
        TPassLogger.Debug("StartTestCycle - Trigger Type is ManualEntry")
    elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.FileDrop):
        TPassLogger.Debug("StartTestCycle - Trigger Type is FileDrop")
    elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Udp):
        TPassLogger.Debug("StartTestCycle - Trigger Type is UDP")

    # If required, parse the StartCycleInputData and pass in to the RunTestCycle() method.  This data will be used by the Request Script for build data retrieval
    try:
        traceId = StartCycleInputData[47:63]
    except Exception as inst:
        traceId = ""
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Trace ID not in Scan at offset 47", True, True)

    #determine if part number in the scan is a Front or Rear 
    if GetPartNumber() == True:
        runTestCycleId = partNumberFound + ";" + traceId + ";" + optionsFound
        # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true, bool useCurrentProductIdentification = false, bool bypassOverrideTestAppScript = false)
        if MainTPassScripting.RunTestCycle(testApplicationScriptFileName, optionCodeFileName, runTestCycleId):
            isSuccess = True
        else:
            isSuccess = False
            TPassLogger.Warn("Start Test Cycle Script:  Error Running Test Cycle")
    else:
        isSuccess = False
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Part Number not found in Scan data", True, True)
        TPassLogger.Error("Start Test Cycle Script:  Error Running Test Cycle because Part Number not found")


except Exception as inst:
    TPassLogger.Warn("Start Test Cycle Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Start Test Cycle Script:  Processing Failed.")
    isSuccess = False

TPassLogger.Info("Start Test Cycle Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 02172023
#   Version: 2.0
#   ChangeBy: RMM
#   Change: Added options to the part number files to be parsed
#   Date: 10252022
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################
