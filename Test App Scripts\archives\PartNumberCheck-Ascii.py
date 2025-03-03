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

#rawCanDataResponse = "100D62F13236383137313139334142"
#broadcastedPartNumber = '12345678A'
#print('Raw can data response = ', rawCanDataResponse)

import clr
version = "1.0"
production = False

# string offset starts with 0
partNumberHexByteOffset = 10
isSuccess = True
TestAppLogger.Info("Part Number Check Python Script:  Raw Can Data Response = {0}", rawCanDataResponse)
TestAppLogger.Info("Part Number Check Python Script:  Broadcasted Part Number = {0}", broadcastedPartNumber)
rawCanDataWithoutHeader = rawCanDataResponse[partNumberHexByteOffset:]
TestAppLogger.Info("Part Number Check Python Script:  Raw Can Data without Header = {0}", rawCanDataWithoutHeader)
rawCanDataPartNumberHex = rawCanDataWithoutHeader
try:
	processedPartNumber = bytes.fromhex(rawCanDataWithoutHeader)
	TestAppLogger.Info("Part Number Check Python Script:  Processed Part Number = {0}", processedPartNumber)
	if broadcastedPartNumberWithoutRev != processedPartNumber:
		isSuccess = False
except Exception as inst:
	TestAppLogger.Warn("Part Number Check Python Script:  Exception Occurred :{0}", inst)
	TestAppLogger.Warn("Part Number Check Python Script:  Invalid raw hex string")
	isSuccess = False
TestAppLogger.Info("Part Number Check Python Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 01012019
#	Version: 1.0
#	Change: Initial Version
############################################################


