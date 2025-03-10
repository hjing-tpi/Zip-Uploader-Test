# Retrieve Build Data for Product
# This Script is expected to set the out parameter productBuildData.  If this script fails, the Option Selection Screen will be presented to the operator.
#
# TPass Objects Passed In/Returned
#   in  - string "RunTestCycleId" - This is the data that was passed from the Start Test Cycle script via the RunTestCycle method.
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
#   out - string "productBuildData"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

import clr

version = "1.0"
production = False
TPassLogger.Debug("Product Attribute Retrieval Script:  RunTestCycleId = {0}", RunTestCycleId)

try:

    # Request build data from the plants MES system using the passed in "RequestScriptData" 
    productBuildData = ""
    isSuccess = True

except Exception as inst:
    TPassLogger.Warn("Product Attribute Retrieval Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Product Attribute Retrieval Script:  Processing Failed.")
    isSuccess = False

TPassLogger.Info("Product Attribute Retrieval Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 01172021
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################
