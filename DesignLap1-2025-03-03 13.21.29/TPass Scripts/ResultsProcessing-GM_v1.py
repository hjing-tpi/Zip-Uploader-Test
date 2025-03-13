#Create a MERS Test Results Record, GEPICS Shipping Control Record and GSIP Quality Record using the GM EDI interface
#Format and return the Printed Label Text for TPass to send to a printer
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - object "testAppResults"
#   in  - object "productIdentification"
#   in  - COM object "gmEdiBuildResultsRecord" - GM EDI Interface pointer for creating GEPICS Shipping Control records, GSIP Quality Records and MERS Test Results records
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application log file
#   in  - method "GetConfigurationValue" - This is the method to get values set in the System Configuration file
#   out - string "printedLabelText"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

import clr
clr.AddReferenceToFileAndPath('.\\Tpi.TPass.Common.dll')
from Tpi.TPass.Common.JsonStore import TestResults
from System.Text.RegularExpressions import Regex

version = "1.0"
production = False
TPassLogger.Debug("Test Results Processing Script:  Product Primary Id = {0}", productIdentification.PrimaryId)
isSuccess = True

# Internal Functions
def IsTestFailed(testResults):

    if (testResults == str(TestResults.Fail) or testResults == str(TestResults.FatalFail) or
            testResults == str(TestResults.OperatorFail) or testResults == str(TestResults.OperatorAbort) or testResults == str(TestResults.SystemError)):
        return True
    else:
        return False

def SetFault(faultId):
    if (faultId):
        try:
            ediFaultId = int(faultId)
        except:
            TPassLogger.Warn("Test Results Processing Script:  Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = {0}", faultId)
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetFault() Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = " + faultId, True, True)
        else:
            if (ediFaultId >= 0 and ediFaultId <= 65535):
                try:
                    gmEdiBuildResultsRecord.HrSetFault(ediFaultId)
                    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetFault() Fault =  " + faultId, False, False)
                except Exception as inst:
                    TPassLogger.Warn("Test Results Processing Script:  Error HrSetFault().  Exception Occurred :{0}", inst)
                    MainTPassScripting.InterfaceUiLogger("GM EDI", "Error HrSetFault().  Exception Occurred = " + str(inst), True, False)
            else:
                TPassLogger.Warn("Test Results Processing Script:  Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = {0}", faultId)
                # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetFault() Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = " + faultId, True, True)

def SetUserValue(userValueId, userValue):
    if (userValueId and userValue):
        try:
            ediUserValueId = int(userValueId)
        except:
            TPassLogger.Warn("Test Results Processing Script:  User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = {0}, Value = {1}", userValueId, userValue)
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
            MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetUserValue() User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = " + userValueId + ", Value = " + userValue, True, True)
        else:
            try:
                if (ediUserValueId >= 1 and ediUserValueId <= 413):
                    ediUserValue = int(float(userValue))
                    if (ediUserValue >= -32768 and ediUserValue <= 32767):
                        gmEdiBuildResultsRecord.HrSetUserValue(ediUserValueId, ediUserValue)
                        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                        MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetUserValue() User Value Id = " + userValueId + ", Value = " + userValue, False, False)
                    else:
                        TPassLogger.Warn("Test Results Processing Script:  User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = {0}, Value = {1}", userValueId, userValue)
                        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                        MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetUserValue() User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = " + userValueId + ", Value = " + userValue, True, True)
                else:
                    TPassLogger.Warn("Test Results Processing Script:  User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = {0}, Value = {1}", userValueId, userValue)
                    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetUserValue() User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = " + userValueId + ", Value = " + userValue, True, True)
            except:
                TPassLogger.Warn("Test Results Processing Script:  User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = {0}, Value = {1}", userValueId, userValue)
                # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetUserValue() User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = " + userValueId + ", Value = " + userValue, True, True)


# Main Logic
try:

    gmEdiBuildResultsRecord.HrClearDateTime()
    gmEdiBuildResultsRecord.HrClearFaults()
    gmEdiBuildResultsRecord.HrClearUserValues()
    gmEdiBuildResultsRecord.ScClearShippingCtrl()
    gmEdiBuildResultsRecord.HrSetDpn(productIdentification.PrimaryId)
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetDpn() Primary ID = " + productIdentification.PrimaryId, False, False)
    # Get VIN from Build Data
    keyValuePairs = productIdentification.BuildData.Split(',')
    if keyValuePairs[0] != productIdentification.BuildData:
        for keyValuePair in keyValuePairs:
            key = keyValuePair.Split('=')[0].Trim().ToUpper()
            value = keyValuePair.Split('=')[1].ToUpper()
            if (key == "VIN"):
                gmEdiBuildResultsRecord.HrSetVinAndModelYear(value)
                MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetVinAndModelYear() VIN = " + value, False, False)
                break
    gmEdiBuildResultsRecord.HrSetTestPgmName(testAppResults.MainTestApplication.GmReporting.MersTestName)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetTestPgmName() value = " + testAppResults.MainTestApplication.GmReporting.MersTestName, False, False)
    gmEdiBuildResultsRecord.HrSetTestType(testAppResults.MainTestApplication.GmReporting.MersTestType)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetTestType() value = " + testAppResults.MainTestApplication.GmReporting.MersTestType, False, False)
    gmEdiBuildResultsRecord.HrSetTestPgmRev(testAppResults.MainTestApplication.GmReporting.MersTestPgmRev)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetTestPgmRev() value = " + str(testAppResults.MainTestApplication.GmReporting.MersTestPgmRev), False, False)
    gmEdiBuildResultsRecord.HrSetTestTableRev(testAppResults.MainTestApplication.GmReporting.MersTestTableRev)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetTestTableRev() value = " + str(testAppResults.MainTestApplication.GmReporting.MersTestTableRev), False, False)
    gmEdiBuildResultsRecord.HrSetTcaNumber(testAppResults.MainTestApplication.GmReporting.MersTca)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetTcaNumber() value = " + testAppResults.MainTestApplication.GmReporting.MersTca, False, False)
    gmEdiBuildResultsRecord.HrSetEngineType(testAppResults.MainTestApplication.GmReporting.MersEngineType)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetEngineType() value = " + testAppResults.MainTestApplication.GmReporting.MersEngineType, False, False)
    gmEdiBuildResultsRecord.HrSetDevIdBitMap(0, int(testAppResults.MainTestApplication.GmReporting.MersDeviceId, 0))
    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetDevIdBitMap() value = " + testAppResults.MainTestApplication.GmReporting.MersDeviceId, False, False)
    gmEdiBuildResultsRecord.HrSetUserValue(1, testAppResults.MainTestApplication.TestCycleResults.DurationMsec / 1000)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetUserValue() User Value Id = 1, Value = " + str(testAppResults.MainTestApplication.TestCycleResults.DurationMsec / 1000), False, False)

    if (str(testAppResults.MainTestApplication.TestCycleResults.TestResults) == str(TestResults.Fail)):
        overallTestResultsPass = False
    else:
        overallTestResultsPass = True

    if (overallTestResultsPass):
        gmEdiBuildResultsRecord.HrSetStaticPassFailFlag(ord('P'))
        MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetStaticPassFailFlag() value = P", False, False)
        gmEdiBuildResultsRecord.ScAddShipCode(testAppResults.MainTestApplication.GmReporting.GepicsShipCode, ord('P'))
        MainTPassScripting.InterfaceUiLogger("GM EDI", "ScAddShipCode() value = P, ShipCode = " + testAppResults.MainTestApplication.GmReporting.GepicsShipCode, False, False)
    else:
        gmEdiBuildResultsRecord.HrSetStaticPassFailFlag(ord('F'))
        MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetStaticPassFailFlag() value = F", False, False)
        gmEdiBuildResultsRecord.ScAddShipCode(testAppResults.MainTestApplication.GmReporting.GepicsShipCode, ord('F'))
        MainTPassScripting.InterfaceUiLogger("GM EDI", "ScAddShipCode() value = F, ShipCode = " + testAppResults.MainTestApplication.GmReporting.GepicsShipCode, False, False)

    if (testAppResults.MainTestApplication.TestCycleResults.Abort):
        gmEdiBuildResultsRecord.HrSetAbortedFlag(ord('Y'))
        MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetAbortedFlag() value = Y", False, False)


    # Set Faults and User Values
    for groupInx in range(len(testAppResults.MainTestApplication.TestCycle)):
        for subGroupInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx])):
            for testInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps)):
                testStep = testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps[testInx]
                if (IsTestFailed(str(testStep.TestStepResults.TestResults))):
                    SetFault(testStep.Fault.Id)

                # Test Step Specific Faults and User Values
                if (testStep.Name == "VoltageRange"):
                    for voltageRange in testStep.VoltageRanges:
                        for limit in voltageRange.Limits:
                            if (IsTestFailed(str(limit.TestStepResults.TestResults))):
                                SetFault(limit.Fault.Id)

                            if (str(limit.TestStepResults.TestResults) != str(TestResults.NotTested) and str(limit.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                                SetUserValue(limit.TestDataReporting.UpperLimitVolts, str(limit.UpperLimitVolts*100))
                                SetUserValue(limit.TestDataReporting.LowerLimitVolts, str(limit.LowerLimitVolts*100))
                                SetUserValue(limit.TestDataReporting.Samples, str(limit.TestData.Samples))
                                SetUserValue(limit.TestDataReporting.AvgChannelVoltageInRangeVolts, str(limit.TestData.AvgChannelVoltageInRangeVolts*100))
                                SetUserValue(limit.TestDataReporting.MaxChannelVoltageVolts, str(limit.TestData.MaxChannelVoltageVolts*100))
                                SetUserValue(limit.TestDataReporting.MinChannelVoltageVolts, str(limit.TestData.MinChannelVoltageVolts*100))
                                SetUserValue(limit.TestDataReporting.MaxTimeInPassWindowMsec, str(limit.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "SinkCurrentRangeBase" or testStep.Name == "SourceCurrentRangeBase" or testStep.Name == "SinkCurrentRangeDelta" or testStep.Name == "SourceCurrentRangeDelta"):
                    for currentRange in testStep.CurrentRanges:
                        if (IsTestFailed(str(currentRange.TestStepResults.TestResults))):
                            SetFault(currentRange.Fault.Id)

                        if (str(currentRange.TestStepResults.TestResults) != str(TestResults.NotTested) and str(currentRange.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetUserValue(currentRange.TestDataReporting.UpperLimitMamp, str(currentRange.UpperLimitMamp/100))
                            SetUserValue(currentRange.TestDataReporting.LowerLimitMamp, str(currentRange.LowerLimitMamp/100))
                            SetUserValue(currentRange.TestDataReporting.Samples, str(currentRange.TestData.Samples))
                            SetUserValue(currentRange.TestDataReporting.AvgCurrentInRangeMamp, str(currentRange.TestData.AvgCurrentInRangeMamp/100))
                            SetUserValue(currentRange.TestDataReporting.BaseCurrentMamp, str(currentRange.TestData.BaseCurrentMamp/100))
                            SetUserValue(currentRange.TestDataReporting.MaxCurrentMamp, str(currentRange.TestData.MaxCurrentMamp/100))
                            SetUserValue(currentRange.TestDataReporting.MinCurrentMamp, str(currentRange.TestData.MinCurrentMamp/100))
                            SetUserValue(currentRange.TestDataReporting.MaxTimeInPassWindowMsec, str(currentRange.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "SetCurrentLimits"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        SetUserValue(testStep.SetCurrentLimits.TestDataReporting.SourceLimitMamp, str(testStep.SetCurrentLimits.SourceLimitMamp/100))
                        SetUserValue(testStep.SetCurrentLimits.TestDataReporting.SinkLimitMamp, str(testStep.SetCurrentLimits.SinkLimitMamp/100))
                        SetUserValue(testStep.SetCurrentLimits.TestDataReporting.SourceLimitCounts, str(testStep.SetCurrentLimits.TestData.SourceLimitCounts/100))
                        SetUserValue(testStep.SetCurrentLimits.TestDataReporting.SinkLimitCounts, str(testStep.SetCurrentLimits.TestData.SinkLimitCounts/100))

                if (testStep.Name == "CanReceiveValidate"):
                    for canDataEntity in testStep.CanReceiveValidate.CanDataEntities:
                        if (IsTestFailed(str(canDataEntity.TestStepResults.TestResults))):
                            SetFault(canDataEntity.Fault.Id)

                if (testStep.Name == "CanSendReceiveValidate"):
                    for canDataEntity in testStep.CanSendReceiveValidate.CanDataEntities:
                        if (IsTestFailed(str(canDataEntity.TestStepResults.TestResults))):
                            SetFault(canDataEntity.Fault.Id)

                if (testStep.Name == "CanValidateSavedDtcData"):
                    for dtc in testStep.CanValidateSavedDtcData.Dtcs:
                        if (IsTestFailed(str(dtc.TestStepResults.TestResults))):
                            SetFault(dtc.Fault.Id)

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
                                            SetUserValue(userValueIds[0], userValues[0])
                                            SetUserValue(userValueIds[1], userValues[1])
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
                                            SetUserValue(userValueIds[0], userValues[0])
                                            SetUserValue(userValueIds[1], userValues[1])
                                    except Exception as inst:
                                        TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                        isSuccess = False
                            except Exception as inst:
                                TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                TPassLogger.Warn("Test Results Processing Script:  ProcessedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber)

                if (testStep.Name == "ModbusValidateVoltageRange"):
                    for channel in testStep.ModbusValidateVoltageRange.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetUserValue(channel.TestDataReporting.UpperLimitMVolt, str(channel.UpperLimitMVolt/100))
                            SetUserValue(channel.TestDataReporting.LowerLimitMVolt, str(channel.LowerLimitMVolt/100))
                            SetUserValue(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetUserValue(channel.TestDataReporting.MaxChannelVoltageMVolts, str(channel.TestData.MaxChannelVoltageMVolts/100))
                            SetUserValue(channel.TestDataReporting.MinChannelVoltageMVolts, str(channel.TestData.MinChannelVoltageMVolts/100))
                            SetUserValue(channel.TestDataReporting.AvgChannelVoltageInRangeMVolt, str(channel.TestData.AvgChannelVoltageInRangeMVolt/100))
                            SetUserValue(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "ModbusValidateVoltageRangeBase"):
                    for channel in testStep.ModbusValidateVoltageRangeBase.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetUserValue(channel.TestDataReporting.UpperLimitMVolt, str(channel.UpperLimitMVolt/100))
                            SetUserValue(channel.TestDataReporting.LowerLimitMVolt, str(channel.LowerLimitMVolt/100))
                            SetUserValue(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetUserValue(channel.TestDataReporting.MaxChannelVoltageMVolts, str(channel.TestData.MaxChannelVoltageMVolts/100))
                            SetUserValue(channel.TestDataReporting.MinChannelVoltageMVolts, str(channel.TestData.MinChannelVoltageMVolts/100))
                            SetUserValue(channel.TestDataReporting.BaseChannelVoltageMVolts, str(channel.TestData.BaseChannelVoltageMVolts/100))
                            SetUserValue(channel.TestDataReporting.AvgChannelVoltageInRangeMVolt, str(channel.TestData.AvgChannelVoltageInRangeMVolt/100))
                            SetUserValue(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "ModbusValidateVoltageRangeDelta"):
                    for channel in testStep.ModbusValidateVoltageRangeDelta.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetUserValue(channel.TestDataReporting.UpperLimitMVolt, str(channel.UpperLimitMVolt/100))
                            SetUserValue(channel.TestDataReporting.LowerLimitMVolt, str(channel.LowerLimitMVolt/100))
                            SetUserValue(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetUserValue(channel.TestDataReporting.MaxChannelVoltageMVolts, str(channel.TestData.MaxChannelVoltageMVolts/100))
                            SetUserValue(channel.TestDataReporting.MinChannelVoltageMVolts, str(channel.TestData.MinChannelVoltageMVolts/100))
                            SetUserValue(channel.TestDataReporting.BaseChannelVoltageMVolts, str(channel.TestData.BaseChannelVoltageMVolts/100))
                            SetUserValue(channel.TestDataReporting.AvgChannelVoltageInRangeMVolt, str(channel.TestData.AvgChannelVoltageInRangeMVolt/100))
                            SetUserValue(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "MeterValidateVoltageRange"):
                    for channel in testStep.MeterValidateVoltageRange.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetUserValue(channel.TestDataReporting.UpperLimitVolt, str(channel.UpperLimitVolt))
                            SetUserValue(channel.TestDataReporting.LowerLimitVolt, str(channel.LowerLimitVolt))
                            SetUserValue(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetUserValue(channel.TestDataReporting.MaxChannelVoltageVolts, str(channel.TestData.MaxChannelVoltageVolts))
                            SetUserValue(channel.TestDataReporting.MinChannelVoltageVolts, str(channel.TestData.MinChannelVoltageVolts))
                            SetUserValue(channel.TestDataReporting.AvgChannelVoltageInRangeVolt, str(channel.TestData.AvgChannelVoltageInRangeVolt))
                            SetUserValue(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                if (testStep.Name == "MeterValidateFrequencyRange"):
                    for channel in testStep.MeterValidateFrequencyRange.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id)

                        if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetUserValue(channel.TestDataReporting.UpperLimitHz, str(channel.UpperLimitHz))
                            SetUserValue(channel.TestDataReporting.LowerLimitHz, str(channel.LowerLimitHz))
                            SetUserValue(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            SetUserValue(channel.TestDataReporting.MaxChannelFrequencyHz, str(channel.TestData.MaxChannelFrequencyHz))
                            SetUserValue(channel.TestDataReporting.MinChannelFrequencyHz, str(channel.TestData.MinChannelFrequencyHz))
                            SetUserValue(channel.TestDataReporting.AvgChannelFrequencyInRangeHz, str(channel.TestData.AvgChannelFrequencyInRangeHz))
                            SetUserValue(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

    # Create MERS Record
    if (GetConfigurationValue("Partner Interfaces", "Create Mers Reporting Record", False)): 
        gmEdiBuildResultsRecord.HrCreateHistoryRecord()
        TPassLogger.Info("Test Results Processing Script:  Mers Reporting Record Created")
        MainTPassScripting.InterfaceUiLogger("GM EDI", "HrCreateHistoryRecord()", False, False)
    else:
        TPassLogger.Info("Test Results Processing Script:  System Parameter 'Create Mers Reporting Record' = False, No Mers Reporting Record Created")
        MainTPassScripting.InterfaceUiLogger("GM EDI", "System Parameter 'Create Mers Reporting Record' = False, No Mers Reporting Record Created", False, False)

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating MERS History Record.  Exception Occurred :{0}", inst)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "Error Creating MERS History Record.  Exception Occurred = " + str(inst), True, True)
    isSuccess = False

# Create GEPICS SHIP Record
try:
    if (GetConfigurationValue("Partner Interfaces", "Create Gepics Ship Record", False)): 
        gmEdiBuildResultsRecord.ScCreateShippingCtrlRecord()
        TPassLogger.Info("Test Results Processing Script:  GEPICS Shipping Record Created")
        MainTPassScripting.InterfaceUiLogger("GM EDI", "ScCreateShippingCtrlRecord()", False, False)
    else:
        TPassLogger.Info("Test Results Processing Script:  System Parameter 'Create Gepics Ship Record' = False, No Gepics Ship Record Created")
        MainTPassScripting.InterfaceUiLogger("GM EDI", "System Parameter 'Create Gepics Ship Record' = False, No Gepics Ship Record Created", False, False)

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating GEPICS SHIPPING Record.  Exception Occurred :{0}", inst)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "Error Creating GEPICS SHIPPING Record.  Exception Occurred = " + str(inst), True, True)
    isSuccess = False

# Create GSIP Record
try:     
    if (GetConfigurationValue("Partner Interfaces", "Create Gsip Quality Record", False)): 
        gmEdiBuildResultsRecord.GrCreateGsipRecord()
        TPassLogger.Info("Test Results Processing Script:  GSIP Quality Record Created")
        MainTPassScripting.InterfaceUiLogger("GM EDI", "GrCreateGsipRecord()", False, False)
    else:
        TPassLogger.Info("Test Results Processing Script:  System Parameter Create Gsip Quality Record = False, No Gsip Quality Record Created")
        MainTPassScripting.InterfaceUiLogger("GM EDI", "System Parameter Create Gsip Quality Record = False, No Gsip Quality Record Created", False, False)

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating GSIP Quality Record.  Exception Occurred :{0}", inst)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "Error Creating GSIP Quality Record.  Exception Occurred = " + str(inst), True, True)
    isSuccess = False

# Create Printed Label Text to pass back to TPass for printing
try:
    printedLabelText = "Test Label Text\n\r" + "Line 2"

    TPassLogger.Info("Test Results Processing Script:  Product Primary ID = {0}, Printed Label Text = {1}", productIdentification.PrimaryId, printedLabelText )

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Test Label Text.  Exception Occurred :{0}", inst)
    isSuccess = False

TPassLogger.Info("Test Results Processing Script:  Is Success = {0}", isSuccess)





############################################################
# Change History
############################################################
#	Date: 01012019
#	Version: 1.0
#	Change: Initial Version
############################################################

