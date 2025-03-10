#Create a Magna-ESSS Test Results Record and format and return the Printed Label Text for TPass to send to a printer
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
from System.IO import File
from System.IO import Directory
from System import DateTime
from System.Collections.Generic import List

version = "4.0"
production = False
TPassLogger.Debug("Test Results Processing Script:  Product Primary Id = {0}", productIdentification.PrimaryId)
TPassLogger.Debug("Test Results Processing Script:  Product Secondary Id = {0}", productIdentification.SecondaryId)
isSuccess = True

#########################################################################################################################################
# Application Engineer:  
#
printPassLabel = False

maxNumberFaultsOnPrintedLabel = 10
customLogFileName = "C:\TPass\Logs\Magna\TestResults.csv"
customLogDirectoryName = "C:\TPass\Logs\Magna"
#
#########################################################################################################################################

testerId = "0"                                      # Will be read from the \TPass\Support Files\SID.txt file
testerIdFile = "C:\TPass\Support Files\SID.txt"
overallTestResultsPass = False
testResultsText = ""
testFaults = ""
processResultsText = ""
printedFaultText = ""
numberFaultsAdded = 0
screenLabelFaultText = ""
totalNumberOfFaults = 0
testSeat1WbsKeyIde = ""
testSeat2WbsKeyIde = ""
testSeat3WbsKeyIde = ""
testSeat1B1Status = "0"
testSeat1B2Status = "0"
testSeat1B3Status = "0"
testSeat2B1Status = "0"
testSeat2B2Status = "0"
testSeat2B3Status = "0"
testSeat3B1Status = "0"
testSeat3B2Status = "0"
testSeat3B3Status = "0"
resultsFile = "C:\TPass\Data Outgoing\Results.txt"
magaResultLogHeaderFields = List[str](["TesterId","TestResults","TestStartTime","CycleTimeSec","MFGUnitID","Recipe","RowType","TestApp","Seat1WbsKeyIde","Seat2WbsKeyIde","Seat3WbsKeyIde","Seat1B1Status","Seat1B2Status","Seat1B3Status","Seat2B1Status","Seat2B2Status","Seat2B3Status","Seat3B1Status","Seat3B2Status","Seat3B3Status","FaultDesc"])
magaResultLog = "\r\n"
magnaLogFaultText = ""

#DEBUG
#12529693;PASS
#12535192;FAIL;214,101,106

# Internal Functions
def IsTestFailed(testResults):

    if (testResults == str(TestResults.Fail) or testResults == str(TestResults.FatalFail) or
            testResults == str(TestResults.OperatorFail) or testResults == str(TestResults.OperatorAbort) or testResults == str(TestResults.SystemError)):
        return True
    else:
        return False

def SetFault(faultId, faultDescription):
    global testFaults
    global printedFaultText
    global magnaLogFaultText
    global maxNumberFaultsOnPrintedLabel
    global numberFaultsAdded
    global totalNumberOfFaults
    global screenLabelFaultText
    
    totalNumberOfFaults += 1
    if (faultDescription != ""):
        screenLabelFaultText = screenLabelFaultText + " - " + faultDescription + "\r\n"
        if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
            numberFaultsAdded = numberFaultsAdded + 1
            testFaults = testFaults + faultDescription[0:64] + ","
            printedFaultText = printedFaultText + faultDescription[0:64] + "\r\n"
            magnaLogFaultText = magnaLogFaultText + faultDescription[0:64] + ";" 
        
def SetBuckleResults(testResults):

    if (testResults == str(TestResults.OptionCodeNotTested)):
        return "1"
    elif (testResults == str(TestResults.Pass)):
        return "2"
    elif (IsTestFailed(testResults)):
        return "3"    
    else:
        return "0"

def SetProcessData(reportId, reportData):
    global processResultsText
    if (reportId and reportData):
        # Saving Process Data is not implemented for Magna-ESSS
        processResultsText = ""

# Main Logic
try:

    #Read testerId from file
    try:
       testerIdLines = File.ReadAllLines(testerIdFile)
       testerId = testerIdLines[0]
    except Exception as inst:
       MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Error Reading Test ID File, will default to Tester ID = 0.  Exception Occurred = " + str(inst), True, True)
       TPassLogger.Error("Option Parsing Script:  Error Reading Test ID File, will default to Tester ID = 0.  File.ReadLines Exception Occurred :{0}", inst)            
    magaResultLog += testerId + ","
    
    # Remove results file if exist
    if File.Exists(resultsFile + "TMP"):
        try:
            File.Delete(resultsFile + "TMP")
        except Exception as inst:
            TPassLogger.Debug("Results Processing Script:  File.Delete Exception Occurred :{0}", inst)            
    if File.Exists(resultsFile):
        try:
            File.Delete(resultsFile)
        except Exception as inst:
            TPassLogger.Debug("Results Processing Script:  File.Delete Exception Occurred :{0}", inst)            


    testResultsText = testerId + ";"
    testResultsText = productIdentification.PrimaryId

    printedLabelText = str(DateTime.Now) + "\r\n"
    printedLabelText = printedLabelText + "Serial Number:" + productIdentification.PrimaryId + "\r\n"
#    printedLabelText = printedLabelText + "Recipe:" + productIdentification.SecondaryId + "\r\n"
    printedLabelText = printedLabelText + "Tester ID:" + testerId + "\r\n"
    screenLabelText = str(DateTime.Now) + "\r\n"
    screenLabelText = screenLabelText + "STN:" + testerId + "  " + " BSN:" + productIdentification.PrimaryId + "  " + "Recipe:" + productIdentification.SecondaryId + "  " + "Row Type:" + productIdentification.TertiaryId + "\r\n"
        

    if (str(testAppResults.MainTestApplication.TestCycleResults.TestResults) == str(TestResults.Fail)):
        overallTestResultsPass = False
        testResultsText = testResultsText + ";" + "FAIL;"
        printedLabelText = printedLabelText + "Overall = F" + "\r\n"
        magaResultLog += "FAIL" + ","
    else:
        testResultsText = testResultsText + ";" + "PASS;"
        printedLabelText = printedLabelText + "Overall = P" + "\r\n"
        overallTestResultsPass = True
        magaResultLog += "PASS" + ","

    if (testAppResults.MainTestApplication.TestCycleResults.Abort):
        SetFault("", "TEST ABORTED")
        
    # Set Results to send to Magna-ESSS
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
 
                if (testStep.Name == "CanValidatePartNumber"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        SetProcessData(testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber, testStep.CanValidatePartNumber.TestData.BroadcastedPartNumber)
                        SetProcessData(testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber, testStep.CanValidatePartNumber.TestData.ProcessedPartNumber)

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

                if (testStep.Name == "MarquardtKtbSeatBuckleTest"):
                    #Set the PLC Seat Result Status for each Seat based on Device ID
                    if (testStep.MarquardtKtbSeatBuckleTest.DeviceId == 1):
                        testSeat1B1Status = SetBuckleResults(str(testStep.MarquardtKtbSeatBuckleTest.TestData.Buckle1Results))
                        testSeat1B2Status = SetBuckleResults(str(testStep.MarquardtKtbSeatBuckleTest.TestData.Buckle2Results))
                        testSeat1B3Status = SetBuckleResults(str(testStep.MarquardtKtbSeatBuckleTest.TestData.Buckle3Results))
                        testSeat1WbsKeyIde = str(testStep.MarquardtKtbSeatBuckleTest.TestData.KeyIde)
                    if (testStep.MarquardtKtbSeatBuckleTest.DeviceId == 2):
                        testSeat2B1Status = SetBuckleResults(str(testStep.MarquardtKtbSeatBuckleTest.TestData.Buckle1Results))
                        testSeat2B2Status = SetBuckleResults(str(testStep.MarquardtKtbSeatBuckleTest.TestData.Buckle2Results))
                        testSeat2B3Status = SetBuckleResults(str(testStep.MarquardtKtbSeatBuckleTest.TestData.Buckle3Results))
                        testSeat2WbsKeyIde = str(testStep.MarquardtKtbSeatBuckleTest.TestData.KeyIde)
                    if (testStep.MarquardtKtbSeatBuckleTest.DeviceId == 3):
                        testSeat3B1Status = SetBuckleResults(str(testStep.MarquardtKtbSeatBuckleTest.TestData.Buckle1Results))
                        testSeat3B2Status = SetBuckleResults(str(testStep.MarquardtKtbSeatBuckleTest.TestData.Buckle2Results))
                        testSeat3B3Status = SetBuckleResults(str(testStep.MarquardtKtbSeatBuckleTest.TestData.Buckle3Results))
                        testSeat3WbsKeyIde = str(testStep.MarquardtKtbSeatBuckleTest.TestData.KeyIde)
                
                    #Add Fault Detail to screen and printed results labels
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.Pass)):
                        if (testStep.Fault.Detail):
                            screenLabelFaultText = screenLabelFaultText + "   :" + testStep.Fault.Detail + "\r\n"
                        if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                            if (testStep.Fault.Detail):
                                numberFaultsAdded = numberFaultsAdded + 1
                                printedFaultText = printedFaultText + "   :" + testStep.Fault.Detail + "\r\n"
                                magnaLogFaultText = magnaLogFaultText + ";" + testStep.Fault.Detail  + ";"
                    for sequentialTestStep in testStep.MarquardtKtbSeatBuckleTest.KtbSequentialTestSteps:
                        if (IsTestFailed(str(sequentialTestStep.TestStepResults.TestResults))):
                            SetFault(sequentialTestStep.Fault.Id, sequentialTestStep.Fault.Description)
                            if (sequentialTestStep.Fault.Detail):
                                screenLabelFaultText = screenLabelFaultText + "   :" + sequentialTestStep.Fault.Detail + "\r\n"
                            if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                                if (sequentialTestStep.Fault.Detail):
                                    numberFaultsAdded = numberFaultsAdded + 1
                                    printedFaultText = printedFaultText + "   :" + sequentialTestStep.Fault.Detail + "\r\n"
                                    magnaLogFaultText = magnaLogFaultText + ";" + sequentialTestStep.Fault.Detail + ";"

                    #Add Process Data
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        SetProcessData(testStep.MarquardtKtbSeatBuckleTest.TestDataReporting.KeyIde, str(testStep.MarquardtKtbSeatBuckleTest.TestData.KeyIde))

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Results Record.  Exception Occurred :{0}", inst)
    MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Error Creating Results Record.  Exception Occurred = " + str(inst), True, True)
    isSuccess = False

# Create Results file for Magna-ESSS to process
try:
    try:
        testResultsText = testResultsText + testSeat1B1Status + ";"
        testResultsText = testResultsText + testSeat1B2Status + ";"
        testResultsText = testResultsText + testSeat1B3Status + ";"
        testResultsText = testResultsText + testSeat2B1Status + ";"
        testResultsText = testResultsText + testSeat2B2Status + ";"
        testResultsText = testResultsText + testSeat2B3Status + ";"
        testResultsText = testResultsText + testSeat3B1Status + ";"
        testResultsText = testResultsText + testSeat3B2Status + ";"
        testResultsText = testResultsText + testSeat3B3Status + ";"
        testResultsText = testResultsText + testFaults.rstrip(",")
        MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Test Results - " + testResultsText, False, False)
        File.WriteAllText(resultsFile + "TMP", testResultsText)
        File.Move(resultsFile + "TMP", resultsFile)
        MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Results File Written - " + resultsFile, False, False)
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "File.WriteAllText Exception Occurred" + str(inst), True, True)
        TPassLogger.Error("Option Retrieval Script:  File Exception Occurred :{0}", inst)            

    TPassLogger.Debug("Test Results Processing Script:  Product Primary ID = {0}, Results File Text = {1}", productIdentification.PrimaryId, testResultsText )

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Test Label Text.  Exception Occurred :{0}", inst)
    isSuccess = False

# Create Screen Label Text to pass back to TPass for displaying on the Pass/Fail screens
try:
    if (overallTestResultsPass):
        screenLabelText = "<fontsize:32>" + screenLabelText + "<b>\r\n\r\nPASSED\r\nPASSED\r\nPASSED\r\nPASSED" + "</b></fontsize>"
    else:
        screenLabelText = "<fontsize:32>" + screenLabelText + "</fontsize>" + "<fontsize:24>\r\n<b>FLTS:" + str(totalNumberOfFaults) + "</b></fontsize>" + "<fontsize:24>\r\n" + screenLabelFaultText + "</fontsize>"
        #screenLabelText = "<b>The reason</b> <fontsize:30>why this failed</fontsize> <fontsize:12><color:green>is because somebody turned</color> the light off... duh!</fontsize>"

    MainTPassScripting.UpdateTestResultsScreenCustomText(screenLabelText)
    TPassLogger.Debug("Test Results Processing Script:  Product Primary ID = {0}, Screen Custom Label Text = {1}", productIdentification.PrimaryId, screenLabelText )

except:
    TPassLogger.Warn("Test Results Processing Script:  UpdateTestResultsScreenCustomText being called but functionality is not implemented until TPass v1.4.0.3 or later")
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "UpdateTestResultsScreenCustomText being called but functionality is not implemented until TPass v1.4.0.3 or later", True, False)

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

# Create Magna Custom Log File
try:
    magaResultLogHeader = ""
    for field in magaResultLogHeaderFields:
        magaResultLogHeader += field + ","
    if (not Directory.Exists(customLogDirectoryName)):
        Directory.CreateDirectory(customLogDirectoryName)
    if (not File.Exists(customLogFileName)):
        #populate field names in first row
        File.WriteAllText(customLogFileName, magaResultLogHeader)

    testAppFileName = testAppResults.MainTestApplication.FileName + " Ver: " + str(testAppResults.MainTestApplication.VersionMajor) + "." + str(testAppResults.MainTestApplication.VersionMinor)
    magaResultLog += testAppResults.MainTestApplication.TestCycleResults.BeginDateTime.ToString("MM/dd/yyyy HH:mm:ss:fff") + ","
    magaResultLog += str((float(testAppResults.MainTestApplication.TestCycleResults.DurationMsec) / 1000)) + "," + productIdentification.PrimaryId + "," + productIdentification.SecondaryId + "," + productIdentification.TertiaryId + "," + testAppFileName + ","
    magaResultLog += testSeat1WbsKeyIde + "," + testSeat2WbsKeyIde + "," + testSeat3WbsKeyIde + "," + testSeat1B1Status + "," + testSeat1B2Status + "," + testSeat1B3Status + ","
    magaResultLog += testSeat2B1Status + "," + testSeat2B2Status + "," + testSeat2B3Status + "," + testSeat3B1Status + "," + testSeat3B2Status + "," + testSeat3B3Status + "," + magnaLogFaultText.rstrip(",")
    File.AppendAllText(customLogFileName, magaResultLog)
    
except Exception as inst:
    #TPassLogger.Warn("Test Results Processing Script:  Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = {0}", faultId)
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("Magna", "Results Processing Script:  Error writing to Magna Custom Test Results Log File - " + str(inst), True, False)

TPassLogger.Info("Test Results Processing Script:  Is Success = {0}", isSuccess)


############################################################
# Change History
############################################################
#	Date: 02122024
#	Version: 4.0
#   ChangeBy: RMM
#	Change: Added writing Magna Custom Test Result Log File
#	Date: 06162023
#	Version: 3.0
#   ChangeBy: RMM
#	Change: Added writing Test Results for each buckle on each seat
#	Date: 06062023
#	Version: 2.0
#   ChangeBy: RMM
#	Change: Implement PLC Interface
#	Date: 04172023
#	Version: 1.0
#   ChangeBy: RMM
#	Change: Initial Version
############################################################

