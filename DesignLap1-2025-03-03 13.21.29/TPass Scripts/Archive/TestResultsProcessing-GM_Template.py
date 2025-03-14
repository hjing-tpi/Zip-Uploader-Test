#Create a MERS Results Record, GEPICS Shipping Record and GSIP Quality Record using the GM EDI interface.
#Format and return the Printed Label Text for TPass to send to a printer
#This Script is expected to set the out parameters below
#TPass Objects Passed In/Returned
#   in - object "testAppResults"
#   in - object "productIdentification"
#   in - COM object "gmEdiBuildResultsRecord"
#   in - Function "TPassLogger"
#   in - Function "GetConfigurationValue"
#   out - string "printedLabelText"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

import clr
clr.AddReferenceToFileAndPath('.\\Tpi.TPass.Common.dll')
from Tpi.TPass.Common.JsonStore import TestResults
from System.Text.RegularExpressions import Regex

#System.Diagnostics.Debugger.Break();

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
        else:
            if (ediFaultId >= 0 and ediFaultId <= 65535):
                gmEdiBuildResultsRecord.HrSetFault(ediFaultId)
            else:
                TPassLogger.Warn("Test Results Processing Script:  Fault Id Invalid and not saved.  Valid range is 0-65535.  Fault Id = {0}", faultId)

def SetUserValue(userValueId, userValue):
    if (userValueId and userValue):
        try:
            ediUserValueId = int(userValueId)
        except:
            TPassLogger.Warn("Test Results Processing Script:  User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = {0}, Value = {1}", userValueId, userValue)
        else:
            try:
                if (ediUserValueId >= 1 and ediUserValueId <= 413):
                    ediUserValue = int(float(userValue))
                    if (ediUserValue >= -32768 and ediUserValue <= 32767):
                        gmEdiBuildResultsRecord.HrSetUserValue(ediUserValueId, ediUserValue)
                    else:
                        TPassLogger.Warn("Test Results Processing Script:  User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = {0}, Value = {1}", userValueId, userValue)
                else:
                    TPassLogger.Warn("Test Results Processing Script:  User Value Id Invalid and not saved.  Valid range is 1 - 413.  User Value Id = {0}, Value = {1}", userValueId, userValue)
            except:
                TPassLogger.Warn("Test Results Processing Script:  User Value Invalid and not saved.  Valid range is -32,768 to 32,767.  User Value Id = {0}, Value = {1}", userValueId, userValue)


# Main Logic
try:
    gmEdiBuildResultsRecord.HrClearDateTime()
    gmEdiBuildResultsRecord.HrClearFaults()
    gmEdiBuildResultsRecord.HrClearUserValues()
    gmEdiBuildResultsRecord.ScClearShippingCtrl()
    gmEdiBuildResultsRecord.HrSetDpn(productIdentification.PrimaryId)
    gmEdiBuildResultsRecord.HrSetVinAndModelYear(productIdentification.Vin)
    gmEdiBuildResultsRecord.HrSetTestPgmName(testAppResults.MainTestApplication.GmReporting.MersTestName)
    gmEdiBuildResultsRecord.HrSetTestType(testAppResults.MainTestApplication.GmReporting.MersTestType)
    gmEdiBuildResultsRecord.HrSetTestPgmRev(testAppResults.MainTestApplication.GmReporting.MersTestPgmRev)
    gmEdiBuildResultsRecord.HrSetTestTableRev(testAppResults.MainTestApplication.GmReporting.MersTestTableRev)
    gmEdiBuildResultsRecord.HrSetTcaNumber(testAppResults.MainTestApplication.GmReporting.MersTca)
    gmEdiBuildResultsRecord.HrSetEngineType(testAppResults.MainTestApplication.GmReporting.MersEngineType)
    gmEdiBuildResultsRecord.HrSetDevIdBitMap(0, int(testAppResults.MainTestApplication.GmReporting.MersDeviceId, 0))
    gmEdiBuildResultsRecord.HrSetUserValue(1, testAppResults.MainTestApplication.TestCycleResults.DurationMsec / 1000)

    #pResultsRec->HrSetRetestFlag(‘Y’);
    #pResultsRec->HrSetTimeOutFlag(‘Y’);
    #pResultsRec->HrSetDateTime(_bstr_t("092501"), _bstr_t("135405"));
    #pResultsRec->HrSetCsn(_bstr_t("1GA1234567 "));
    #pResultsRec->HrSetOperatorNickName(_bstr_t("OPER1"));
    #pResultsRec->HrSetOptionString(_bstr_t("PERG"));
    #pResultsRec->HrSetProductionYear(_bstr_t("2015"));

    if (str(testAppResults.MainTestApplication.TestCycleResults.TestResults) == str(TestResults.Fail)):
        overallTestResultsPass = False
    else:
        overallTestResultsPass = True

    if (overallTestResultsPass):
        gmEdiBuildResultsRecord.HrSetStaticPassFailFlag(ord('P'))
        gmEdiBuildResultsRecord.ScAddShipCode(testAppResults.MainTestApplication.GmReporting.GepicsShipCode, ord('P'))
    else:
        gmEdiBuildResultsRecord.HrSetStaticPassFailFlag(ord('F'))
        gmEdiBuildResultsRecord.ScAddShipCode(testAppResults.MainTestApplication.GmReporting.GepicsShipCode, ord('F'))

    if (testAppResults.MainTestApplication.TestCycleResults.Abort):
        gmEdiBuildResultsRecord.HrSetAbortedFlag(ord('Y'))


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
    else:
        TPassLogger.Info("Test Results Processing Script:  System Parmeter 'Create Mers Reporting Record' = False, No Mers Reporting Record Created")

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating MERS History Record.  Exception Occurred :{0}", inst)
    isSuccess = False

# Create GEPICS SHIP Record
try:
    if (GetConfigurationValue("Partner Interfaces", "Create Gepics Ship Record", False)): 
        gmEdiBuildResultsRecord.ScCreateShippingCtrlRecord()
        TPassLogger.Info("Test Results Processing Script:  GEPICS Shipping Record Created")
    else:
        TPassLogger.Info("Test Results Processing Script:  'System Parmeter Create Gepics Ship Record' = False, No Gepics Ship Record Created")

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating GEPICS SHIPPING Record.  Exception Occurred :{0}", inst)
    isSuccess = False

# Create GSIP Record
try:     
    if (GetConfigurationValue("Partner Interfaces", "Create Gsip Quality Record", False)): 
        gmEdiBuildResultsRecord.GrCreateGsipRecord()
        TPassLogger.Info("Test Results Processing Script:  GSIP Quality Record Created")
    else:
        TPassLogger.Info("Test Results Processing Script:  System Parmeter Create Gsip Quality Record = False, No Gsip Quality Record Created")

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating GSIP Quality Record Record.  Exception Occurred :{0}", inst)
    isSuccess = False

# Create Printed Label Text to pass back to TPass for printing
try:
    printedLabelText = "Test Label Text"

    TPassLogger.Info("Test Results Processing Script:  Product Primary ID = {0}, CSN = {1}, Printed Label Text = {2}", productIdentification.PrimaryId, productIdentification.CurrentSequenceNumber, printedLabelText )

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

