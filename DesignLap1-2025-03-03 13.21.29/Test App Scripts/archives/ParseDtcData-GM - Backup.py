#Parse DTCs.  Parse raw data GDDS
#
#TPass Objects Passed In/Returned
#   in - string "rawCanDataResponse"
#   in - bool "isMultiFrameMessage"
#   in - bool "ignoreStatus"
#   in - Function "TestAppLogger"
#   out - dictionary<string, string> "dtcDictionary"
#   out bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#   out - bool "parsingDtcComplete"
#

#System.Diagnostics.Debugger.Break();

import clr
version = "1.0"
production = False

try:
    # string offset starts with 0
    TestAppLogger.Info("DTC Parsing Python Script:  Raw Can Data Response = {0}", rawCanDataResponse)
    TestAppLogger.Info("DTC Parsing Python Script:  Is Multiframe = {0}", isMultiFrameMessage)
    TestAppLogger.Info("DTC Parsing Python Script:  Ignore Status = {0}", ignoreStatus)

    TestAppLogger.Info("DTC Parsing Python Script:  GM Single Frame Response")
    dtc = rawCanDataResponse[2:6]
    statusByte = rawCanDataResponse[6:8]

    if (rawCanDataResponse[0:8] == "81000000"):
        TestAppLogger.Info("DTC Parsing Python Script:  End of DTC Responses, Parsing is Complete")
        parsingDtcComplete = True
    else:
        parsingDtcComplete = False
    if not parsingDtcComplete:
        if (not dtcDictionary.ContainsKey(dtc+statusByte)):
            dtcDictionary.Add(dtc+statusByte, statusByte)
            TestAppLogger.Info("DTC Parsing Python Script:  DTC Added: {0}, Status = {1}", dtc+statusByte, statusByte)
        else:
            TestAppLogger.Warn("DTC Parsing Python Script:  Duplicate DTC:  :{0}.  DTC won't be saved", dtc+statusByte)
    isSuccess = True
except Exception as inst:
    TestAppLogger.Warn("DTC Parsing Python Script:  Exception Occurred :{0}", inst)
    TestAppLogger.Warn("DTC Parsing Python Script:  Processing Failed.")
    isSuccess = False
    parsingDtcComplete = True
TestAppLogger.Info("DTC Parsing Python Script:  Is Success = {0}", isSuccess)
TestAppLogger.Info("DTC Parsing Python Script:  Parsing Dtc Complete = {0}", parsingDtcComplete)

############################################################
# Change History
############################################################
#	Date: 01012019
#	Version: 1.0
#	Change: Initial Version
############################################################
