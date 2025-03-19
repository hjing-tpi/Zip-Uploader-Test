#Retrieve Build Data for Product Id
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - string "RunTestCycleId" - This is the data that was passed from the Start Test Cycle script via the RunTestCycle method.
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application Detail log file
#   in  - object "SystemConfigurationValue" - This is the object to get values set in the System Configuration file
#   out - string "productBuildData" - Build data retrieved to be processed by the Option Parsing script
#   out - bool "isSuccess" - Set to True if build data retrieval was successful.  Otherwise False
#   out - bool "production"
#   out - string "version"
#

from System.IO import File
from System import DateTime

version = "2.0"
production = False
productBuildData = ""
isSuccess = False


#########################################################################################################################################
# Application Engineer:  Specific constant variables to maintain
#
buildDataRequestTimeoutMsec = 5000
requestFile = "C:\TPass\Data Outgoing\Request.txt"
buildDataFile = "C:\TPass\Data Incoming\Options.txt"
#
#########################################################################################################################################


# Main Logic
try:

    TPassLogger.Debug("Option Retrieval Script:  Product Id = {0}", RunTestCycleId)
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Trigger Type = " + str(MainTPassScripting.StartTestCycleTriggerType), False, False)
    MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "RunTestCycleId = " + RunTestCycleId, False, False)

    #Add logic to get the recipe from the PLC
    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Modbus):

        # Remove request and build data files if exist
        if File.Exists(requestFile + "TMP"):
            try:
                File.Delete(requestFile + "TMP")
            except Exception as inst:
                TPassLogger.Debug("Option Retrieval Script:  File.Delete Exception Occurred :{0}", inst)            
        if File.Exists(requestFile):
            try:
                File.Delete(requestFile)
            except Exception as inst:
                TPassLogger.Debug("Option Retrieval Script:  File.Delete Exception Occurred :{0}", inst)            
        if File.Exists(buildDataFile):
            try:
                File.Delete(buildDataFile)
            except Exception as inst:
                TPassLogger.Debug("Option Retrieval Script:  File.Delete Exception Occurred :{0}", inst)            

        # Create Request file for SQLConnect to read, query the plant database and write the results
        try:
            File.WriteAllText(requestFile + "TMP", RunTestCycleId + "\r\n")
            File.Move(requestFile + "TMP", requestFile)
            MainTPassScripting.InterfaceUiLogger("SQLConnect", "Request File Written - " + requestFile, False, False)
        except Exception as inst:
            MainTPassScripting.InterfaceUiLogger("SQLConnect", "File.WriteAllText Exception Occurred" + str(inst), True, True)
            TPassLogger.Error("Option Retrieval Script:  File.WriteAllText Exception Occurred :{0}", inst)            

        # Read Build Data File if exist within timeout
        try:
            buildDataFileFound = False
            startDateTime = DateTime.Now
            while (DateTime.Now - startDateTime).TotalMilliseconds < buildDataRequestTimeoutMsec and not buildDataFileFound:
                MainTPassScripting.UpdateEvents()
                if File.Exists(buildDataFile):
                    buildDataFileFound = True
                    MainTPassScripting.InterfaceUiLogger("SQLConnect", "Build Data File Received - " + buildDataFile, False, False)

                    #Read contents and delete file
                    productBuildData = File.ReadAllText(buildDataFile)
                    MainTPassScripting.InterfaceUiLogger("SQLConnect", "Build Data Received - " + productBuildData, False, False)
                    isSuccess = True

                    try:
                        File.Delete(buildDataFile)
                    except Exception as inst:
                        TPassLogger.Debug("Option Retrieval Script:  File.Delete Exception Occurred :{0}", inst)            

            if buildDataFileFound == False:
                MainTPassScripting.InterfaceUiLogger("SQLConnect", "Build Data File Not Received - " + buildDataFile, True, False)
                productBuildData = ""
        
        except Exception as inst:
            MainTPassScripting.InterfaceUiLogger("SQLConnect", "Read Build Data File Exception Occurred" + str(inst), True, True)
            TPassLogger.Error("Option Retrieval Script:  Read Build Data File Exception Occurred :{0}", inst)            
        
    else:
        MainTPassScripting.InterfaceUiLogger("SQLConnect", "Button Push, no need to interface with SQLConnect", False, False)
        TPassLogger.Debug("Option Retrieval Script - Button Push, no need to interface with SQLConnect")
        productBuildData = RunTestCycleId
        # Force Options Screen Selection to allow for Operator to change the options
        isSuccess = False


except Exception as inst:
    MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Get Build Data Failed: " + str(inst), True, True)
    TPassLogger.Warn("Option Retrieval Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Retrieval Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Retrieval Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 05042023
#   Version: 2.0
#   ChangeBy: RMM
#   Change: SQLConnect interface
#   Date: 04172023
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################
