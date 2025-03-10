#Create a GM Test Results to be sent to the Flash Tool via Gm Tcp Handshake protocol
#Format and return the Printed Label Text for TPass to send to a printer
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - object "testAppResults"
#   in  - object "productIdentification"
#   in  - COM object "gmEdiBuildResultsRecord" - GmTcpHs Interface pointer for creating GEPICS Shipping Control records, GSIP Quality Records and MERS Test Results records
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application Detail log file
#   in  - object "SystemConfigurationValue" - This is the object to get values set in the System Configuration file
#   out - string "printedLabelText" - TPass will send this text to the default printer if the string is not blank and if the printer is enabled in the TPass system configuration settings
#   out - string "MainTPassScripting.GmTcpHsLastTestResult" - TPass will send this text to GmHs using tag RESULTSDATA
#   out - string "MainTPassScripting.GmTcpHsLastTestResultsFlag" - TPass will send this text to GmHs using tag STATUS
#   out - bool "isSuccess" - Set to True if Test Results processing was successful.  Otherwise False
#   out - bool "production"
#   out - string "version"
#

import clr
clr.AddReferenceToFileAndPath('.\\Tpi.TPass.Common.dll')
from Tpi.TPass.Common.JsonStore import TestResults
from System.Text.RegularExpressions import Regex
from System import DateTime

version = "2.0"
production = False
TPassLogger.Debug("Test Results Processing Script:  Product Primary Id = {0}", productIdentification.PrimaryId)
TPassLogger.Debug("Test Results Processing Script:  Product Secondary Id = {0}", productIdentification.SecondaryId)
isSuccess = True
printedLabelText = ""

#########################################################################################################################################
# Application Engineer:  Set Station Number to be written to the printed label
#
stationNumber = "77" 
printPassLabel = False
maxNumberTestFaultsOnLabel = 5
maxNumberFlashFaultsOnLabel = 5
overrideResultsScreenDisplayTimeSec = 0   # This time is used for Passed Tests as well as when Flash Fails and the Operator hits the Flash Retest button during the ETest
#
#########################################################################################################################################

overallTestResultsPass = False
printedFaultText = ""
resultsFaultText = ""
resultsGmHsText = ""
numberFaultsAdded = 0

# Internal Functions
def IsTestFailed(testResults):

    if (testResults == str(TestResults.Fail) or testResults == str(TestResults.FatalFail) or
            testResults == str(TestResults.OperatorFail) or testResults == str(TestResults.OperatorAbort) or testResults == str(TestResults.SystemError)):
        return True
    else:
        return False

def SetFault(faultId, faultDescription):
    global printedFaultText
    global resultsFaultText
    global maxNumberTestFaultsOnLabel
    global numberFaultsAdded
    if (faultId):
        try:
            if (numberFaultsAdded < maxNumberTestFaultsOnLabel):
                numberFaultsAdded = numberFaultsAdded + 1
                addedString = "  " + faultId + "," + faultDescription + "\r\n"
                printedFaultText = printedFaultText + addedString
            ediFaultId = int(faultId)
        except:
            TPassLogger.Warn("Test Results Processing Script:  Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = {0}", faultId)
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            MainTPassScripting.InterfaceUiLogger("GmTcpHs", "Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = " + faultId, True, True)
        else:
            if (ediFaultId >= 0 and ediFaultId <= 65535):
                try:
                    resultsFaultText = resultsFaultText + ",FLT=" + str(ediFaultId).zfill(5)
                    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                    MainTPassScripting.InterfaceUiLogger("GmTcpHs", "SetFault() Fault =  " + faultId, False, False)
                except Exception as inst:
                    TPassLogger.Warn("Test Results Processing Script:  Error SetFault().  Exception Occurred :{0}", inst)
                    MainTPassScripting.InterfaceUiLogger("GmTcpHs", "Error SetFault().  Exception Occurred = " + str(inst), True, False)
            else:
                TPassLogger.Warn("Test Results Processing Script:  Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = {0}", faultId)
                # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                MainTPassScripting.InterfaceUiLogger("GmTcpHs", "Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = " + faultId, True, True)

def SetProcessData(userValueId, userValue):
    # Saving Process Data is not implemented for GmHs
    userValueId = userValueId

# Main Logic
try:
    if MainTPassScripting.GmTcpHsLastMsgType != "FLASH":

        printedLabelText = str(DateTime.Now) + "\r\n"
        printedLabelText = printedLabelText + "VIN:" + productIdentification.SecondaryId + "\r\n"
        printedLabelText = printedLabelText + "STN:" + stationNumber + " DP#" + productIdentification.PrimaryId + "\r\n"

        if (str(testAppResults.MainTestApplication.TestCycleResults.TestResults) == str(TestResults.Fail)):
            overallTestResultsPass = False
            printedLabelText = printedLabelText + "Test Status: Failed" + "\r\n"
            resultsGmHsText = "RESULT=" + "F,"
            MainTPassScripting.GmTcpHsLastTestResultsFlag = "FAIL"
        else:
            printedLabelText = printedLabelText + "Test Status: Passed" + "\r\n"
            resultsGmHsText = "RESULT=" + "P,"
            overallTestResultsPass = True
            MainTPassScripting.GmTcpHsLastTestResultsFlag = "PASS"
            MainTPassScripting.OverrideResultsScreenDisplayTimeSec(overrideResultsScreenDisplayTimeSec)

        if MainTPassScripting.GmHsFlashRetestButtonPressed:
            MainTPassScripting.OverrideResultsScreenDisplayTimeSec(overrideResultsScreenDisplayTimeSec)
        
        resultsGmHsText = resultsGmHsText + "PVI=" + productIdentification.PrimaryId + ","
        resultsGmHsText = resultsGmHsText + "VIN=" + productIdentification.SecondaryId + ","
        resultsGmHsText = resultsGmHsText + "STN=" + stationNumber + ","
        resultsGmHsText = resultsGmHsText + "TIME=" + str(testAppResults.MainTestApplication.TestCycleResults.DurationMsec / 1000)
            
        if (testAppResults.MainTestApplication.TestCycleResults.Abort):
            SetFault("08495", "TEST ABORTED")
            MainTPassScripting.GmTcpHsLastTestResultsFlag = "ABORT"

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

                    if (testStep.Name == "CanValidatePartNumber"):
                        if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
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
                                            TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in History Record.  Exception Occurred :{0}", inst)
                                            isSuccess = False
                                except Exception as inst:
                                    TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in History Record.  Exception Occurred :{0}", inst)
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
                                            TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in History Record.  Exception Occurred :{0}", inst)
                                            isSuccess = False
                                except Exception as inst:
                                    TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in History Record.  Exception Occurred :{0}", inst)
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

        # Set GmHs Results string for TPass to send
        MainTPassScripting.GmTcpHsLastTestResult = resultsGmHsText + resultsFaultText
        MainTPassScripting.InterfaceUiLogger("GmTcpHs", "Results Data =  " + MainTPassScripting.GmTcpHsLastTestResult, False, False)
        TPassLogger.Debug("Test Results Processing Script:  Product Primary ID = {0}, Results = {1}", productIdentification.PrimaryId, MainTPassScripting.GmTcpHsLastTestResult )

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating GmHs Test Results String.  Exception Occurred :{0}", inst)
    MainTPassScripting.InterfaceUiLogger("GmTcpHs", "Error Creating GmHs Test Results String.  Exception Occurred = " + str(inst), True, True)
    isSuccess = False


# GmHs only prints for the power up (PREDATA) and electrical test (TEST).  Create Printed Label Text to pass back to TPass for printing.
try:

    if MainTPassScripting.GmTcpHsLastMsgType == "PREDATA":   
        if (printPassLabel == False and overallTestResultsPass):
            printedLabelText = ""
        else:
            printedLabelText = printedLabelText + printedFaultText + "\r\n" 
    elif MainTPassScripting.GmTcpHsLastMsgType == "TEST":   
        if (printPassLabel == False and overallTestResultsPass):
            printedLabelText = ""
        else:
            printedLabelText = printedLabelText + printedFaultText + "\r\n" 
            if MainTPassScripting.GmTcpHsLastFlashResults == "":
                printedLabelText = printedLabelText + "FLASH Results: NOT TESTED" 
            else:
                # Format Flash Results prior to appending to TEST results
                flashResultsText = ""
                try:
                    numberFlashFaultsAdded = 0
                    
                    flashLines = MainTPassScripting.GmTcpHsLastFlashResults.split(",FLT=")
                    if len(flashLines) != 0:
                        for flashLine in flashLines:
                            if (numberFlashFaultsAdded == 0):
                                if "RESULT=P" in flashLine:
                                    flashResultsText = "Passed" + "\r\n"
                                else:
                                    flashResultsText = "Failed" + "\r\n"
                            elif (numberFlashFaultsAdded <= maxNumberFlashFaultsOnLabel):
                                flashResultsText = flashResultsText + "  " + flashLine
                            numberFlashFaultsAdded = numberFlashFaultsAdded + 1
                except:
                    TPassLogger.Warn("Test Results Processing Script:  Failed parsing Flash Results  Flash Results = {0}", MainTPassScripting.GmTcpHsLastFlashResults)
                    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                    MainTPassScripting.InterfaceUiLogger("GmTcpHs", "Test Results Processing Script:  Failed parsing Flash Results  Flash Results = " + MainTPassScripting.GmTcpHsLastFlashResults, True, True)
                
                printedLabelText = printedLabelText + "FLASH Results: " + flashResultsText 
    else:
        printedLabelText = ""
        
    TPassLogger.Debug("Test Results Processing Script:  Product Primary ID = {0}, Printed Label Text = {1}", productIdentification.PrimaryId, printedLabelText )

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Test Label Text.  Exception Occurred :{0}", inst)
    isSuccess = False

TPassLogger.Info("Test Results Processing Script:  Is Success = {0}", isSuccess)





############################################################
# Change History
############################################################
#	Date: 02082022
#	Version: 2.0
#	Change: If Flash Retest Button was hit, override Results Screen Display Time
#	Date: 11082021
#	Version: 1.0
#	Change: Initial Version
############################################################

