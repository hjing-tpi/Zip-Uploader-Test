#Part Number Check ETM WD - Parse raw data and compare with numeric broadcasted part number.  Actual part number must be >= broadcasted part number
#
#TPass Objects Passed In/Returned
#   in - string "broadcastedPartNumber"
#   in - string "rawCanDataResponse"
#   in - Function "TestAppLogger"
#   out - string "processedPartNumber
#   out - string "rawCanDataPartNumberHex"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#


#System.Diagnostics.Debugger.Break();

#rawCanDataResponse = "100E62F19509F4000000000000000000000000000000"
#broadcastedPartNumber = "2548"

import clr
version = "1.0"
production = False

# string offset starts with 0
partNumberHexByteOffset = 10
partNumberHexLength = 4

isSuccess = True
try:
    TestAppLogger.Info("Part Number Check Python Script:  Raw Can Data Response = {0}", rawCanDataResponse)
    TestAppLogger.Info("Part Number Check Python Script:  Broadcasted Part Number = {0}", broadcastedPartNumber)

    rawCanDataPartNumberHex = rawCanDataResponse[partNumberHexByteOffset:partNumberHexByteOffset+partNumberHexLength]
    TestAppLogger.Info("Part Number Check Python Script:  Raw Can Data Part Number = {0}", rawCanDataPartNumberHex)

    processedPartNumberInt = int(rawCanDataPartNumberHex, 16)
    processedPartNumber = str(processedPartNumberInt)
    broadcastedPartNumberInt = int(broadcastedPartNumber, 10)
    TestAppLogger.Info("Part Number Check Python Script:  Processed Part Number = {0}", processedPartNumber)
    if processedPartNumberInt < broadcastedPartNumberInt:
        isSuccess = False
except Exception as inst:
    TestAppLogger.Warn("Part Number Check Python Script:  Exception Occurred :{0}", inst)
    TestAppLogger.Warn("Part Number Check Python Script:  Invalid raw hex string or broadcasted part number")
    isSuccess = False
TestAppLogger.Info("Part Number Check Python Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 01032023
#	Version: 1.0
#	Change: Initial Version
############################################################


