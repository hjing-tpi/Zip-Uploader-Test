#Parse Scanned part numbers and validate 
#
#TPass Objects Passed In/Returned
#   in - Function "TestAppLogger"
#   in - dictionary<string, string> "ScanData"
#   
#   out - string "FaultDetail" 
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

#########################################################################################################################################
# Application Engineer:  Specific constant variables to maintain
#
testApplicationScriptFileNameFrontLeft = "Vuteq SLP D2Ux-2 Door Pad LF.json"
testApplicationScriptFileNameFrontRight = "Vuteq SLP D2Ux-2 Door Pad RF.json"
optionCodeFileName = "Options.json"
leftPartNumbersFile = "C:\TPass\Support Files\LeftPartNumbers.txt"
rightPartNumbersFile = "C:\TPass\Support Files\RightPartNumbers.txt"
# Software Engineer Debug / Simulate
# ScanData["DOOR"] = "26558182-0000108"
##########################################################################################################################################

import clr
from System.IO import File
clr.AddReference("Tpi.TPass.Common")
from Tpi.TPass.Common.Business import ProductIdentification

version = "2.0"
production = False
FaultDetailText = ""
ScannedHarnessPartNumber = ""
ScannedDoorPartNumber = ""

# Internal Functions
def ValidateScan():
    global FaultDetailText
    global ScannedHarnessPartNumber
    global ScannedDoorPartNumber
    #Read Left part number file 
    try:
        partNumberLines = File.ReadAllLines(leftPartNumbersFile)
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Reading Part Number File - " + leftPartNumbersFile + "  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Vuteq Start Test Cycle Script:  Error Reading Part Number File - " + leftPartNumbersFile + "  File.ReadLines Exception Occurred :{0}", inst)
        FaultDetailText = "Error Reading Part Number File - " + leftPartNumbersFile
        return False
    try:
        for partNumberLine in partNumberLines: 
            if (partNumberLine and partNumberLine.isspace() == False):
                partNumberLine = partNumberLine.strip()
                partNumberFields = partNumberLine.split(";")
                if len(partNumberFields) >= 3:
                    harnessPartNumber = partNumberFields[0].Trim().ToUpper()
                    doorPanelPartNumbers = partNumberFields[2].Trim().ToUpper()
                    if (harnessPartNumber == ScannedHarnessPartNumber):
                        if doorPanelPartNumbers.find(ScannedDoorPartNumber) != -1:
                            MainTPassScripting.InterfaceUiLogger("Vuteq", "Valid Left Harness/Door Panel Part Number Combination.  Harness = " + ScannedHarnessPartNumber + ", Door Panel = " + ScannedDoorPartNumber, False, False)
                            FaultDetailText = "Valid Left Harness/Door Panel Part Number Combination.  Harness = " + ScannedHarnessPartNumber + ", Door Panel = " + ScannedDoorPartNumber
                            return True
                
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Processing Part Number File - " + leftPartNumbersFile + "  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Vuteq Start Test Cycle Script:  Error Processing Part Number File - " + leftPartNumbersFile + "  File.ReadLines Exception Occurred :{0}", inst)
        FaultDetailText = "Exception Processing Left Part Number File: " + str(inst)
        return False

    #Read Right part number file 
    try:
        partNumberLines = File.ReadAllLines(rightPartNumbersFile)
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Reading Part Number File - " + rightPartNumbersFile + "  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Vuteq Start Test Cycle Script:  Error Reading Part Number File - " + rightPartNumbersFile + "  File.ReadLines Exception Occurred :{0}", inst)
        FaultDetailText = "Error Reading Part Number File - " + rightPartNumbersFile
        return False
    try:
        for partNumberLine in partNumberLines: 
            if (partNumberLine and partNumberLine.isspace() == False):
                partNumberLine = partNumberLine.strip()
                partNumberFields = partNumberLine.split(";")
                if len(partNumberFields) >= 3:
                    harnessPartNumber = partNumberFields[0].Trim().ToUpper()
                    doorPanelPartNumbers = partNumberFields[2].Trim().ToUpper()
                    if (harnessPartNumber == ScannedHarnessPartNumber):
                        if doorPanelPartNumbers.find(ScannedDoorPartNumber) != -1:
                            MainTPassScripting.InterfaceUiLogger("Vuteq", "Valid Right Harness/Door Panel Part Number Combination.  Harness = " + ScannedHarnessPartNumber + ", Door Panel = " + ScannedDoorPartNumber, False, False)
                            FaultDetailText = "Valid Right Harness/Door Panel Part Number Combination.  Harness = " + ScannedHarnessPartNumber + ", Door Panel = " + ScannedDoorPartNumber
                            return True
                
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Processing Part Number File - " + rightPartNumbersFile + "  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Vuteq Start Test Cycle Script:  Error Processing Part Number File - " + rightPartNumbersFile + "  File.ReadLines Exception Occurred :{0}", inst)
        FaultDetailText = "Exception Processing Right Part Number File: " + str(inst)
        return False

    MainTPassScripting.InterfaceUiLogger("Vuteq", "Invalid Harness/Door Panel Part Number Combination.  Harness = " + ScannedHarnessPartNumber + ", Door Panel = " + ScannedDoorPartNumber, False, False)
    FaultDetailText = "Invalid Harness/Door Panel Part Number Combination.  Harness = " + ScannedHarnessPartNumber + ", Door Panel = " + ScannedDoorPartNumber
    return False
    
try:
    
    isSuccess = True
    TestAppLogger.Info("Scan Data Validation Python Script")
    TestAppLogger.Info("Scan Data Validation Python Script: Harness = " + ProductIdentification.Singleton.Instance.PrimaryId)
    TestAppLogger.Info("Scan Data Validation Python Script: Door Scan = " + ScanData["DOOR"])
    
    ScannedHarnessPartNumber = ProductIdentification.Singleton.Instance.PrimaryId
    TestAppLogger.Info("Scan Data Validation Python Script: Harness Part Number from Scan = " + ScannedHarnessPartNumber)
    ScannedDoorPartNumber = ScanData["DOOR"].Trim().ToUpper().Substring(0,8)
    TestAppLogger.Info("Scan Data Validation Python Script: Door Part Number from Scan = " + ScannedDoorPartNumber)

    if ValidateScan():
        isSuccess = True
    else:
        isSuccess = False
    FaultDetail = FaultDetailText
        
except Exception as inst:
    TestAppLogger.Warn("Scan Data Validation Python Script: Exception Occurred :{0}", inst)
    TestAppLogger.Warn("Scan Data Validation Python Script: Processing Failed.")
    isSuccess = False
TestAppLogger.Info("Scan Data Validation Python Script: Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 06192024
#	Version: 2.0
#	Change: Removed processing harness part number scan.  will just use the primary id instead
#	Date: 05012024
#	Version: 1.0
#	Change: Initial Version
############################################################