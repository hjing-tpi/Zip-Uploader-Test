#Format and return the Printed Label Text for TPass to send to a printer
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - object "testAppResults"
#   in  - object "productIdentification"
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application Detail log file
#   in  - object "SystemConfigurationValue" - This is the object to get values set in the System Configuration file
#   out - string "printedLabelText" - TPass will send this text to the default printer if the string is not blank and if the printer is enabled in the TPass system configuration settings
#   out - bool "isSuccess" - Set to True if Test Results processing was successful.  Otherwise False
#   out - bool "production"
#   out - string "version"
#

import clr
clr.AddReferenceToFileAndPath('.\\Tpi.TPass.Common.dll')
from Tpi.TPass.Common.JsonStore import TestResults
from System.Text.RegularExpressions import Regex
from System.IO import Directory
from System.IO import File
from System import DateTime

version = "1.0"
production = False
TPassLogger.Debug("Test Results Processing Script:  Product Primary Id = {0}", productIdentification.PrimaryId)
TPassLogger.Debug("Test Results Processing Script:  Product Secondary Id = {0}", productIdentification.SecondaryId)
isSuccess = True

#########################################################################################################################################
# Application Engineer:  Set Station Number to be written to the printed label
#
maxNumberFaultsOnPrintedLabel = 10
printPassLabel = False
resultsFileFolder = "C:\\CTester History\\"

#
#########################################################################################################################################

overallTestResultsPass = False
printedFaultText = ""
screenLabelFaultText = ""
numberFaultsAdded = 0
totalNumberOfFaults = 0
testerId = "0"                                      # Will be read from the \TPass\Support Files\SID.txt file
testerIdFile = "C:\TPass\Support Files\SID.txt"

# Internal Functions
def IsTestFailed(testResults):

    if (testResults == str(TestResults.Fail) or testResults == str(TestResults.FatalFail) or
            testResults == str(TestResults.OperatorFail) or testResults == str(TestResults.OperatorAbort) or testResults == str(TestResults.SystemError)):
        return True
    else:
        return False

def SetFault(faultId, faultDescription):
    global totalNumberOfFaults
    global printedFaultText
    global screenLabelFaultText
    global maxNumberFaultsOnPrintedLabel
    global numberFaultsAdded
    try:
        totalNumberOfFaults += 1
        screenLabelFaultText = screenLabelFaultText + faultDescription + "\r\n"
        if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
            numberFaultsAdded = numberFaultsAdded + 1
            printedFaultText = printedFaultText + faultDescription + "\r\n"
    except:
        TPassLogger.Warn("Test Results Processing Script:  Fault Invalid and not saved.  Fault = {0}", faultDescription)
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Fault Invalid and not saved.  Fault = " + faultDescription, True, True)

def SetProcessData(reportId, reportData):
    global processResultsText
    if (reportId and reportData):
        # Saving Process Data is not implemented for Vuteq
        processResultsText = ""



# Main Logic
try:
    # Read testerId from file
    try:
        testerIdLines = File.ReadAllLines(testerIdFile)
        testerId = testerIdLines[0]
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Test Results Processing Script:  Error Reading Test ID File, will default to Tester ID = 0.  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Results Processing Script:  Error Reading Test ID File, will default to Tester ID = 0.  File.ReadLines Exception Occurred :{0}", inst)            

    printedLabelText = str(DateTime.Now) + "\r\n"
    printedLabelText = printedLabelText + "Tool ID:" + testerId + " Part Number:" + productIdentification.PrimaryId + " Trace ID:" + productIdentification.SecondaryId + "\r\n"
    screenLabelText = str(DateTime.Now) + "\r\n"
    screenLabelText = screenLabelText + "Tool ID:" + testerId + "    " + " Part Number:<b>" + productIdentification.PrimaryId + "</b>    " + "Trace ID:<b>" + productIdentification.SecondaryId + "</b>    \r\n"

    if (str(testAppResults.MainTestApplication.TestCycleResults.TestResults) == str(TestResults.Fail)):
        overallTestResultsPass = False
        printedLabelText = printedLabelText + "Test Status: Failed" + "\r\n"
    else:
        printedLabelText = printedLabelText + "Test Status: Passed" + "\r\n"
        overallTestResultsPass = True

    if (testAppResults.MainTestApplication.TestCycleResults.Abort):
        #gmEdiBuildResultsRecord.HrSetAbortedFlag(ord('A'))
        #MainTPassScripting.InterfaceUiLogger("Vuteq", "HrSetAbortedFlag() value = A", False, False)
        SetFault("08495", "TEST ABORTED")


    # Set Faults and User Values
    for groupInx in range(len(testAppResults.MainTestApplication.TestCycle)):
        for subGroupInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx])):
            for testInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps)):
                testStep = testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps[testInx]
                if (IsTestFailed(str(testStep.TestStepResults.TestResults))):
                    SetFault(testStep.Fault.Id, testStep.Fault.Description)

                # Test Step Specific Faults and Process data
                if (testStep.Name == "VoltageRange"):
                    for voltageRange in testStep.VoltageRanges:
                        for limit in voltageRange.Limits:
                            if (IsTestFailed(str(limit.TestStepResults.TestResults))):
                                SetFault(limit.Fault.Id, limit.Fault.Description)

                            if (str(limit.TestStepResults.TestResults) != str(TestResults.NotTested) and str(limit.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                                SetProcessData(limit.TestDataReporting.UpperLimitVolts, str(limit.UpperLimitVolts*100))
                                SetProcessData(limit.TestDataReporting.LowerLimitVolts, str(limit.LowerLimitVolts*100))
                                SetProcessData(limit.TestDataReporting.Samples, str(limit.TestData.Samples))
                                SetProcessData(limit.TestDataReporting.AvgChannelVoltageInRangeVolts, str(limit.TestData.AvgChannelVoltageInRangeVolts*100))
                                SetProcessData(limit.TestDataReporting.MaxChannelVoltageVolts, str(limit.TestData.MaxChannelVoltageVolts*100))
                                SetProcessData(limit.TestDataReporting.MinChannelVoltageVolts, str(limit.TestData.MinChannelVoltageVolts*100))
                                SetProcessData(limit.TestDataReporting.MaxTimeInPassWindowMsec, str(limit.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "SinkCurrentRangeBase" or testStep.Name == "SourceCurrentRangeBase" or testStep.Name == "SinkCurrentRangeDelta" or testStep.Name == "SourceCurrentRangeDelta"):
                    for currentRange in testStep.CurrentRanges:
                        if (IsTestFailed(str(currentRange.TestStepResults.TestResults))):
                            SetFault(currentRange.Fault.Id, currentRange.Fault.Description)

                        if (str(currentRange.TestStepResults.TestResults) != str(TestResults.NotTested) and str(currentRange.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetProcessData(currentRange.TestDataReporting.UpperLimitMamp, str(currentRange.UpperLimitMamp/100))
                            SetProcessData(currentRange.TestDataReporting.LowerLimitMamp, str(currentRange.LowerLimitMamp/100))
                            SetProcessData(currentRange.TestDataReporting.Samples, str(currentRange.TestData.Samples))
                            SetProcessData(currentRange.TestDataReporting.AvgCurrentInRangeMamp, str(currentRange.TestData.AvgCurrentInRangeMamp/100))
                            SetProcessData(currentRange.TestDataReporting.BaseCurrentMamp, str(currentRange.TestData.BaseCurrentMamp/100))
                            SetProcessData(currentRange.TestDataReporting.MaxCurrentMamp, str(currentRange.TestData.MaxCurrentMamp/100))
                            SetProcessData(currentRange.TestDataReporting.MinCurrentMamp, str(currentRange.TestData.MinCurrentMamp/100))
                            SetProcessData(currentRange.TestDataReporting.MaxTimeInPassWindowMsec, str(currentRange.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "SetCurrentLimits"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        SetProcessData(testStep.SetCurrentLimits.TestDataReporting.SourceLimitMamp, str(testStep.SetCurrentLimits.SourceLimitMamp/100))
                        SetProcessData(testStep.SetCurrentLimits.TestDataReporting.SinkLimitMamp, str(testStep.SetCurrentLimits.SinkLimitMamp/100))
                        SetProcessData(testStep.SetCurrentLimits.TestDataReporting.SourceLimitCounts, str(testStep.SetCurrentLimits.TestData.SourceLimitCounts/100))
                        SetProcessData(testStep.SetCurrentLimits.TestDataReporting.SinkLimitCounts, str(testStep.SetCurrentLimits.TestData.SinkLimitCounts/100))

                if (testStep.Name == "CanReceiveValidate"):
                    for canDataEntity in testStep.CanReceiveValidate.CanDataEntities:
                        if (IsTestFailed(str(canDataEntity.TestStepResults.TestResults))):
                            SetFault(canDataEntity.Fault.Id, canDataEntity.Fault.Description)

                if (testStep.Name == "CanSendReceiveValidate"):
                    for canDataEntity in testStep.CanSendReceiveValidate.CanDataEntities:
                        if (IsTestFailed(str(canDataEntity.TestStepResults.TestResults))):
                            SetFault(canDataEntity.Fault.Id, canDataEntity.Fault.Description)

                if (testStep.Name == "CanValidateSavedDtcData"):
                    for dtc in testStep.CanValidateSavedDtcData.Dtcs:
                        if (IsTestFailed(str(dtc.TestStepResults.TestResults))):
                            SetFault(dtc.Fault.Id, dtc.Fault.Description)
                            if (dtc.Fault.Detail):
                                screenLabelFaultText = screenLabelFaultText + "   " + dtc.Fault.Detail + "\r\n"
                            if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                                if (dtc.Fault.Detail):
                                    numberFaultsAdded = numberFaultsAdded + 1
                                    printedFaultText = printedFaultText + "   " + dtc.Fault.Detail + "\r\n"

                if (testStep.Name == "CanValidatePartNumber"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):

                        #Add Broadcasted and Processed Part Numbers to printed label
                        if (str(testStep.TestStepResults.TestResults) != str(TestResults.Pass)):
                            if (testStep.Fault.Detail):
                                screenLabelFaultText = screenLabelFaultText + "   " + testStep.Fault.Detail + "\r\n"
                            if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                                if (testStep.Fault.Detail):
                                    numberFaultsAdded = numberFaultsAdded + 1
                                    printedFaultText = printedFaultText + "   " + testStep.Fault.Detail + "\r\n"
                                    #printedFaultText = printedFaultText + "   PN from Broadcast: " + testStep.CanValidatePartNumber.TestData.BroadcastedPartNumber + "," + " PN from Module: " + testStep.CanValidatePartNumber.TestData.ProcessedPartNumber + "\r\n"

                        if (testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber):
                            try:
                                userValueIds = testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber.Split(',')
                                if len(userValueIds) != 2:
                                    TPassLogger.Error("Test Results Processing Script:  BroadcastedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber)
                                else:
                                    try:
                                        userValues = testStep.CanValidatePartNumber.TestData.BroadcastedPartNumber
                                        if (not Regex.IsMatch(userValues, "^\d{8}$")):
                                            TPassLogger.Warn("Test Results Processing Script:  BroadcastedPartNumber format must be 8 digits.  Value = {0}", testStep.CanValidatePartNumber.TestData.BroadcastedPartNumber)
                                        else:
                                            userValues = [userValues[i:i+4] for i in range(0, len(userValues), 4)]
                                            SetProcessData(userValueIds[0], userValues[0])
                                            SetProcessData(userValueIds[1], userValues[1])
                                    except Exception as inst:
                                        TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                        isSuccess = False
                            except Exception as inst:
                                TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                TPassLogger.Warn("Test Results Processing Script:  BroadcastedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber)
 
                        if (testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber):
                            try:
                                userValueIds = testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber.Split(',')
                                if len(userValueIds) != 2:
                                    TPassLogger.Error("Test Results Processing Script:  ProcessedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber)
                                else:
                                    try:
                                        userValues = testStep.CanValidatePartNumber.TestData.ProcessedPartNumber
                                        if (not Regex.IsMatch(userValues, "^\d{8}$")):
                                            TPassLogger.Warn("Test Results Processing Script:  ProcessedPartNumber format must be 8 digits.  Value = {0}", testStep.CanValidatePartNumber.TestData.ProcessedPartNumber)
                                        else:
                                            userValues = [userValues[i:i+4] for i in range(0, len(userValues), 4)]
                                            SetProcessData(userValueIds[0], userValues[0])
                                            SetProcessData(userValueIds[1], userValues[1])
                                    except Exception as inst:
                                        TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                        isSuccess = False
                            except Exception as inst:
                                TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                TPassLogger.Warn("Test Results Processing Script:  ProcessedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber)

                if (testStep.Name == "LinSendReceiveValidate"):
                    for linDataEntity in testStep.LinSendReceiveValidate.LinDataEntities:
                        if (IsTestFailed(str(linDataEntity.TestStepResults.TestResults))):
                            SetFault(linDataEntity.Fault.Id, linDataEntity.Fault.Description)

                if (testStep.Name == "ModbusValidateVoltageRange"):
                    for channel in testStep.ModbusValidateVoltageRange.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id, channel.Fault.Description)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetProcessData(channel.TestDataReporting.UpperLimitMVolt, str(channel.UpperLimitMVolt/100))
                            SetProcessData(channel.TestDataReporting.LowerLimitMVolt, str(channel.LowerLimitMVolt/100))
                            SetProcessData(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetProcessData(channel.TestDataReporting.MaxChannelVoltageMVolts, str(channel.TestData.MaxChannelVoltageMVolts/100))
                            SetProcessData(channel.TestDataReporting.MinChannelVoltageMVolts, str(channel.TestData.MinChannelVoltageMVolts/100))
                            SetProcessData(channel.TestDataReporting.AvgChannelVoltageInRangeMVolt, str(channel.TestData.AvgChannelVoltageInRangeMVolt/100))
                            SetProcessData(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "ModbusValidateVoltageRangeBase"):
                    for channel in testStep.ModbusValidateVoltageRangeBase.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id, channel.Fault.Description)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetProcessData(channel.TestDataReporting.UpperLimitMVolt, str(channel.UpperLimitMVolt/100))
                            SetProcessData(channel.TestDataReporting.LowerLimitMVolt, str(channel.LowerLimitMVolt/100))
                            SetProcessData(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetProcessData(channel.TestDataReporting.MaxChannelVoltageMVolts, str(channel.TestData.MaxChannelVoltageMVolts/100))
                            SetProcessData(channel.TestDataReporting.MinChannelVoltageMVolts, str(channel.TestData.MinChannelVoltageMVolts/100))
                            SetProcessData(channel.TestDataReporting.BaseChannelVoltageMVolts, str(channel.TestData.BaseChannelVoltageMVolts/100))
                            SetProcessData(channel.TestDataReporting.AvgChannelVoltageInRangeMVolt, str(channel.TestData.AvgChannelVoltageInRangeMVolt/100))
                            SetProcessData(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "ModbusValidateVoltageRangeDelta"):
                    for channel in testStep.ModbusValidateVoltageRangeDelta.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id, channel.Fault.Description)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetProcessData(channel.TestDataReporting.UpperLimitMVolt, str(channel.UpperLimitMVolt/100))
                            SetProcessData(channel.TestDataReporting.LowerLimitMVolt, str(channel.LowerLimitMVolt/100))
                            SetProcessData(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetProcessData(channel.TestDataReporting.MaxChannelVoltageMVolts, str(channel.TestData.MaxChannelVoltageMVolts/100))
                            SetProcessData(channel.TestDataReporting.MinChannelVoltageMVolts, str(channel.TestData.MinChannelVoltageMVolts/100))
                            SetProcessData(channel.TestDataReporting.BaseChannelVoltageMVolts, str(channel.TestData.BaseChannelVoltageMVolts/100))
                            SetProcessData(channel.TestDataReporting.AvgChannelVoltageInRangeMVolt, str(channel.TestData.AvgChannelVoltageInRangeMVolt/100))
                            SetProcessData(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "MeterValidateVoltageRange"):
                    for channel in testStep.MeterValidateVoltageRange.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id, channel.Fault.Description)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetProcessData(channel.TestDataReporting.UpperLimitVolt, str(channel.UpperLimitVolt))
                            SetProcessData(channel.TestDataReporting.LowerLimitVolt, str(channel.LowerLimitVolt))
                            SetProcessData(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetProcessData(channel.TestDataReporting.MaxChannelVoltageVolts, str(channel.TestData.MaxChannelVoltageVolts))
                            SetProcessData(channel.TestDataReporting.MinChannelVoltageVolts, str(channel.TestData.MinChannelVoltageVolts))
                            SetProcessData(channel.TestDataReporting.AvgChannelVoltageInRangeVolt, str(channel.TestData.AvgChannelVoltageInRangeVolt))
                            SetProcessData(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "MeterValidateFrequencyRange"):
                    for channel in testStep.MeterValidateFrequencyRange.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id, channel.Fault.Description)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetProcessData(channel.TestDataReporting.UpperLimitHz, str(channel.UpperLimitHz))
                            SetProcessData(channel.TestDataReporting.LowerLimitHz, str(channel.LowerLimitHz))
                            SetProcessData(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetProcessData(channel.TestDataReporting.MaxChannelFrequencyHz, str(channel.TestData.MaxChannelFrequencyHz))
                            SetProcessData(channel.TestDataReporting.MinChannelFrequencyHz, str(channel.TestData.MinChannelFrequencyHz))
                            SetProcessData(channel.TestDataReporting.AvgChannelFrequencyInRangeHz, str(channel.TestData.AvgChannelFrequencyInRangeHz))
                            SetProcessData(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))
 
                if (testStep.Name == "MeterValidateResistanceRange"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        SetProcessData(testStep.MeterValidateResistanceRange.TestDataReporting.UpperLimitOhm, str(testStep.MeterValidateResistanceRange.UpperLimitOhm))
                        SetProcessData(testStep.MeterValidateResistanceRange.TestDataReporting.LowerLimitOhm, str(testStep.MeterValidateResistanceRange.LowerLimitOhm))
                        SetProcessData(testStep.MeterValidateResistanceRange.TestDataReporting.Samples, str(testStep.MeterValidateResistanceRange.TestData.Samples))
                        SetProcessData(testStep.MeterValidateResistanceRange.TestDataReporting.MaxChannelResistanceOhms, str(testStep.MeterValidateResistanceRange.TestData.MaxChannelResistanceOhms))
                        SetProcessData(testStep.MeterValidateResistanceRange.TestDataReporting.MinChannelResistanceOhms, str(testStep.MeterValidateResistanceRange.TestData.MinChannelResistanceOhms))
                        SetProcessData(testStep.MeterValidateResistanceRange.TestDataReporting.AvgChannelResistanceInRangeOhms, str(testStep.MeterValidateResistanceRange.TestData.AvgChannelResistanceInRangeOhms))
                        SetProcessData(testStep.MeterValidateResistanceRange.TestDataReporting.MaxTimeInPassWindowMsec, str(testStep.MeterValidateResistanceRange.TestData.MaxTimeInPassWindowMsec/1000))

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Results File.  Exception Occurred :{0}", inst)
    MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Creating Results File.  Exception Occurred = " + str(inst), True, True)
    isSuccess = False

# Create Results File
try:
    resultsFile = ""
    startDateTime = DateTime.Now.ToString("yyyy-MM-dd HH_mm_ss_fff")
    resultsFile = resultsFileFolder + startDateTime + "_" + productIdentification.PrimaryId + "_" + testerId + ".txt"
    
    # Create folder if it doesn't exist
    if Directory.Exists(resultsFileFolder) == False:
        Directory.CreateDirectory(resultsFileFolder)
        
    # Remove Results files if exist
    if File.Exists(resultsFile + "TMP"):
        try:
            File.Delete(resultsFile + "TMP")
        except Exception as inst:
            TPassLogger.Debug("Test Results Processing Script:  File.Delete Exception Occurred :{0}", inst)            
    if File.Exists(resultsFile):
        try:
            File.Delete(resultsFile)
        except Exception as inst:
            TPassLogger.Debug("Test Results Processing Script:  File.Delete Exception Occurred :{0}", inst)            

    # Create Results file 
    try:
        resultsText = ""
        if (overallTestResultsPass):
            resultsText = printedLabelText
        else:
            resultsText = printedLabelText + printedFaultText
        File.WriteAllText(resultsFile + "TMP", resultsText)
        File.Move(resultsFile + "TMP", resultsFile)
        MainTPassScripting.InterfaceUiLogger("Vuteq", "Results File Written - " + resultsFile, False, False)
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Vuteq", "File.WriteAllText Exception Occurred" + str(inst), True, True)
        TPassLogger.Error("Test Results Processing Script:  File.WriteAllText Exception Occurred :{0}", inst)            

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Results File.  Exception Occurred :{0}", inst)
    MainTPassScripting.InterfaceUiLogger("Vuteq", "Error Creating Results File.  Exception Occurred = " + str(inst), True, True)
    isSuccess = False

# Create Screen Label Text to pass back to TPass for displaying on the Pass/Fail screens
try:
    if (overallTestResultsPass):
        screenLabelText = "<fontsize:32>" + screenLabelText + "<b>\r\n\r\nPASSED\r\nPASSED\r\nPASSED\r\nPASSED" + "</b></fontsize>"
    else:
        screenLabelText = "<fontsize:32>" + screenLabelText + "</fontsize>" + "<fontsize:24>\r\n<b>FLTS:" + str(totalNumberOfFaults) + "</b></fontsize>" + "<fontsize:32>\r\n" + screenLabelFaultText + "</fontsize>"

    MainTPassScripting.UpdateTestResultsScreenCustomText(screenLabelText)
    TPassLogger.Debug("Test Results Processing Script:  Product Primary ID = {0}, Screen Custom Label Text = {1}", productIdentification.PrimaryId, screenLabelText )

except:
    TPassLogger.Warn("Test Results Processing Script:  UpdateTestResultsScreenCustomText being called but functionality is not implemented until TPass v1.4.0.3 or later")
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("Vuteq", "UpdateTestResultsScreenCustomText being called but functionality is not implemented until TPass v1.4.0.3 or later", True, False)

# Create Printed Label Text to pass back to TPass for printing.  Do Not Print if Test Cycle Passed!
try:
    if (printPassLabel == False and overallTestResultsPass):
        printedLabelText = ""
    else:
        printedLabelText = printedLabelText + printedFaultText

    TPassLogger.Debug("Test Results Processing Script:  Product Primary ID = {0}, Printed Label Text = {1}", productIdentification.PrimaryId, printedLabelText )

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Test Label Text.  Exception Occurred :{0}", inst)
    isSuccess = False

TPassLogger.Info("Test Results Processing Script:  Is Success = {0}", isSuccess)





############################################################
# Change History
############################################################
#	Date: 10252022
#	Version: 1.0
#	Change: Initial Version
############################################################

