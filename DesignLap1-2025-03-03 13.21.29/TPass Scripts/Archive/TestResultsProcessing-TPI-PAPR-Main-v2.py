#Process the Test Results data sending to the Plants MES system.  Also Print the Test Results Label if required
#
#This Script is expected to set the out parameters below
#TPass Objects Passed In/Returned
#   in - object "MainTPassScripting" - Exposed all methods and properties for the scripts to use
#   in - object "testAppResults" - Contains all the test cycle results of the current product tested
#   in - object "productIdentification" - Contains all the attributes of the current product tested
#   in - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in - method "GetConfigurationValue" - This is used to retrieve Tool System Configuration parameters
#   out - string "printedLabelText"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

import clr
clr.AddReference('System.Web.Extensions')
clr.AddReferenceToFileAndPath('.\\Tpi.TPass.Common.dll')
import System
from System.IO import StreamReader
from System.Net import HttpWebRequest
from System.Text import Encoding
from System.Web.Script.Serialization import JavaScriptSerializer
from System.Text.RegularExpressions import Regex
from System import Uri
from System import TimeSpan
from Tpi.TPass.Common.JsonStore import TestResults

#System.Diagnostics.Debugger.Break();

version = "2.0"
production = False
TPassLogger.Debug("Test Results Processing Script:  Product Primary Id = {0}", productIdentification.PrimaryId)
isSuccess = True

testerType = "Main Housing Test"


# Internal Functions
def IsTestFailed(testResults):

    if (testResults == str(TestResults.Fail) or testResults == str(TestResults.FatalFail) or
            testResults == str(TestResults.OperatorFail) or testResults == str(TestResults.OperatorAbort) or testResults == str(TestResults.SystemError)):
        return True
    else:
        return False

def SendFailRecord(testFaultId, testFaultDescription):

    if (testFaultId != "" or testFaultDescription != ""):
        f = open("C:\TPass\Logs\PAPR-ResultsForBizowie.txt", 'a')
        f.write(currentDataTime + "," + testerType + "," + productIdentification.PrimaryId + "," + testFaultId + "," + testFaultDescription + "\n")
        f.close()
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("Bizowie", "Sending Fail Record: " + currentDataTime + "," + testerType + "," + productIdentification.PrimaryId + "," + testFaultId + "," + testFaultDescription, False, False)
        payload["data"]["date_time_stamp"] = currentDataTime
        payload["data"]["test_id"] = testerType
        payload["data"]["internal_serial_number"] = productIdentification.PrimaryId
        payload["data"]["passfailure_code"] = testFaultId
        payload["data"]["failure_code_description"] = testFaultDescription
        PostHttpRequest()

def SendPassRecord():

    f = open("C:\TPass\Logs\PAPR-ResultsForBizowie.txt", 'a')
    f.write(currentDataTime + "," + testerType + "," + productIdentification.PrimaryId + "," + "PASS" + "\n")
    f.close()
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("Bizowie", "Sending Pass Record: " + currentDataTime + "," + testerType + "," + productIdentification.PrimaryId + "," + "PASS", False, False)
    payload["data"]["date_time_stamp"] = currentDataTime
    payload["data"]["test_id"] = testerType
    payload["data"]["internal_serial_number"] = productIdentification.PrimaryId
    payload["data"]["passfailure_code"] = "PASS"
    payload["data"]["failure_code_description"] = ""
    PostHttpRequest()

def PostHttpRequest():

    TPassLogger.Debug("Test Results Processing Script:  PostHttpRequest() Begin")

    # convert dictionary to Json string
    payloadJson = JavaScriptSerializer().Serialize(payload)

    # encode the json string
    payloadBytes = Encoding.ASCII.GetBytes(payloadJson)

    # create request
    request = HttpWebRequest.Create(url)
 
    # required properties
    request.ContentType = 'application/json'
    request.Method = 'POST'
    request.Timeout = 5000             #msec
    request.ReadWriteTimeout = 5000    #msec

    # create request stream and write json str to it
    requestStream = request.GetRequestStream()
    requestStream.Write(payloadBytes, 0, payloadBytes.Length)
    requestStream.Close()
 
    # get response
    response = request.GetResponse()
  
    # read response as string
    responseJson = StreamReader(response.GetResponseStream()).ReadToEnd()
    response.Close()

    # convert response string to dictionary
    responseDict = JavaScriptSerializer().Deserialize(responseJson, object)

    if (responseDict["success"] == 1):
        TPassLogger.Debug("Test Results Processing Script:  PostHttpRequest() - Successfully added Result")
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("Bizowie", "Success Posting Record", False, False)
    else:
        TPassLogger.Error("Test Results Processing Script:  PostHttpRequest() - Failed adding Result - Bizowie Reason: " + responseJson)
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("Bizowie", "Failure Posting Record: " + responseJson, True, True)
        global isSuccess
        isSuccess = False

    TPassLogger.Debug("Test Results Processing Script:  PostHttpRequest() End")

# Main Logic
try:

    url = "https://crossequipment.mybizowie.com/bz/apiv2/call/Database/table_row/create"
    payload = {
        "api_key": "6pCp799A4qGd2A4oohH8meo6HrHPSgn0Y",
        "secret_key": "Lf9YCpRY1W4peGFeio2iWUL2FQYtEAinK",
        "db_table_id": 20,
        "data": {"date_time_stamp": "", "test_id": "", "internal_serial_number": "", "passfailure_code": "", "failure_code_description": "" }
    }
    currentDataTime = str(testAppResults.MainTestApplication.TestCycleResults.BeginDateTime)

    if (str(testAppResults.MainTestApplication.TestCycleResults.TestResults) == str(TestResults.Pass)):
        SendPassRecord()
    else:

        # Set Faults
        for groupInx in range(len(testAppResults.MainTestApplication.TestCycle)):
            for subGroupInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx])):
                for testInx in range(len(testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps)):
                    testStep = testAppResults.MainTestApplication.TestCycle[groupInx][subGroupInx].TestSteps[testInx]
                    if (IsTestFailed(str(testStep.TestStepResults.TestResults))):
                        SendFailRecord(testStep.Fault.Id, testStep.Fault.Description)

                    # Test Step Specific Faults
                    if (testStep.Name == "VoltageRange"):
                        for voltageRange in testStep.VoltageRanges:
                            for limit in voltageRange.Limits:
                                if (IsTestFailed(str(limit.TestStepResults.TestResults))):
                                    SendFailRecord(limit.Fault.Id, limit.Fault.Description)

                    if (testStep.Name == "SinkCurrentRangeBase" or testStep.Name == "SourceCurrentRangeBase" or testStep.Name == "SinkCurrentRangeDelta" or testStep.Name == "SourceCurrentRangeDelta"):
                        for currentRange in testStep.CurrentRanges:
                            if (IsTestFailed(str(currentRange.TestStepResults.TestResults))):
                                SendFailRecord(currentRange.Fault.Id, currentRange.Fault.Description)

                    if (testStep.Name == "CanReceiveValidate"):
                        for canDataEntity in testStep.CanReceiveValidate.CanDataEntities:
                            if (IsTestFailed(str(canDataEntity.TestStepResults.TestResults))):
                                SendFailRecord(canDataEntity.Fault.Id, canDataEntity.Fault.Description)

                    if (testStep.Name == "CanSendReceiveValidate"):
                        for canDataEntity in testStep.CanSendReceiveValidate.CanDataEntities:
                            if (IsTestFailed(str(canDataEntity.TestStepResults.TestResults))):
                                SendFailRecord(canDataEntity.Fault.Id, canDataEntity.Fault.Description)

                    if (testStep.Name == "CanValidateSavedDtcData"):
                        for dtc in testStep.CanValidateSavedDtcData.Dtcs:
                            if (IsTestFailed(str(dtc.TestStepResults.TestResults))):
                                SendFailRecord(dtc.Fault.Id, dtc.Fault.Description)

                    if (testStep.Name == "ModbusValidateVoltageRange"):
                        for channel in testStep.ModbusValidateVoltageRange.Channels:
                            if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                                SendFailRecord(channel.Fault.Id, channel.Fault.Description)

                    if (testStep.Name == "MeterValidateVoltageRange"):
                        for channel in testStep.MeterValidateVoltageRange.Channels:
                            if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                                SendFailRecord(channel.Fault.Id, channel.Fault.Description)

                    if (testStep.Name == "MeterValidateFrequencyRange"):
                        for channel in testStep.MeterValidateFrequencyRange.Channels:
                            if (IsTestFailed(str(channel.TestStepResults.TestResults))):
                                SendFailRecord(channel.Fault.Id, channel.Fault.Description)

except Exception as inst:
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("Bizowie", str(inst), True, True)
    TPassLogger.Error("Test Results Processing Script:  Error Creating PAPR Results Record.  Exception Occurred :{0}", inst)
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
#   Date: 03152021
#   Version: 2.0
#   Change: Added writing to Interface UI Logger
#   Date: 11172020
#   Version: 1.0
#   Change: Initial Version
############################################################

