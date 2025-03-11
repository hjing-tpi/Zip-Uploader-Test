#Main Button Triggered Script
#This Script can run any python logic and can also run a TPass Test Application
#TPass Objects Passed In/Returned
#   in  - object MainTPassScripting - Exposed all methods and properties for the scripts to use
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

import clr
from System.IO import File
from System import DateTime
version = "1.0"
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
    global keyPadData
    
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
                    if keyPadData.find(currentPartNumber) != -1:
                        partNumberFound = currentPartNumber
                        testApplicationScriptFileName = testApplicationScriptFileNameFrontLeft
                        MainTPassScripting.InterfaceUiLogger("Vuteq", "Front Part Number found - " + partNumberFound, False, False)
                        if len(partNumberFields) > 1:
                            optionsFound = partNumberFields[1].Trim().ToUpper()
                            MainTPassScripting.InterfaceUiLogger("Vuteq", "Front Part Number Options found - " + optionsFound, False, False)
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
                    if keyPadData.find(currentPartNumber) != -1:
                        partNumberFound = currentPartNumber
                        testApplicationScriptFileName = testApplicationScriptFileNameFrontRight
                        MainTPassScripting.InterfaceUiLogger("Vuteq", "Rear Part Number found - " + partNumberFound, False, False)
                        if len(partNumberFields) > 1:
                            optionsFound = partNumberFields[1].Trim().ToUpper()
                            MainTPassScripting.InterfaceUiLogger("Vuteq", "Rear Part Number Options found - " + optionsFound, False, False)
                        return True
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Processing Part Number File - " + rightPartNumbersFile + "  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Vuteq Start Test Cycle Script:  Error Processing Part Number File - " + rightPartNumbersFile + "  File.ReadLines Exception Occurred :{0}", inst)
        return False
         
    return False


try:

    TPassLogger.Debug("Main Button Script: Run a Test Application")
    keyPadData = MainTPassScripting.GetInputKeyPad("Enter Part Number")
    if keyPadData != "":
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Keypad Data = " + keyPadData, False, False)
        traceId = ""

        #determine if part number in the scan is a Front or Rear 
        if GetPartNumber() == True:
            runTestCycleId = partNumberFound + ";" + traceId + ";" + optionsFound
            # RunTestCycle(string testApplicationScriptFileName, string optionCodeFileName, string runTestCycleId, bool useDefaultOptionCodesOnly = false, bool processTestResults = true, bool useCurrentProductIdentification = false, bool bypassOverrideTestAppScript = false)
            if MainTPassScripting.RunTestCycle(testApplicationScriptFileName, optionCodeFileName, runTestCycleId):
                isSuccess = True
            else:
                isSuccess = False
                TPassLogger.Warn("Main Button Script:  Error Running Test Cycle")
        else:
            isSuccess = False
            MainTPassScripting.InterfaceUiLogger("Vuteq", "Part Number entered not found in part number files: " + keyPadData, True, True)
            TPassLogger.Error("Main Button Script:  Error Running Test Cycle because Part Number not found")
    else:
        isSuccess = True
        TPassLogger.Info("GetInputKeyPad() No Job Entered by Operator")


except Exception as inst:
    TPassLogger.Warn("Main Button Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Main Button Script:  Processing Failed.")
    isSuccess = False

TPassLogger.Info("Main Button Script:  Is Success = {0}", isSuccess)


############################################################
# Change History
############################################################
#   Date: 02172023
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################


