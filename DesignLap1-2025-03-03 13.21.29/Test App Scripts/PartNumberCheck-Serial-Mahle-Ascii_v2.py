#Part Number Check - Serial Number   Parse raw data ASCII and don't perform the compare against the broadcasted part number
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

#rawCanDataResponse = "101B62F18CFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
#broadcastedPartNumber = '_ESP_010122_085_02_01000_'

import clr
version = "2.0"
production = False

# string offset starts with 0
partNumberHexByteOffset = 10
partNumberHexLength = 48

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
#	Date: 05032022
#	Version: 3.0
#	Change: Added compare check
#	Date: 04202022
#	Version: 1.0
#	Change: Initial Version
############################################################


