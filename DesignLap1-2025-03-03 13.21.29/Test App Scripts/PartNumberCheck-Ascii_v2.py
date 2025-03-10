#Part Number Check.  Parse raw data ASCII
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

#rawCanDataResponse = "000D62F1323638343130363139414600"
#broadcastedPartNumber = '68410619AF'

import clr
version = "2.0"
production = False

# string offset starts with 0
partNumberHexByteOffset = 10
partNumberHexLength = 20

isSuccess = True
try:
    TestAppLogger.Info("Part Number Check Python Script:  Raw Can Data Response = {0}", rawCanDataResponse)
    TestAppLogger.Info("Part Number Check Python Script:  Broadcasted Part Number = {0}", broadcastedPartNumber)

    rawCanDataPartNumberHex = rawCanDataResponse[partNumberHexByteOffset:partNumberHexByteOffset+partNumberHexLength]
    TestAppLogger.Info("Part Number Check Python Script:  Raw Can Data Part Number = {0}", rawCanDataPartNumberHex)

    processedPartNumber = bytes.fromhex(rawCanDataPartNumberHex)
    TestAppLogger.Info("Part Number Check Python Script:  Processed Part Number = {0}", processedPartNumber)
    if broadcastedPartNumber != processedPartNumber:
        isSuccess = False
except Exception as inst:
    TestAppLogger.Warn("Part Number Check Python Script:  Exception Occurred :{0}", inst)
    TestAppLogger.Warn("Part Number Check Python Script:  Invalid raw hex string")
    isSuccess = False
TestAppLogger.Info("Part Number Check Python Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 10082021
#	Version: 2.0
#	Change: Fixed issue not using the correct broadcasted part number property
#	Date: 01012019
#	Version: 1.0
#	Change: Initial Version
############################################################


