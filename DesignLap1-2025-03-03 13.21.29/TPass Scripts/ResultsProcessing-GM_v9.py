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
## Note this reference is required in order to access the Colors for the Background
clr.AddReferenceByPartialName("PresentationCore")
from System.Windows.Media import Brushes

version = "9.0"
production = False
TPassLogger.Debug("Test Results Processing Script:  Product Primary Id = {0}", productIdentification.PrimaryId)
TPassLogger.Debug("Test Results Processing Script:  Product Secondary Id = {0}", productIdentification.SecondaryId)
isSuccess = True

#########################################################################################################################################
# Application Engineer:  Set Station Number to be written to the printed label
#
stationNumber = "12" 
maxNumberFaultsOnPrintedLabel = 10
printPassLabel = False
mmtSafetyFault = 52132 
#
#########################################################################################################################################

overallTestResultsPass = False
printedFaultText = ""
screenLabelFaultText = ""
numberFaultsAdded = 0
totalNumberOfFaults = 0
safetyFaultOccurred = False
safetyFaultDescription = ""

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
    global safetyFaultOccurred
    global safetyFaultDescription
    if (faultId):
        try:
            if (int(faultId) == mmtSafetyFault):
                safetyFaultOccurred = True
                safetyFaultDescription = faultId.zfill(5) + "," + faultDescription
            totalNumberOfFaults += 1
            screenLabelFaultText = screenLabelFaultText + faultId.zfill(5) + " - " + faultDescription + "\r\n"
            if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                numberFaultsAdded = numberFaultsAdded + 1
                printedFaultText = printedFaultText + faultId.zfill(5) + "," + faultDescription + "\r\n"
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

def SetProcessData(userValueId, userValue):
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
    printedLabelText = str(DateTime.Now) + "\r\n"
    printedLabelText = printedLabelText + "VIN:" + productIdentification.SecondaryId + "\r\n"
    printedLabelText = printedLabelText + "CHARGE PORT TESTER-STN:" + stationNumber + " DPN#:" + productIdentification.PrimaryId + "\r\n"
    screenLabelText = str(DateTime.Now) + "    " + "VIN:" + productIdentification.SecondaryId + "\r\n"
    builddataCsn = ""
    builddataMd = ""
        
    gmEdiBuildResultsRecord.HrClearDateTime()
    gmEdiBuildResultsRecord.HrClearFaults()
    gmEdiBuildResultsRecord.HrClearUserValues()
    gmEdiBuildResultsRecord.ScClearShippingCtrl()
    gmEdiBuildResultsRecord.HrSetDpn(productIdentification.PrimaryId)
    gmEdiBuildResultsRecord.HrSetAbortedFlag(ord(' '))

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
        for keyValuePair in keyValuePairs:
            key = keyValuePair.Split('=')[0].Trim().ToUpper()
            value = keyValuePair.Split('=')[1].ToUpper()
            if (key == "CSN"):
                builddataCsn = value
                MainTPassScripting.InterfaceUiLogger("GM EDI", "CSN = " + value, False, False)
                break
        for keyValuePair in keyValuePairs:
            key = keyValuePair.Split('=')[0].Trim().ToUpper()
            value = keyValuePair.Split('=')[1].ToUpper()
            if (key == "MD"):
                builddataMd = value
                MainTPassScripting.InterfaceUiLogger("GM EDI", "MD = " + value, False, False)
                break

    screenLabelText = screenLabelText + "CHARGE PORT TESTER-STN:" + stationNumber + "    " + " DPN#:" + productIdentification.PrimaryId + "    " + "CSN:<b>" + builddataCsn + "</b>    " + "MODEL:" + builddataMd + "\r\n"

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
        printedLabelText = printedLabelText + "Test Status: Failed" + "\r\n"
    else:
        printedLabelText = printedLabelText + "Test Status: Passed" + "\r\n"
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
        #gmEdiBuildResultsRecord.HrSetAbortedFlag(ord('A'))
        #MainTPassScripting.InterfaceUiLogger("GM EDI", "HrSetAbortedFlag() value = A", False, False)
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
                    if IsTestFailed(testStep.TestStepResults.TestResults):
                        screenLabelFaultText = screenLabelFaultText + "   " + testStep.Fault.Detail + "\r\n"
                        printedFaultText = printedFaultText + "   " + testStep.Fault.Detail + "\r\n"
                        totalNumberOfFaults += 1
                        
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            SetProcessData(testStep.CanSendReceiveValidate.TestDataReporting.DpidData, str(testStep.CanSendReceiveValidate.TestData.DpidData))

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

                if (testStep.Name == "LinValidatePartNumber"):
                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):

                        #Add Broadcasted and Processed Part Numbers to printed label
                        if (str(testStep.TestStepResults.TestResults) != str(TestResults.Pass)):
                            if (testStep.Fault.Detail):
                                screenLabelFaultText = screenLabelFaultText + "   " + testStep.Fault.Detail + "\r\n"
                            if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                                if (testStep.Fault.Detail):
                                    numberFaultsAdded = numberFaultsAdded + 1
                                    printedFaultText = printedFaultText + "   " + testStep.Fault.Detail + "\r\n"
                                    #printedFaultText = printedFaultText + "   PN from Broadcast: " + testStep.LinValidatePartNumber.TestData.BroadcastedPartNumber + "," + " PN from Module: " + testStep.LinValidatePartNumber.TestData.ProcessedPartNumber + "\r\n"

                        if (testStep.LinValidatePartNumber.TestDataReporting.BroadcastedPartNumber):
                            try:
                                userValueIds = testStep.LinValidatePartNumber.TestDataReporting.BroadcastedPartNumber.Split(',')
                                if len(userValueIds) != 2:
                                    TPassLogger.Error("Test Results Processing Script:  BroadcastedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.LinValidatePartNumber.TestDataReporting.BroadcastedPartNumber)
                                else:
                                    try:
                                        userValues = testStep.LinValidatePartNumber.TestData.BroadcastedPartNumber
                                        if (not Regex.IsMatch(userValues, "^\d{8}$")):
                                            TPassLogger.Warn("Test Results Processing Script:  BroadcastedPartNumber format must be 8 digits.  Value = {0}", testStep.LinValidatePartNumber.TestData.BroadcastedPartNumber)
                                        else:
                                            userValues = [userValues[i:i+4] for i in range(0, len(userValues), 4)]
                                            SetProcessData(userValueIds[0], userValues[0])
                                            SetProcessData(userValueIds[1], userValues[1])
                                    except Exception as inst:
                                        TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                        isSuccess = False
                            except Exception as inst:
                                TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                TPassLogger.Warn("Test Results Processing Script:  BroadcastedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.LinValidatePartNumber.TestDataReporting.BroadcastedPartNumber)
 
                        if (testStep.LinValidatePartNumber.TestDataReporting.ProcessedPartNumber):
                            try:
                                userValueIds = testStep.LinValidatePartNumber.TestDataReporting.ProcessedPartNumber.Split(',')
                                if len(userValueIds) != 2:
                                    TPassLogger.Error("Test Results Processing Script:  ProcessedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.LinValidatePartNumber.TestDataReporting.ProcessedPartNumber)
                                else:
                                    try:
                                        userValues = testStep.LinValidatePartNumber.TestData.ProcessedPartNumber
                                        if (not Regex.IsMatch(userValues, "^\d{8}$")):
                                            TPassLogger.Warn("Test Results Processing Script:  ProcessedPartNumber format must be 8 digits.  Value = {0}", testStep.LinValidatePartNumber.TestData.ProcessedPartNumber)
                                        else:
                                            userValues = [userValues[i:i+4] for i in range(0, len(userValues), 4)]
                                            SetProcessData(userValueIds[0], userValues[0])
                                            SetProcessData(userValueIds[1], userValues[1])
                                    except Exception as inst:
                                        TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                        isSuccess = False
                            except Exception as inst:
                                TPassLogger.Warn("Test Results Processing Script:  Error Setting User Value in MERS History Record.  Exception Occurred :{0}", inst)
                                TPassLogger.Warn("Test Results Processing Script:  ProcessedPartNumberId format must contain two IDs and comma delimited.  Id = {0}", testStep.LinValidatePartNumber.TestDataReporting.ProcessedPartNumber)

                if (testStep.Name == "ModbusValidateReadingRange"):
                    for reading in testStep.ModbusValidateReadingRange.Readings:
                        #Add Detail to printed label
                        if (IsTestFailed(str(reading.TestStepResults.TestResults))):
                            SetFault(reading.Fault.Id, reading.Fault.Description)
                            if (reading.Fault.Detail):
                                screenLabelFaultText = screenLabelFaultText + "   " + reading.Fault.Detail + "\r\n"
                            if (numberFaultsAdded < maxNumberFaultsOnPrintedLabel):
                                if (reading.Fault.Detail):
                                    numberFaultsAdded = numberFaultsAdded + 1
                                    printedFaultText = printedFaultText + "   " + reading.Fault.Detail + "\r\n"

                        if (str(reading.TestStepResults.TestResults) != str(TestResults.NotTested) and str(reading.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                            
                            SetProcessData(reading.TestDataReporting.UpperLimit, str(reading.UpperLimit))
                            SetProcessData(reading.TestDataReporting.LowerLimit, str(reading.LowerLimit))
                            SetProcessData(reading.TestDataReporting.Samples, str(reading.TestData.Samples))
                            SetProcessData(reading.TestDataReporting.MaxReading, str(reading.TestData.MaxReading))
                            SetProcessData(reading.TestDataReporting.MinReading, str(reading.TestData.MinReading))
                            SetProcessData(reading.TestDataReporting.AvgReading, str(reading.TestData.AvgReading))
                            SetProcessData(reading.TestDataReporting.MaxTimeInPassWindowMsec, str(reading.TestData.MaxTimeInPassWindowMsec/1000))
                            
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

                if (testStep.Name == "EVChargerPowerValidation"):

                    if (str(testStep.TestStepResults.TestResults) != str(TestResults.NotTested) and str(testStep.TestStepResults.TestResults) != str(TestResults.OptionCodeNotTested)):
                        
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.UpperLimitVolts, str(testStep.EVChargerPowerValidation.UpperLimitVolts))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.LowerLimitVolts, str(testStep.EVChargerPowerValidation.LowerLimitVolts))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.MaxChargerVoltageVolts, str(testStep.EVChargerPowerValidation.TestData.MaxChargerVoltageVolts))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.MinChargerVoltageVolts, str(testStep.EVChargerPowerValidation.TestData.MinChargerVoltageVolts))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.AvgChargerVoltageInRangeVolts, str(testStep.EVChargerPowerValidation.TestData.AvgChargerVoltageInRangeVolts))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.UpperLimitCurrent, str(testStep.EVChargerPowerValidation.UpperLimitAmp))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.LowerLimitCurrent, str(testStep.EVChargerPowerValidation.LowerLimitAmp))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.MaxChargerCurrentAmps, str(testStep.EVChargerPowerValidation.TestData.MaxChargerAmperageAmps))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.MinChargerCurrentAmps, str(testStep.EVChargerPowerValidation.TestData.MinChargerAmperageAmps))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.AvgChargerCurrentInRangeAmps, str(testStep.EVChargerPowerValidation.TestData.AvgChargerCurrentInRangeAmps))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.Samples, str(testStep.EVChargerPowerValidation.TestData.Samples))
                        SetProcessData(testStep.EVChargerPowerValidation.TestDataReporting.MaxTimeInPassWindowMsec, str(testStep.EVChargerPowerValidation.TestData.MaxTimeInPassWindowMsec/1000))
                            

    # Create MERS Record
    if (SystemConfigurationValue.PartnerInterfaces.GmEdi.CreateMersReportingRecord): 
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
    if (SystemConfigurationValue.PartnerInterfaces.GmEdi.CreateGepicsShipRecord): 
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
    if (SystemConfigurationValue.PartnerInterfaces.GmEdi.CreateGsipQualityRecord): 
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

# Create Screen Label Text to pass back to TPass for displaying on the Pass/Fail screens
try:
    if (overallTestResultsPass):
        screenLabelText = "<fontsize:32>" + screenLabelText + "<b>\r\n\r\nPASSED\r\nPASSED\r\nPASSED\r\nPASSED" + "</b></fontsize>"
    else:
        if (safetyFaultOccurred):
            tempScreenLabelText = "<fontsize:38><b>SAFETY FAULT OCCURRED</fontsize>\r\n<fontsize:32>*GO TO REPAIR STATION DO NOT CHARGE ON COMMERCIAL CHARGER*</b></fontsize>\r\n\r\n" + "<fontsize:32>" + screenLabelText + "</fontsize>" + "<fontsize:24>\r\n<b>FLTS:" + str(totalNumberOfFaults) + "</b></fontsize>" + "<fontsize:32>\r\n" + screenLabelFaultText + "</fontsize>"
            screenLabelText = tempScreenLabelText
            MainTPassScripting.OverrideResultsScreenDisplayTimeSec(20)
        else:
            screenLabelText = "<fontsize:32>" + screenLabelText + "</fontsize>" + "<fontsize:24>\r\n<b>FLTS:" + str(totalNumberOfFaults) + "</b></fontsize>" + "<fontsize:32>\r\n" + screenLabelFaultText + "</fontsize>"
            #screenLabelText = "<b>The reason</b> <fontsize:30>why this failed</fontsize> <fontsize:12><color:green>is because somebody turned</color> the light off... duh!</fontsize>"

    MainTPassScripting.UpdateTestResultsScreenCustomText(screenLabelText)
    TPassLogger.Debug("Test Results Processing Script:  Product Primary ID = {0}, Screen Custom Label Text = {1}", productIdentification.PrimaryId, screenLabelText )

except:
    TPassLogger.Warn("Test Results Processing Script:  UpdateTestResultsScreenCustomText being called but functionality is not implemented until TPass v1.4.0.3 or later")
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("GM EDI", "UpdateTestResultsScreenCustomText being called but functionality is not implemented until TPass v1.4.0.3 or later", True, False)

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

# Alert if safety fault occurred
# try:
    # if (safetyFaultOccurred):
        # AlertMessage = """<fontsize:32><b>SAFETY FAULT OCCURRED:</b>  DPN = {primaryId}\r\n\r\nRETURN VEHICLE TO REPAIR STATION, DO NOT CHARGE ON COMMERCIAL CHARGER  </fontsize>""".format(primaryId = productIdentification.PrimaryId)
        # AlertMessage += "\r\n\r\n\r\n\r\n<b>FLT:</b>\r\n<fontsize:32>" + safetyFaultDescription + "</fontsize>"
        # #AlertMessage = """<fontsize:32> >: <b>SAFETY FAULT OCCURRED</b>", "RETURN VEHICLE TO REPAIR STATION, DO NOT CHARGE ON COMMERCIAL CHARGER.  DPN = = {primaryId}  </fontsize>""".format(primaryId = productIdentification.PrimaryId)
        # TPassLogger.Info("Test Results Processing Script: SAFETY FAULT OCCURRED RETURN VEHICLE TO REPAIR STATION, DO NOT CHARGE ON COMMERCIAL CHARGER")
        # MainTPassScripting.Alert("SAFETY FAULT OCCURRED", AlertMessage, 32.0, Brushes.Red)
        # MainTPassScripting.InterfaceUiLogger("Test Results Processing Script", "SAFETY FAULT OCCURRED RETURN VEHICLE TO REPAIR STATION, DO NOT CHARGE ON COMMERCIAL CHARGER.  DPN = " + productIdentification.PrimaryId, True, True)

# except Exception as inst:
    # TPassLogger.Warn("Test Results Processing Script:  Error alerting for safety fault.  Exception Occurred :{0}", inst)
    # isSuccess = False


TPassLogger.Info("Test Results Processing Script:  Is Success = {0}", isSuccess)





############################################################
# Change History
############################################################
#	Date: 10032023
#	Version: 9.0
#	Change: Added CanSendReceiveValidate test step ability to send process data to MERS
#	Date: 06082023
#	Version: 8.0
#	Change: Added EV Test Steps to allow for sending process data to MERS - LinValidatePartNumber, ModbusValidateReadingRange, EVChargerPowerValidation
#	Date: 09262022
#	Version: 7.0
#	Change: Added populating Custom Test Results for TPass to display on Pass/Fail Screens when enabled by System Parameter ResultsScreen->UseCustomTextOnTestResultsScreen
#	Date: 04212022
#	Version: 6.0
#	Change: Added Broad casted and Processed Part Numbers to fail label 
#	Date: 10202021
#	Version: 5.0
#	Change: Remove setting Abort flag with EDI.  Added missing Test Steps LinSendReceiveValidate and MeterValidateResistanceRange
#	Date: 08052021
#	Version: 4.0
#	Change: Don't set print string for Passed Test Cycle if printPassLabel = False
#	Date: 08042021
#	Version: 3.0
#	Change: Added Print label text formatting for DHAM
#	Date: 01012019
#	Version: 1.0
#	Change: Initial Version
############################################################

