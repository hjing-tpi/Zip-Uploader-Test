#Part Number Check.  Parse raw data ASCII 8 in Length
#
#TPass Objects Passed In/Returned
#   in - string "broadcastedPartNumber"
#   in - string "rawCanDataResponse"
#   in - Function "TestAppLogger"
#   out - string "processedPartNumber"
#   out - string "rawCanDataPartNumberHex"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#


#System.Diagnostics.Debugger.Break();

#rawCanDataResponse = "065ACB00CE5FBAAA"
#broadcastedPartNumber = '13524922'
#print('Raw can data response = ', rawCanDataResponse)

import clr
version = "1.0"
production = False

# string offset starts with 0
partNumberHexByteOffset = 6
isSuccess = True
try:
	TestAppLogger.Info("Part Number Check Python Script:  Raw Can Data Response = {0}", rawCanDataResponse)
	TestAppLogger.Info("Part Number Check Python Script:  Broadcasted Part Number = {0}", broadcastedPartNumber)
	rawCanDataPartNumberHex = rawCanDataResponse[partNumberHexByteOffset:partNumberHexByteOffset+8]
	TestAppLogger.Info("Part Number Check Python Script:  Raw Can Data Part Number Hex = {0}", rawCanDataPartNumberHex)
	processedPartNumber = long(rawCanDataPartNumberHex, 16)
	TestAppLogger.Info("Part Number Check Python Script:  Processed Part Number = {0}", processedPartNumber)
	if processedPartNumber != long(broadcastedPartNumber):
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


