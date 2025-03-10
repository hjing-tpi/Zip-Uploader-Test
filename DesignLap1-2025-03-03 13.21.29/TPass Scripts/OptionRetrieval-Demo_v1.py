#Retrieve Build Data for Product Id
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - string "RunTestCycleId" - This is the data that was passed from the Start Test Cycle script via the RunTestCycle method.
#   in  - COM object "GatsSfeObj" - DEMO Interface pointer for retrieving build data from GEPICS
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application log file
#   in  - method "GetConfigurationValue" - This is the method to get values set in the System Configuration file
#   out - string "productBuildData" - Build data retrieved to be processed by the Option Parsing script
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

import clr
import System

version = "1.0"
production = False
productBuildData = ""

#########################################################################################################################################
# Application Engineer:  Set the assembly line number below if the TPass Tool is on a different assembly line specified by GEPICS
#
assyLine = 1
#
#########################################################################################################################################

TPassLogger.Debug("Option Retrieval Script:  Product Id = {0}", RunTestCycleId)
try:

    refProductBuildData = clr.Reference[System.String]()
    refBuildDataSource = clr.Reference[System.String]()
    refReturnValue = clr.Reference[System.Int32]()

    GatsSfeObj.SfeGetBuildData("", RunTestCycleId, assyLine, refProductBuildData, 0,  refBuildDataSource, "C:\\EDISERVER\\BUILDDATA\\ALT.GAD", refReturnValue);

    TPassLogger.Debug("Option Retrieval Script:  Return from DEMO = {0}", refReturnValue.Value)
    if refReturnValue.Value == 0x40000:
        productBuildData = refProductBuildData.Value
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("DEMO", "Build Data FOUND for Primary Id = " + RunTestCycleId + ", Build Data = " + productBuildData, False, False)
        MainTPassScripting.InterfaceUiLogger("DEMO", "Build Data Source = " + refBuildDataSource.Value, False, False)
        TPassLogger.Debug("Option Retrieval Script:  Product Build Data from DEMO = {0}", productBuildData)
        TPassLogger.Debug("Option Retrieval Script:  Build Data Source from DEMO = {0}", refBuildDataSource.Value)
        isSuccess = True
    else:
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
        MainTPassScripting.InterfaceUiLogger("DEMO", "Build Data NOT FOUND for Primary Id = " + RunTestCycleId, True, False)
        TPassLogger.Debug("Option Retrieval Script:  Build Data NOT FOUND for Product Id = {0}", RunTestCycleId)
        isSuccess = False

except Exception as inst:
    # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
    MainTPassScripting.InterfaceUiLogger("DEMO", "Get Build Data for Primary Id " + RunTestCycleId + ": " + str(inst), True, True)
    TPassLogger.Warn("Option Retrieval Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Retrieval Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Retrieval Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 04152021
#   Version: 1.0
#   Change: Initial Version
############################################################
