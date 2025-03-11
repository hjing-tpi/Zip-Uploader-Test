#Process the Test Results data sending to the Plants MES system.  Also Print the Test Results Label if required
#
#This Script is expected to set the out parameters below
#TPass Objects Passed In/Returned
#   in - object "testAppResults" - Contains all the test cycle results of the current product tested
#   in - object "productIdentification" - Contains all the attributes of the current product tested
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in - Method "GetConfigurationValue" - This is used to retrieve Tool System Configuration parameters
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
isSuccess = True

TPassLogger.Debug("Test Results Processing Script:  Product Primary Id = {0}", productIdentification.PrimaryId)
#MainTPassScripting.InterfaceUiLogger("MES", "Test Results Processing", True, True)
if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Scan):
    TPassLogger.Debug("Test Results Processing Script - Trigger Type is Scan")
elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ContinuousMode):
    TPassLogger.Debug("Test Results Processing Script - Trigger Type is ContinuousMode")

# Internal Functions
def IsTestFailed(testResults):

    if (testResults == str(TestResults.Fail) or testResults == str(TestResults.FatalFail) or
            testResults == str(TestResults.OperatorFail) or testResults == str(TestResults.OperatorAbort) or testResults == str(TestResults.SystemError)):
        return True
    else:
        return False


# Main Logic
try:

    # Parse the test results and send data to the plants MES system
 
    if (str(testAppResults.MainTestApplication.TestCycleResults.TestResults) == str(TestResults.Fail)):
        overallTestResultsPass = False
    else:
        overallTestResultsPass = True

    if (testAppResults.MainTestApplication.TestCycleResults.Abort):
        abortFlag = True

    # # Set Faults and Process Data
    # for groupInx in range(len(testAppResults.MainTestApplication.TestCycle)):
        # for subGroupInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx])):
            # for testInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps)):
                # testStep = testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps[testInx]
                # if (IsTestFailed(str(testStep.TestStepResults.TestResults))):
                    # #SetFault(testStep.Fault.Id)

                # # Test Step Specific Faults and User Values
                # if (testStep.Name == "VoltageRange"):
                    # for voltageRange in testStep.VoltageRanges:
                        # for limit in voltageRange.Limits:
                            # if (IsTestFailed(str(limit.TestStepResults.TestResults))):
                                # # SetFault(limit.Fault.Id)

                            # if (str(limit.TestStepResults.TestResults) != str(TestResults.NotTested) and str(limit.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                                # # SetUserValue(limit.TestDataReporting.UpperLimitVolts, str(limit.UpperLimitVolts*100))
                                # # SetUserValue(limit.TestDataReporting.LowerLimitVolts, str(limit.LowerLimitVolts*100))
                                # # SetUserValue(limit.TestDataReporting.Samples, str(limit.TestData.Samples))
                                # # SetUserValue(limit.TestDataReporting.AvgChannelVoltageInRangeVolts, str(limit.TestData.AvgChannelVoltageInRangeVolts*100))
                                # # SetUserValue(limit.TestDataReporting.MaxChannelVoltageVolts, str(limit.TestData.MaxChannelVoltageVolts*100))
                                # # SetUserValue(limit.TestDataReporting.MinChannelVoltageVolts, str(limit.TestData.MinChannelVoltageVolts*100))
                                # # SetUserValue(limit.TestDataReporting.MaxTimeInPassWindowMsec, str(limit.TestData.MaxTimeInPassWindowMsec/1000))

                # if (testStep.Name == "SinkCurrentRangeBase" or testStep.Name == "SourceCurrentRangeBase" or testStep.Name == "SinkCurrentRangeDelta" or testStep.Name == "SourceCurrentRangeDelta"):
                    # for currentRange in testStep.CurrentRanges:
                        # if (IsTestFailed(str(currentRange.TestStepResults.TestResults))):
                            # # SetFault(currentRange.Fault.Id)

                        # if (str(currentRange.TestStepResults.TestResults) != str(TestResults.NotTested) and str(currentRange.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            # # SetUserValue(currentRange.TestDataReporting.UpperLimitMamp, str(currentRange.UpperLimitMamp/100))
                            # # SetUserValue(currentRange.TestDataReporting.LowerLimitMamp, str(currentRange.LowerLimitMamp/100))
                            # # SetUserValue(currentRange.TestDataReporting.Samples, str(currentRange.TestData.Samples))
                            # # SetUserValue(currentRange.TestDataReporting.AvgCurrentInRangeMamp, str(currentRange.TestData.AvgCurrentInRangeMamp/100))
                            # # SetUserValue(currentRange.TestDataReporting.BaseCurrentMamp, str(currentRange.TestData.BaseCurrentMamp/100))
                            # # SetUserValue(currentRange.TestDataReporting.MaxCurrentMamp, str(currentRange.TestData.MaxCurrentMamp/100))
                            # # SetUserValue(currentRange.TestDataReporting.MinCurrentMamp, str(currentRange.TestData.MinCurrentMamp/100))
                            # # SetUserValue(currentRange.TestDataReporting.MaxTimeInPassWindowMsec, str(currentRange.TestData.MaxTimeInPassWindowMsec/1000))

                # if (testStep.Name == "SetCurrentLimits"):
                    # if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        # # SetUserValue(testStep.SetCurrentLimits.TestDataReporting.SourceLimitMamp, str(testStep.SetCurrentLimits.SourceLimitMamp/100))
                        # # SetUserValue(testStep.SetCurrentLimits.TestDataReporting.SinkLimitMamp, str(testStep.SetCurrentLimits.SinkLimitMamp/100))
                        # # SetUserValue(testStep.SetCurrentLimits.TestDataReporting.SourceLimitCounts, str(testStep.SetCurrentLimits.TestData.SourceLimitCounts/100))
                        # # SetUserValue(testStep.SetCurrentLimits.TestDataReporting.SinkLimitCounts, str(testStep.SetCurrentLimits.TestData.SinkLimitCounts/100))

                # if (testStep.Name == "CanReceiveValidate"):
                    # for canDataEntity in testStep.CanReceiveValidate.CanDataEntities:
                        # if (IsTestFailed(str(canDataEntity.TestStepResults.TestResults))):
                            # # SetFault(canDataEntity.Fault.Id)

                # if (testStep.Name == "CanSendReceiveValidate"):
                    # for canDataEntity in testStep.CanSendReceiveValidate.CanDataEntities:
                        # if (IsTestFailed(str(canDataEntity.TestStepResults.TestResults))):
                            # # SetFault(canDataEntity.Fault.Id)

                # if (testStep.Name == "CanValidateSavedDtcData"):
                    # for dtc in testStep.CanValidateSavedDtcData.Dtcs:
                        # if (IsTestFailed(str(dtc.TestStepResults.TestResults))):
                            # SetFault(dtc.Fault.Id)

                # if (testStep.Name == "CanValidatePartNumber"):
                    # if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        # if (testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber):
                            # try:
                                # userValueIds = testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber.Split(',')
                                # if len(userValueIds) != 2:
                                    # TPassLogger.Error("Test Results Processing Script:  BroadcastedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber)
                                # else:
                                    # try:
                                        # userValues = testStep.CanValidatePartNumber.TestData.BroadcastedPartNumber
                                        # if (not Regex.IsMatch(userValues, "^\d{8}$")):
                                            # TPassLogger.Warn("Test Results Processing Script:  BroadcastedPartNumber format must be 8 digits.  Value = {0}", testStep.CanValidatePartNumber.TestData.BroadcastedPartNumber)
                                        # else:
                                            # userValues = [userValues[i:i+4] for i in range(0, len(userValues), 4)]
                                            # # SetUserValue(userValueIds[0], userValues[0])
                                            # # SetUserValue(userValueIds[1], userValues[1])
                                    # except Exception as inst:
                                        # TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                        # isSuccess = False
                            # except Exception as inst:
                                # TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                # TPassLogger.Warn("Test Results Processing Script:  BroadcastedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber)
 
                        # if (testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber):
                            # try:
                                # userValueIds = testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber.Split(',')
                                # if len(userValueIds) != 2:
                                    # TPassLogger.Error("Test Results Processing Script:  ProcessedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber)
                                # else:
                                    # try:
                                        # userValues = testStep.CanValidatePartNumber.TestData.ProcessedPartNumber
                                        # if (not Regex.IsMatch(userValues, "^\d{8}$")):
                                            # TPassLogger.Warn("Test Results Processing Script:  ProcessedPartNumber format must be 8 digits.  Value = {0}", testStep.CanValidatePartNumber.TestData.ProcessedPartNumber)
                                        # else:
                                            # userValues = [userValues[i:i+4] for i in range(0, len(userValues), 4)]
                                            # # SetUserValue(userValueIds[0], userValues[0])
                                            # # SetUserValue(userValueIds[1], userValues[1])
                                    # except Exception as inst:
                                        # TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                        # isSuccess = False
                            # except Exception as inst:
                                # TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                # TPassLogger.Warn("Test Results Processing Script:  ProcessedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber)

                # if (testStep.Name == "ModbusValidateVoltageRange"):
                    # for channel in testStep.ModbusValidateVoltageRange.Channels:
                        # if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            # # SetFault(channel.Fault.Id)

                        # if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            # # SetUserValue(channel.TestDataReporting.UpperLimitMVolt, str(channel.UpperLimitMVolt/100))
                            # # SetUserValue(channel.TestDataReporting.LowerLimitMVolt, str(channel.LowerLimitMVolt/100))
                            # # SetUserValue(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            # # SetUserValue(channel.TestDataReporting.MaxChannelVoltageMVolts, str(channel.TestData.MaxChannelVoltageMVolts/100))
                            # # SetUserValue(channel.TestDataReporting.MinChannelVoltageMVolts, str(channel.TestData.MinChannelVoltageMVolts/100))
                            # # SetUserValue(channel.TestDataReporting.AvgChannelVoltageInRangeMVolt, str(channel.TestData.AvgChannelVoltageInRangeMVolt/100))
                            # # SetUserValue(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                # if (testStep.Name == "MeterValidateVoltageRange"):
                    # for channel in testStep.MeterValidateVoltageRange.Channels:
                        # if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            # # SetFault(channel.Fault.Id)

                        # if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            # # SetUserValue(channel.TestDataReporting.UpperLimitVolt, str(channel.UpperLimitVolt))
                            # # SetUserValue(channel.TestDataReporting.LowerLimitVolt, str(channel.LowerLimitVolt))
                            # # SetUserValue(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            # # SetUserValue(channel.TestDataReporting.MaxChannelVoltageVolts, str(channel.TestData.MaxChannelVoltageVolts))
                            # # SetUserValue(channel.TestDataReporting.MinChannelVoltageVolts, str(channel.TestData.MinChannelVoltageVolts))
                            # # SetUserValue(channel.TestDataReporting.AvgChannelVoltageInRangeVolt, str(channel.TestData.AvgChannelVoltageInRangeVolt))
                            # # SetUserValue(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

                # if (testStep.Name == "MeterValidateFrequencyRange"):
                    # for channel in testStep.MeterValidateFrequencyRange.Channels:
                        # if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            # # SetFault(channel.Fault.Id)

                        # if (str(channel.TestStepResults.TestResults) != str(TestResults.NotTested) and str(channel.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            # # SetUserValue(channel.TestDataReporting.UpperLimitHz, str(channel.UpperLimitHz))
                            # # SetUserValue(channel.TestDataReporting.LowerLimitHz, str(channel.LowerLimitHz))
                            # # SetUserValue(channel.TestDataReporting.Samples, str(channel.TestData.Samples))
                            # # SetUserValue(channel.TestDataReporting.MaxChannelFrequencyHz, str(channel.TestData.MaxChannelFrequencyHz))
                            # # SetUserValue(channel.TestDataReporting.MinChannelFrequencyHz, str(channel.TestData.MinChannelFrequencyHz))
                            # # SetUserValue(channel.TestDataReporting.AvgChannelFrequencyInRangeHz, str(channel.TestData.AvgChannelFrequencyInRangeHz))
                            # # SetUserValue(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestData.MaxTimeInPassWindowMsec/1000))

    # Create MES Record
    TPassLogger.Info("Test Results Processing Script:  MES Reporting Record Created")

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating MES Reporting Record.  Exception Occurred :{0}", inst)
    isSuccess = False


# Create Printed Label Text to pass back to TPass for printing
try:
    printedLabelText = "Test Label Text"

    TPassLogger.Info("Test Results Processing Script:  Product Primary ID = {0}, Printed Label Text = {1}", productIdentification.PrimaryId, printedLabelText )

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Test Label Text.  Exception Occurred :{0}", inst)
    isSuccess = False

TPassLogger.Info("Test Results Processing Script:  Is Success = {0}", isSuccess)





############################################################
# Change History
############################################################
#   Date: 01012019
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################

