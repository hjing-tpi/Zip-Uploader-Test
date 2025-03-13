#Parse Product Id Input sent to TPass, either by Keyboard, Scanner, File Drop, Serial etc.
#This Script is expected to set the out parameters parsedProductId and productBuildData if appropriate
#TPass will set the PrimaryID to the parsedProductId passed back from this script
#TPass Objects Passed In/Returned
#   in - string "productIdInput"
#   in - Function "TPassLogger"
#   out - string "parsedProductId"
#   out - string "productBuildData"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

import clr
version = "1.0"
production = False

TPassLogger.Debug("Parse Product Id Script:  Product Id Input = {0}", productIdInput)

try:
#   if productIdInput.Length == 6:
        parsedProductId = productIdInput
        productBuildData = ""
        TPassLogger.Info("Parse Product Id Script:  Parsed Product Id = {0}", parsedProductId)
        TPassLogger.Info("Parse Product Id Script:  Parsed Build Data = {0}", productBuildData)
        isSuccess = True
#   else:
#       isSuccess = False

except Exception as inst:
    TPassLogger.Warn("Parse Product Id Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Parse Product Id Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Parse Product Id Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 01012019
#   Version: 1.0
#   Change: Initial Version
############################################################
