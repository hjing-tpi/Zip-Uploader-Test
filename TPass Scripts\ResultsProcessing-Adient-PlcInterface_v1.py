#Create a Adient Test Results Record and format and return the Printed Label Text for TPass to send to a printer
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
from System import DateTime

version = "3.0"
production = False
TPassLogger.Debug("Test Results Processing Script:  Product Primary Id = {0}", productIdentification.PrimaryId)
TPassLogger.Debug("Test Results Processing Script:  Product Secondary Id = {0}", productIdentification.SecondaryId)
isSuccess = True

#########################################################################################################################################
# Application Engineer:  
#
printPassLabel = False

resultsFile = "C:\TPass\Data Outgoing\Results.txt"
maxNumberFaultsToSave = 10

initialFormat = "Initial Format, 06"
plantText = "PLT2_LH_EOL"
testSiteText = "EOL_DRIVER_P2"

#
#########################################################################################################################################

testerId = "0"                                      # Will be read from the \TPass\Support Files\SID.txt file
testerIdFile = "C:\TPass\Support Files\SID.txt"
overallTestResultsPass = False
testResultsText = ""
processResultsText = ""
printedFaultText = ""
printedLabelText = ""
numberFaultsAdded = 0

#178,20211486710,F,D335C TBM2 GPS COAX BLUE,COMPLETE INITIALIZATION OF DTC`s,
#178,20211488200,P,,

# Internal Functions
def IsTestFailed(testResults):

    if (testResults == str(TestResults.Fail) or testResults == str(TestResults.FatalFail) or
            testResults == str(TestResults.OperatorFail) or testResults == str(TestResults.OperatorAbort) or testResults == str(TestResults.SystemError)):
        return True
    else:
        return False

def SetFault(faultId, faultDescription, testResult):
    global testResultsText
    global printedFaultText
    global maxNumberFaultsToSave
    global numberFaultsAdded

    if faultDescription != "" and faultId != "":
        testResultsText = testResultsText + faultId + "," + faultDescription[0:64] + "," + testResult + "\r\n"
    ## Change set fault
    if (numberFaultsAdded < maxNumberFaultsToSave and faultDescription != ""):
        numberFaultsAdded = numberFaultsAdded + 1
        printedFaultText = printedFaultText + faultId + "," + faultDescription[0:64] + "," + testResult+ "\r\n"
        
def SetProcessData(reportId, reportData):
    global processResultsText
    if (reportId and reportData):
        # Saving Process Data is not implemented for Dakkota
        processResultsText = ""

# Main Logic
try:

    # Read testerId from file
    try:
        testerIdLines = File.ReadAllLines(testerIdFile)
        testerId = testerIdLines[0]
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("PLCInterface", "Test Results Processing Script:  Error Reading Test ID File, will default to Tester ID = 0.  Exception Occurred = " + str(inst), True, True)
        TPassLogger.Error("Results Processing Script:  Error Reading Test ID File, will default to Tester ID = 0.  File.ReadLines Exception Occurred :{0}", inst)            
    
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

    testResultsText = testResultsText + productIdentification.PrimaryId + "\r\n"

    ## Test flag
    if (str(testAppResults.MainTestApplication.TestCycleResults.TestResults) == str(TestResults.Fail)):
        overallTestResultsPass = False
        testResultsText = testResultsText + "0" + "\r\n"
        printedLabelText = printedLabelText + "Overall = F" + "\r\n"
    else:
        testResultsText = testResultsText + "1" + "\r\n"
        printedLabelText = printedLabelText + "Overall = P" + "\r\n"
        overallTestResultsPass = True
        
    testResultsText = testResultsText + productIdentification.SecondaryId + "\r\n"
    #testResultsText = testResultsText + testerId + "\r\n"
    testResultsText = testResultsText + initialFormat + "\r\n"    #Inital format
    testResultsText = testResultsText + plantText + "\r\n"    #plant location
    testResultsText = testResultsText + testSiteText + "\r\n"    #test site location
    testResultsText = testResultsText + str( testAppResults.MainTestApplication.TestCycleResults.DurationMsec / 1000) + "\r\n"

    printedLabelText = str(DateTime.Now) + "\r\n"
    printedLabelText = printedLabelText + "Sequence Number:" + productIdentification.PrimaryId + "\r\n"
    printedLabelText = printedLabelText + "Build Code:" + productIdentification.SecondaryId + "\r\n"
    printedLabelText = printedLabelText + "Tester ID:" + testerId + "\r\n"
    ## Need to add total test cycle time

    # Set Results to send to Adient
    for groupInx in range(len(testAppResults.MainTestApplication.TestCycle)):
        for subGroupInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx])):
            for testInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps)):
                testStep = testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps[testInx]
                if (IsTestFailed(str(testStep.TestStepResults.TestResults))):
                    SetFault(testStep.Fault.Id, testStep.Fault.Description, "0")
                else:
                    SetFault(testStep.Fault.Id, testStep.Fault.Description, "1")
                # Test Step Specific Faults and Process data
                if (testStep.Name == "VoltageRange"):
                    for voltageRange in testStep.VoltageRanges:
                        for limit in voltageRange.Limits:
                            if (IsTestFailed(str(limit.TestStepResults.TestResults))):
                                SetFault(limit.Fault.Id, limit.Fault.Description, "0")
                            else:
                                SetFault(limit.Fault.Id, limit.Fault.Description, "1")

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
                            SetFault(currentRange.Fault.Id, currentRange.Fault.Description, "0")    
                        else:
                            SetFault(currentRange.Fault.Id, currentRange.Fault.Description, "1")
                            
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
                            SetFault(canDataEntity.Fault.Id, canDataEntity.Fault.Description, "0")
                        else:
                            SetFault(canDataEntity.Fault.Id, canDataEntity.Fault.Description, "1")
                            
                if (testStep.Name == "CanSendReceiveValidate"):
                    for canDataEntity in testStep.CanSendReceiveValidate.CanDataEntities:
                        if (IsTestFailed(str(canDataEntity.TestStepResults.TestResults))):
                            SetFault(canDataEntity.Fault.Id, canDataEntity.Fault.Description, "0")
                        else:
                            SetFault(canDataEntity.Fault.Id, canDataEntity.Fault.Description, "1")
 
                if (testStep.Name == "CanValidateSavedDtcData"):
                    for dtc in testStep.CanValidateSavedDtcData.Dtcs:
                        if (IsTestFailed(str(dtc.TestStepResults.TestResults))):
                            SetFault(dtc.Fault.Id, dtc.Fault.Description, "0")
                        else:
                            SetFault(dtc.Fault.Id, dtc.Fault.Description, "1")
 
                if (testStep.Name == "CanValidatePartNumber"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        SetProcessData(testStep.CanValidatePartNumber.TestDataReporting.BroadcastedPartNumber, testStep.CanValidatePartNumber.TestData.BroadcastedPartNumber)
                        SetProcessData(testStep.CanValidatePartNumber.TestDataReporting.ProcessedPartNumber, testStep.CanValidatePartNumber.TestData.ProcessedPartNumber)

                if (testStep.Name == "LinSendReceiveValidate"):
                    for linDataEntity in testStep.LinSendReceiveValidate.LinDataEntities:
                        if (IsTestFailed(str(linDataEntity.TestStepResults.TestResults))):
                            SetFault(linDataEntity.Fault.Id, linDataEntity.Fault.Description, "0")
                        else:
                            SetFault(linDataEntity.Fault.Id, linDataEntity.Fault.Description, "1")
                            
                if (testStep.Name == "ModbusValidateVoltageRange"):
                    for channel in testStep.ModbusValidateVoltageRange.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id, channel.Fault.Description, "0")
                        else:
                            SetFault(channel.Fault.Id, channel.Fault.Description, "1")

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
                            SetFault(channel.Fault.Id, channel.Fault.Description, "0")
                        else:
                            SetFault(channel.Fault.Id, channel.Fault.Description, "1")

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
                            SetFault(channel.Fault.Id, channel.Fault.Description, "0")
                        else:
                            SetFault(channel.Fault.Id, channel.Fault.Description, "1")
                            
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
                            SetFault(channel.Fault.Id, channel.Fault.Description, "0")
                        else:
                            SetFault(channel.Fault.Id, channel.Fault.Description, "1")

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
                            SetFault(channel.Fault.Id, channel.Fault.Description, "0")
                        else:
                            SetFault(channel.Fault.Id, channel.Fault.Description, "1")

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
                        
                if(testStep.Name == "ModbusValidateLaserPositionRange"):
                    
                    for channel in testStep.ModbusValidateLaserPositionRange.Channels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id, channel.Fault.Description, "0")
                        else:
                            SetFault(channel.Fault.Id, channel.Fault.Description, "1")
                            
                        if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetProcessData(channel.TestDataReporting.UpperLimitMMeter, str(channel.TestDataReporting.UpperLimitMMeter))
                            SetProcessData(channel.TestDataReporting.LowerLimitMMeter, str(channel.TestDataReporting.LowerLimitMMeter))
                            SetProcessData(channel.TestDataReporting.Samples, str(channel.TestDataReporting.Samples))
                            SetProcessData(channel.TestDataReporting.MaxTimeInPassWindowMsec, str(channel.TestDataReporting.MaxTimeInPassWindowMsec))
                            SetProcessData(channel.TestDataReporting.MaxChannelLaserPositionMMeters, str(channel.TestDataReporting.MaxChannelLaserPositionMMeters))
                            SetProcessData(channel.TestDataReporting.MinChannelLaserPositionMMeters, str(channel.TestDataReporting.MinChannelLaserPositionMMeters))
                            SetProcessData(channel.TestDataReporting.AvgChannelLaserPositionInRangeMMeters, str(channel.TestDataReporting.AvgChannelLaserPositionInRangeMMeters))
                
                if (testStep.Name == "ModbusIOBoardValidateLaserPositionRange"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        SetProcessData(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.UpperLimitMamp, str(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.UpperLimitMamp))
                        SetProcessData(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.LowerLimitMamp, str(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.LowerLimitMamp))
                        SetProcessData(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.Samples, str(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.Samples))
                        SetProcessData(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.AvgCurrentInRangeMamp, str(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.AvgCurrentInRangeMamp))
                        SetProcessData(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.BaseCurrentMamp, str(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.BaseCurrentMamp))
                        SetProcessData(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.MaxCurrentMamp, str(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.MaxCurrentMamp))
                        SetProcessData(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.MinCurrentMamp, str(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.MinCurrentMamp))
                        SetProcessData(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.MaxTimeInPassWindowMsec, str(testStep.ModbusIOBoardValidateLaserPositionRange.TestDataReporting.MaxTimeInPassWindowMsec))
                    
                    for channel in testStep.ModbusIOBoardValidateLaserPositionRange.Channels:
                        if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetProcessData(channel.TestDataReporting.UpperLimitMMeter, str(channel.TestDataReporting.UpperLimitMMeter))
                            SetProcessData(channel.TestDataReporting.LowerLimitMMeter, str(channel.TestDataReporting.LowerLimitMMeter))
                            SetProcessData(channel.TestDataReporting.MaxChannelLaserPositionMMeters, str(channel.TestDataReporting.MaxChannelLaserPositionMMeters))
                            SetProcessData(channel.TestDataReporting.MinChannelLaserPositionMMeters, str(channel.TestDataReporting.MinChannelLaserPositionMMeters))
                            SetProcessData(channel.TestDataReporting.AvgChannelLaserPositionInRangeMMeters, str(channel.TestDataReporting.AvgChannelLaserPositionInRangeMMeters))
                            SetProcessData(channel.TestDataReporting.BaseChannelVoltageMVolts, str(channel.TestDataReporting.BaseChannelVoltageMVolts))
        
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id, channel.Fault.Description, "0")
                        else:
                            SetFault(channel.Fault.Id, channel.Fault.Description, "1")
                    
                    for channel in testStep.ModbusIOBoardValidateLaserPositionRange.ExclusionChannels:
                        if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                            SetFault(channel.Fault.Id, channel.Fault.Description, "0")
                        else:
                            SetFault(channel.Fault.Id, channel.Fault.Description, "1")

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Results Record.  Exception Occurred :{0}", inst)
    MainTPassScripting.InterfaceUiLogger("PLCInterface", "Error Creating Results Record.  Exception Occurred = " + str(inst), True, True)
    isSuccess = False

# Create Results file for SQL connect to process
try:
    try:
        testResultsText = testResultsText.rstrip(',')
        File.WriteAllText(resultsFile + "TMP", testResultsText)
        File.Move(resultsFile + "TMP", resultsFile)
        MainTPassScripting.InterfaceUiLogger("PLCInterface", "Results File Written - " + resultsFile, False, False)
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("PLCInterface", "File.WriteAllText Exception Occurred" + str(inst), True, True)
        TPassLogger.Error("Option Retrieval Script:  File Exception Occurred :{0}", inst)            

    TPassLogger.Debug("Test Results Processing Script:  Product Primary ID = {0}, Results File Text = {1}", productIdentification.PrimaryId, testResultsText )

except Exception as inst:
    TPassLogger.Warn("Test Results Processing Script:  Error Creating Test Label Text.  Exception Occurred :{0}", inst)
    isSuccess = False

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
#	Date: 07112023
#	Version: 3.0
#	Change: Changed format of result for Adient PLCInterface
#	Date: 06052023
#	Version: 3.0
#	Change: Changed format of results for Inteva PLCInterface
#	Date: 05262023
#	Version: 2.0
#	Change: Fixed formatting issue with Faults preventing more than one fault from being sent by PLCInterface
#	Date: 05042022
#	Version: 2.0
#	Change: Read tester ID from the \TPass\Support Files\SID.txt file
#	Date: 10092021
#	Version: 1.0
#	Change: Initial Version
############################################################

