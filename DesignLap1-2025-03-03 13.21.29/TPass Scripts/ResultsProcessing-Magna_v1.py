#Create a Magna Test Results Record
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
from System import DateTime

version = "0.2"
production = False
TPassLogger.Debug("Test Results Processing Script:  Product Primary Id = {0}", productIdentification.PrimaryId)
TPassLogger.Debug("Test Results Processing Script:  Product Secondary Id = {0}", productIdentification.SecondaryId)
isSuccess = True

#########################################################################################################################################
# Application Engineer:  Set Station Number to be written to the printed label
#
stationNumber = "01" 
maxNumberFaultsOnPrintedLabel = 10
printPassLabel = False
#
#########################################################################################################################################

overallTestResultsPass = False
printedFaultText = ""
screenLabelFaultText = ""
numberFaultsAdded = 0
totalNumberOfFaults = 0

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
        screenLabelFaultText = screenLabelFaultText + faultId.zfill(5) + " - " + faultDescription + "\r\n"
        if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
            numberFaultsAdded = numberFaultsAdded + 1
            printedFaultText = printedFaultText + faultId.zfill(5) + "," + faultDescription + "\r\n"
    except:
        TPassLogger.Warn("Test Results Processing Script:  Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = {0}", faultId)
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("Magna", "Results Processing Script:  SetFault() Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = " + faultId, True, True)


def SetProcessData(userValueId, userValue):
    #No Process Data yet
    userValueId = ""
    # if (userValueId and userValue):
        # try:
            # ediUserValueId = int(userValueId)
        # except:
            # TPassLogger.Warn("Test Results Processing Script:  User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = {0}, Value = {1}", userValueId, userValue)
            # # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            # MainTPassScripting.InterfaceUiLogger("Magna", "HrSetUserValue() User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = " + userValueId + ", Value = " + userValue, True, True)
        # else:
            # try:
                # if (ediUserValueId >= 1 and ediUserValueId <= 413):
                    # ediUserValue = int(float(userValue))
                    # if (ediUserValue >= -32768 and ediUserValue <= 32767):
                        # gmEdiBuildResultsRecord.HrSetUserValue(ediUserValueId, ediUserValue)
                        # # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                        # MainTPassScripting.InterfaceUiLogger("Magna", "HrSetUserValue() User Value Id = " + userValueId + ", Value = " + userValue, False, False)
                    # else:
                        # TPassLogger.Warn("Test Results Processing Script:  User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = {0}, Value = {1}", userValueId, userValue)
                        # # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                        # MainTPassScripting.InterfaceUiLogger("Magna", "HrSetUserValue() User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = " + userValueId + ", Value = " + userValue, True, True)
                # else:
                    # TPassLogger.Warn("Test Results Processing Script:  User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = {0}, Value = {1}", userValueId, userValue)
                    # # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                    # MainTPassScripting.InterfaceUiLogger("Magna", "HrSetUserValue() User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = " + userValueId + ", Value = " + userValue, True, True)
            # except:
                # TPassLogger.Warn("Test Results Processing Script:  User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = {0}, Value = {1}", userValueId, userValue)
                # # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                # MainTPassScripting.InterfaceUiLogger("Magna", "HrSetUserValue() User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = " + userValueId + ", Value = " + userValue, True, True)



# Main Logic
try:
    printedLabelText = str(DateTime.Now) + "\r\n"
    printedLabelText = printedLabelText + "Secondary ID:" + productIdentification.SecondaryId + "\r\n"
    printedLabelText = printedLabelText + "STN:" + stationNumber + " Seat Type:" + productIdentification.PrimaryId + "\r\n"
    screenLabelText = str(DateTime.Now) + "\r\n"
    builddataCsn = ""
    builddataMd = ""
        

    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("Magna", "Results Processing Script:  Primary ID = " + productIdentification.PrimaryId, False, False)
    # Get VIN from Build Data
    keyValuePairs = productIdentification.BuildData.Split(',')
    # if keyValuePairs[0] != productIdentification.BuildData:
        # for keyValuePair in keyValuePairs:
            # key = keyValuePair.Split('=')[0].Trim().ToUpper()
            # value = keyValuePair.Split('=')[1].ToUpper()
            # if (key == "VIN"):
                # gmEdiBuildResultsRecord.HrSetVinAndModelYear(value)
                # MainTPassScripting.InterfaceUiLogger("Magna", "HrSetVinAndModelYear() VIN = " + value, False, False)
                # break
        # for keyValuePair in keyValuePairs:
            # key = keyValuePair.Split('=')[0].Trim().ToUpper()
            # value = keyValuePair.Split('=')[1].ToUpper()
            # if (key == "CSN"):
                # builddataCsn = value
                # MainTPassScripting.InterfaceUiLogger("Magna", "CSN = " + value, False, False)
                # break
        # for keyValuePair in keyValuePairs:
            # key = keyValuePair.Split('=')[0].Trim().ToUpper()
            # value = keyValuePair.Split('=')[1].ToUpper()
            # if (key == "MD"):
                # builddataMd = value
                # MainTPassScripting.InterfaceUiLogger("Magna", "MD = " + value, False, False)
                # break

    screenLabelText = screenLabelText + "STN:" + stationNumber + "    " + " Seat Type: <b>" + productIdentification.PrimaryId + "</b>    " + "Secondary: " + productIdentification.SecondaryId + "\r\n"

    if (str(testAppResults.MainTestApplication.TestCycleResults.TestResults) == str(TestResults.Fail)):
        overallTestResultsPass = False
        printedLabelText = printedLabelText + "Test Status: Failed" + "\r\n"
    else:
        printedLabelText = printedLabelText + "Test Status: Passed" + "\r\n"
        overallTestResultsPass = True

    if (testAppResults.MainTestApplication.TestCycleResults.Abort):
        SetFault("", "TEST ABORTED")


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
                        
                if (testStep.Name == "FamSendPvmSeatTestString"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        #Add PVM Detail to printed label
                        if (str(testStep.TestStepResults.TestResults) != str(TestResults.Pass)):
                            if (testStep.Fault.Detail):
                                screenLabelFaultText = screenLabelFaultText + "   " + testStep.Fault.Detail + "\r\n"
                            if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                                if (testStep.Fault.Detail):
                                    numberFaultsAdded = numberFaultsAdded + 1
                                    printedFaultText = printedFaultText + "   " + testStep.Fault.Detail + "\r\n"

                if (testStep.Name == "FamSendPvmTrigger"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        #Add PVM Detail to printed label
                        if (str(testStep.TestStepResults.TestResults) != str(TestResults.Pass)):
                            if (testStep.Fault.Detail):
                                screenLabelFaultText = screenLabelFaultText + "   " + testStep.Fault.Detail + "\r\n"
                            if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                                if (testStep.Fault.Detail):
                                    numberFaultsAdded = numberFaultsAdded + 1
                                    printedFaultText = printedFaultText + "   " + testStep.Fault.Detail + "\r\n"

                if (testStep.Name == "FamSendPvmCanPressure"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        #Add PVM Detail to printed label
                        if (str(testStep.TestStepResults.TestResults) != str(TestResults.Pass)):
                            if (testStep.Fault.Detail):
                                screenLabelFaultText = screenLabelFaultText + "   " + testStep.Fault.Detail + "\r\n"
                            if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                                if (testStep.Fault.Detail):
                                    numberFaultsAdded = numberFaultsAdded + 1
                                    printedFaultText = printedFaultText + "   " + testStep.Fault.Detail + "\r\n"

    ####################
    # Add new test steps
    ####################

    # Create Magna Record
    # if (SystemConfigurationValue.PartnerInterfaces.GmEdi.CreateMersReportingRecord): 
        # gmEdiBuildResultsRecord.HrCreateHistoryRecord()
        # TPassLogger.Info("Test Results Processing Script:  Mers Reporting Record Created")
        # MainTPassScripting.InterfaceUiLogger("Magna", "HrCreateHistoryRecord()", False, False)
    # else:
        # TPassLogger.Info("Test Results Processing Script:  System Parameter 'Create Mers Reporting Record' = False, No Mers Reporting Record Created")
        # MainTPassScripting.InterfaceUiLogger("Magna", "System Parameter 'Create Mers Reporting Record' = False, No Mers Reporting Record Created", False, False)

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Magna Test Results Record.  Exception Occurred :{0}", inst)
    MainTPassScripting.InterfaceUiLogger("Magna", "Results Processing Script:  Error Creating Magna Test Results Record.  Exception Occurred = " + str(inst), True, True)
    isSuccess = False


# Create Screen Label Text to pass back to TPass for displaying on the Pass/Fail screens
try:
    if (overallTestResultsPass):
        screenLabelText = "<fontsize:32>" + screenLabelText + "<b>\r\n\r\nPASSED\r\nPASSED\r\nPASSED\r\nPASSED" + "</b></fontsize>"
    else:
        screenLabelText = "<fontsize:32>" + screenLabelText + "</fontsize>" + "<fontsize:24>\r\n<b>FLTS:" + str(totalNumberOfFaults) + "</b></fontsize>" + "<fontsize:32>\r\n" + screenLabelFaultText + "</fontsize>"
        #screenLabelText = "<b>The reason</b> <fontsize:30>why this failed</fontsize> <fontsize:12><color:green>is because somebody turned</color> the light off... duh!</fontsize>"

    MainTPassScripting.UpdateTestResultsScreenCustomText(screenLabelText)
    TPassLogger.Debug("Test Results Processing Script:  Product Primary ID = {0}, Screen Custom Label Text = {1}", productIdentification.PrimaryId, screenLabelText )

except:
    TPassLogger.Warn("Test Results Processing Script:  UpdateTestResultsScreenCustomText being called but functionality is not implemented until TPass v1.4.0.3 or later")
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("Magna", "Results Processing Script:  UpdateTestResultsScreenCustomText being called but functionality is not implemented until TPass v1.4.0.3 or later", True, False)

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
#   Date: 03092023
#   Version: 0.2
#   Change: Added displaying fault detail for all PVM Test Steps
#   Date: 02282023
#   Version: 0.1
#   Change: Initial Version
############################################################

