#Command Camera to take picture and validate Pass/Fail 
#
#TPass Objects Passed In/Returned
#   in - Function "TestAppLogger"
#   in - Function "TPassLogger"
#   in - string "primaryId"
#   in - string "secondaryId"
#   in - string "tertiaryId"
#   in - string "quaternaryId"
#   in - string "quinaryId"
#   in - object "SystemConfigurationValue"
#   in - string "TestAppLogFileName"
#   in - string[] "validationScriptInputs"
#   in - bool     "TerminateScript"
#   out - string "FaultDetail" 
#   out - string "Comments" 
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

#########################################################################################################################################
# Application Engineer:  Specific constant variables to maintain
#
#########################################################################################################################################

import clr
from System.IO import File
from System import DateTime
from System.Text import Encoding
version = "1.0"
production = False
cameraResponse = ""
# Following parameters get set via System Configuration parameters
cameraRemoteIpAddress = ""
cameraRemotePort = 0 
cameraConnectTimeout = 0
cameraCommandTimeout = 0
cameraRetryCount = 0

# Internal Functions
def LogBoth(message, isError):
    if isError:
        TPassLogger.Error(message)
        TestAppLogger.Error(message)
    else:
        TPassLogger.Info(message)
        TestAppLogger.Info(message)
    return
    
def CameraConnect(tcpClient):
    global cameraRemoteIpAddress
    global cameraRemotePort
    global cameraConnectTimeout
    global FaultDetail
    
    isSuccessful = False
    try:
        if tcpClient.ConnectAsync() == True:
            startDateTime = DateTime.Now
            while (DateTime.Now - startDateTime).TotalMilliseconds < cameraConnectTimeout and str(tcpClient.ConnectAsyncStage) == str(tcpClient.ConnectAsyncStages.InProgress) and not MainTPassScripting.CommandAbortPythonScript:
                MainTPassScripting.UpdateEvents()
            if str(tcpClient.ConnectAsyncStage) == str(tcpClient.ConnectAsyncStages.Success):
                LogBoth("Vision Validation Python Script - ConnectAsync - Success Connecting to " + str(cameraRemoteIpAddress) + ":" + str(cameraRemotePort), False)
                isSuccessful = True
            else:
                if str(tcpClient.ConnectAsyncStage) == str(tcpClient.ConnectAsyncStages.InProgress):
                    LogBoth("Vision Validation Python Script - ConnectAsync - Timeout waiting on connection to camera", True)
                    tcpClient.ResetAsyncOperations()
                    FaultDetail += "ConnectAsync - Timeout waiting on connection to camera\r"
                else:
                    LogBoth("Vision Validation Python Script - ConnectAsync - Failed connecting to camera", True)
                    FaultDetail += "ConnectAsync - Failed connecting to camera\r"
        else:
            LogBoth("Vision Validation Python Script - ConnectAsync - Error Connecting to camera", True)
            FaultDetail += "ConnectAsync - Error Connecting to camera\r"

    except Exception as inst:
        LogBoth("Vision Validation Python Script - CameraConnect:  Exception Occurred: " + str(inst), True)            
        FaultDetail += "ConnectAsync - Error Connecting to camera - " + str(inst) + "\r"

    return isSuccessful

def CameraSendReceive(tcpClient, command):
    global cameraCommandTimeout
    global cameraResponse
    global cameraRemoteIpAddress
    global cameraRemotePort
    global FaultDetail

    isSuccessful = False
    try:
        if tcpClient.AsyncSend(Encoding.ASCII.GetBytes(command)) == True:
            startDateTime = DateTime.Now
            while (DateTime.Now - startDateTime).TotalMilliseconds < cameraCommandTimeout and str(tcpClient.SendAsyncStage) == str(tcpClient.SendAsyncStages.InProgress) and not MainTPassScripting.CommandAbortPythonScript:
                MainTPassScripting.UpdateEvents()
            if str(tcpClient.SendAsyncStage) == str(tcpClient.SendAsyncStages.Success):
                TestAppLogger.Info("Vision Validation Python Script - AsyncSend - Success Sending validation command " + command.replace("\r", "") + " to " + str(cameraRemoteIpAddress) + ":" + str(cameraRemotePort))
                # Receive ACK
                if tcpClient.AsyncReceive() == True:
                    startDateTime = DateTime.Now
                    while (DateTime.Now - startDateTime).TotalMilliseconds < cameraCommandTimeout and str(tcpClient.ReceiveAsyncStage) == str(tcpClient.ReceiveAsyncStages.InProgress) and not MainTPassScripting.CommandAbortPythonScript:
                        MainTPassScripting.UpdateEvents()
                    if str(tcpClient.ReceiveAsyncStage) == str(tcpClient.ReceiveAsyncStages.Success):
                        cameraResponse = bytearray.fromhex(tcpClient.ReceivedMessageHex).decode()
                        TestAppLogger.Info("Vision Validation Python Script - AsyncReceive - Received camera response =  " + str(tcpClient.ReceivedMessageHex))
                        TestAppLogger.Info("Vision Validation Python Script - AsyncReceive - Received camera response ASCII =  " + str(cameraResponse.replace("\r", "")))
                        isSuccessful = True
                    else:
                        if str(tcpClient.ReceiveAsyncStage) == str(tcpClient.ReceiveAsyncStages.InProgress):
                            LogBoth("Vision Validation Python Script - AsyncReceive - Timeout waiting on camera response", True)
                            tcpClient.ResetAsyncOperations()
                            FaultDetail += "AsyncReceive - Timeout waiting on camera response\r"
                        else:
                            LogBoth("Vision Validation Python Script - AsyncReceive - Failed receiving camera response", True)
                            FaultDetail += "AsyncReceive - Failed receiving camera response\r"
                else:
                    LogBoth("Vision Validation Python Script - AsyncReceive - Error Receiving camera response", True)
                    FaultDetail += "AsyncReceive - Error Receiving camera response\r"
            else:
                if str(tcpClient.SendAsyncStage) == str(tcpClient.SendAsyncStages.InProgress):
                    LogBoth("Vision Validation Python Script - AsyncSend - Timeout waiting on sending validation command to camera", True)
                    tcpClient.ResetAsyncOperations()
                    FaultDetail += "AsyncSend - Timeout waiting on sending validation command to camera\r"
                else:
                    LogBoth("Vision Validation Python Script - AsyncSend - Failed sending validation command to camera", True)
                    FaultDetail += "AsyncSend - Failed sending validation command to camera\r"
        else:
            LogBoth("Vision Validation Python Script - AsyncSend - Error Sending validation command to camera", True)
            FaultDetail += "AsyncSend - Error Sending validation command to camera\r"
    except Exception as inst:
        LogBoth("Vision Validation Python Script - CameraSendReceive:  Exception Occurred: " + str(inst), True)            
        FaultDetail += "AsyncSend - Error Sending validation command to camera - " + str(inst) + "\r"

    return isSuccessful

# Main    
try:
    
    isSuccess = False
    FaultDetail = ""
    Comments = ""
    
    if validationScriptInputs == None:
        TestAppLogger.Info("Vision Validation Python Script: Vision Validation = Empty")
    else:
        for scriptInputs in validationScriptInputs:
            TestAppLogger.Info("Vision Validation Python Script: validationScriptInputs = " + str(scriptInputs))
    TestAppLogger.Info("Vision Validation Python Script: CommandAbortPythonScript = " + str(MainTPassScripting.CommandAbortPythonScript))

    # Override Camera variables based on System Configuration settings
    cameraConfigFound = False
    try:
        if SystemConfigurationValue.Hardware.Vision.VisionEnabled:
            cameraConnectTimeout = SystemConfigurationValue.Hardware.Vision.ConnectTimeout
            cameraCommandTimeout = SystemConfigurationValue.Hardware.Vision.CommandTimeout
            cameraRetryCount = SystemConfigurationValue.Hardware.Vision.RetryCount
            for device in SystemConfigurationValue.Hardware.Vision.VisionDevices:
                if validationScriptInputs[0].upper().strip() == device.DeviceName.upper().strip():
                    cameraConfigFound = True
                    cameraRemoteIpAddress = str(device.IP1) + "." + str(device.IP2) + "." + str(device.IP3) + "." + str(device.IP4)
                    cameraRemotePort = device.Port
                    TestAppLogger.Info("Vision Validation Python Script: cameraRemoteIpAddress = " + str(cameraRemoteIpAddress) + ", cameraRemotePort=" + str(cameraRemotePort))
                    break
            if cameraConfigFound is False:
                LogBoth("Validate Vision Script:   Test Step Script Input name defined in Test Application Test Step doesn't match a Camera Device Name defined in System Configuration : " + validationScriptInputs[0].upper().strip(), True)    
                FaultDetail += "Test Step Script Input name defined in Test Application Test Step doesn't match a Camera Device Name defined in System Configuration : " + validationScriptInputs[0].upper().strip() + "\n"
        else:
            LogBoth("Validate Vision Script:  Vision Hardware is disabled in the System Configuration", True)
            FaultDetail += "Vision Hardware is disabled in the System Configuration\n"
    except Exception as inst:
        LogBoth("Validate Vision Script:  Issue with Vision System Configuration parameters - Exception Occurred : " + str(inst), True)    
        FaultDetail += "Issue with Vision System Configuration parameters\n"

    
    cameraTcpRetries = 0
    tcpSendReceiveSuccess = False
    cameraIp = cameraRemoteIpAddress.split(".")
    try:
        tcpClient = MainTPassScripting.CreateTcpClient(int(cameraIp[0]), int(cameraIp[1]), int(cameraIp[2]), int(cameraIp[3]), cameraRemotePort)
    except Exception as inst:
        LogBoth("Validate Vision Script:  Could not create Tcp Client - TCP Exception Occurred : " + str(inst), True)    
        FaultDetail += "Could not create Tcp Client\n"
    else:
        try:
            while tcpSendReceiveSuccess == False and cameraTcpRetries <= cameraRetryCount:
                FaultDetail = ""
                # Open Connection with the camera
                if CameraConnect(tcpClient):
                    TestAppLogger.Info("Vision Validation Python Script - Version Reading")
                    if CameraSendReceive(tcpClient, "VI\r"):                                                                        # Version Reading
                        Comments += "Version Reading Response: " + cameraResponse
                        TestAppLogger.Info("Vision Validation Python Script - Read Statistics")
                        if CameraSendReceive(tcpClient, "STR\r"):                                                                   # Read Statistics
                            Comments += "Retrieve Statistics Response: " + cameraResponse
                            TestAppLogger.Info("Vision Validation Python Script - Retrieve Warnings")
                            if CameraSendReceive(tcpClient, "WR\r"):                                                                # Retrieve warnings
                                Comments += "Retrieve Warnings Response: " + cameraResponse
                                TestAppLogger.Info("Vision Validation Python Script - Retrieve Errors")
                                if CameraSendReceive(tcpClient, "RER\r"):                                                           # Retrieve errors
                                    Comments += "Retrieve Errors Response: " + cameraResponse
                                    # Process errors

                                    TestAppLogger.Info("Vision Validation Python Script - Clear Warnings")
                                    if CameraSendReceive(tcpClient, "WC\r"):                                                        # Clear Warnings
                                        TestAppLogger.Info("Vision Validation Python Script - Set File Name Override for camera results")
                                        if CameraSendReceive(tcpClient, "FNW,1,0," + str(primaryId) + "\r"):                        # Set File Name Override for camera results
                                            TestAppLogger.Info("Vision Validation Python Script - Send Trigger & Status Results")
                                            if CameraSendReceive(tcpClient, "T2\r"):                                                # Send Trigger & Status Results
                                                tcpSendReceiveSuccess = True
                                                Comments += "Send Trigger & Status Results Response: " + cameraResponse
                                                responseFields = cameraResponse.split(",")
                                                if len(responseFields) > 2:
                                                    if responseFields[2] == "OK":
                                                        isSuccess = True
                cameraTcpRetries += 1

        except Exception as inst:
            LogBoth("Validate Vision Script:  Could not connect to camera - TCP Exception Occurred : " + str(inst), True)            
            FaultDetail += "Validate Vision Script:  Could not connect to camera - " + str(inst) + "\r"

    finally:
        LogBoth("Vision Validation Python Script - Closing TCP Connection " + str(cameraRemoteIpAddress) + ":" + str(cameraRemotePort), False)
        try:
            tcpClient.CloseConnection()
        except Exception as inst:
            LogBoth("Validate Vision Script:  Close TCP Connection Exception Occurred : " + str(inst), True)            
        tcpClient = None
        if tcpSendReceiveSuccess == True:
            TestAppLogger.Info("Vision Validation Python Script - Successfully validated with camera")
        else:
            LogBoth("Vision Validation Python Script - Error completing validation with camera", True)
            Comments += FaultDetail

    if MainTPassScripting.CommandAbortPythonScript == True:
        TestAppLogger.Info("Vision Validation Python Script: TPass commanded to terminate the script")
       
except Exception as inst:
    FaultDetail += "Validate Vision Script:  Exception Occurred - " + str(inst) + "\r"
    Comments += FaultDetail
    TestAppLogger.Warn("Vision Validation Python Script: Exception Occurred :{0}", str(inst))
    TestAppLogger.Warn("Vision Validation Python Script: Processing Failed.")

TestAppLogger.Info("Vision Validation Python Script: Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 01202025
#	Version: 1.0
#	Change: Initial Version
############################################################