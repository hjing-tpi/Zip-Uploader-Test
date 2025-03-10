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

version = "1.0"
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

TPassLogger.Debug("Option Retrieval Script:  Product Id = {0}", RunTestCycleId)

# Main Logic
try:

    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Trigger Type = " + str(MainTPassScripting.StartTestCycleTriggerType), False, False)
    MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Data = " + RunTestCycleId, False, False)

    # Retrieve the build data using PfcsInterface
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

    # Create Request file for PfcsInterface to read, query the plant PFCS system and write the results
    try:
        File.WriteAllText(requestFile + "TMP", RunTestCycleId)
        File.Move(requestFile + "TMP", requestFile)
        MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Request File Written - " + requestFile, False, False)
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("PfcsInterface", "File.WriteAllText Exception Occurred" + str(inst), True, True)
        TPassLogger.Error("Option Retrieval Script:  File.WriteAllText Exception Occurred :{0}", inst)            

    # Read Build Data File if exist within timeout
    try:
        buildDataFileFound = False
        startDateTime = DateTime.Now
        while (DateTime.Now - startDateTime).TotalMilliseconds < buildDataRequestTimeoutMsec and not buildDataFileFound:
            MainTPassScripting.UpdateEvents()
            if File.Exists(buildDataFile):
                #Read contents and delete file
                MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Build Data File Received - " + buildDataFile, False, False)
                try:
                    productBuildData = File.ReadAllText(buildDataFile)
                except Exception as inst:
                    MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Build Data File locked by PFCS Interface, trying again", True, False)
                    TPassLogger.Debug("Option Retrieval Script:  File.Exists Exception Occurred, Keep trying :{0}", inst)    
                    DelayStartDateTime = DateTime.Now
                    while (DateTime.Now - DelayStartDateTime).TotalMilliseconds < 100:
                        MainTPassScripting.UpdateEvents()
                else:
                    buildDataFileFound = True
                    MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Build Data Received - " + productBuildData, False, False)
                    isSuccess = True

                    try:
                        File.Delete(buildDataFile)
                    except Exception as inst:
                        TPassLogger.Debug("Option Retrieval Script:  File.ReadAllText Exception Occurred :{0}", inst)            
            

        if buildDataFileFound == False:
            MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Build Data File Not Received - " + buildDataFile, True, False)
            productBuildData = ""
    
    except Exception as inst:
        MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Read Build Data File Exception Occurred" + str(inst), True, True)
        TPassLogger.Error("Option Retrieval Script:  Read Build Data File Exception Occurred :{0}", inst)            
        
except Exception as inst:
    MainTPassScripting.InterfaceUiLogger("PfcsInterface", "Get Build Data Failed: " + str(inst), True, True)
    TPassLogger.Warn("Option Retrieval Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Retrieval Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Retrieval Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 11282023
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################
