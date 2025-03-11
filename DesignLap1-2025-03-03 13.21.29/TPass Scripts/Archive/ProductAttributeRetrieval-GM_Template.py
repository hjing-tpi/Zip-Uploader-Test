#Retrieve Build Data for Product Id
#This Script is expected to set the out parameter partBuildData
#TPass Objects Passed In/Returned
#   in - string "partId"
#   in - object "gatsSfeObj"
#   in - Function "TPassLogger"
#   out - string "productBuildData"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

import clr
import System
#from ctypes import *
#import comtypes
#import win32com.client
#ediBuildData = POINTER(comtypes.BSTR)
version = "1.0"
production = False
productBuildData = ""
TPassLogger.Debug("Product Attribute Retrieval Script:  Product Id = {0}", productId)

try:

    assyLine = 1
    refProductBuildData = clr.Reference[System.String]()
    refBuildDataSource = clr.Reference[System.String]()
    refReturnValue = clr.Reference[System.Int32]()

    gatsSfeObj.SfeGetBuildData("", productId, assyLine, refProductBuildData, 0,  refBuildDataSource, "C:\\EDISERVER\\BUILDDATA\\ALT.GAD", refReturnValue);

    TPassLogger.Debug("Product Attribute Retrieval Script:  Return from GM EDI = {0}", refReturnValue.Value)
    if refReturnValue.Value == 0x40000:
        productBuildData = refProductBuildData.Value
        TPassLogger.Debug("Product Attribute Retrieval Script:  Product Build Data from GM EDI = {0}", productBuildData)
        TPassLogger.Debug("Product Attribute Retrieval Script:  Build Data Source from GM EDI = {0}", refBuildDataSource.Value)
        isSuccess = True
    else:
        TPassLogger.Debug("Product Attribute Retrieval Script:  Build Data NOT FOUND for Product Id = {0}", productId)
        isSuccess = False

except Exception as inst:
    TPassLogger.Warn("Product Attribute Retrieval Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Product Attribute Retrieval Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Product Attribute Retrieval Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 01012019
#   Version: 1.0
#   Change: Initial Version
############################################################
