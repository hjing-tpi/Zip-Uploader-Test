#Retrieve Build Data for Product Id
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - string "RunTestCycleId" - This is the data that was passed from the Start Test Cycle script via the RunTestCycle method.
#   in  - COM object "GatsSfeObj" - GM EDI Interface pointer for retrieving build data from GEPICS
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application log file
#   in  - method "GetConfigurationValue" - This is the method to get values set in the System Configuration file
#   out - string "productBuildData" - Build data retrieved to be processed by the Option Parsing script
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#import clr
import System

version = "1.0"
production = False
productBuildData = ""

try:

    TPassLogger.Debug("Option Retrieval Script:  Product Id = {0}", RunTestCycleId)
    isSuccess = True
    productBuildData = RunTestCycleId

except Exception as inst:
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("GmTcpHs", "Option Retrieval Script Exception : " + str(inst), True, True)
    TPassLogger.Warn("Option Retrieval Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Retrieval Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Retrieval Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 10282021
#   Version: 1.0
#   Change: Initial Version
############################################################
