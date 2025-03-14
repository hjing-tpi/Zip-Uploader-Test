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
#

#System.Diagnostics.Debugger.Break();

import clr
version = "2.0"
production = False

# string offset starts with 0
TestAppLogger.Info("DTC Parsing Python Script:  Raw Can Data Response = {0}", rawCanDataResponse)
TestAppLogger.Info("DTC Parsing Python Script:  Is Multiframe = {0}", isMultiFrameMessage)
TestAppLogger.Info("DTC Parsing Python Script:  Ignore Status = {0}", ignoreStatus)
dtcString = ""

if isMultiFrameMessage:
    try:
        TestAppLogger.Info("DTC Parsing Python Script:  Multiple Frame Response")
        numberOfDtcs = ((int(rawCanDataResponse[1:4], 16)-3)/4)
        TestAppLogger.Info("DTC Parsing Python Script:  Number of Calculated DTCs = {0}", numberOfDtcs)
        numberOfDtcsPossible = int(rawCanDataResponse[8:10], 16)
        TestAppLogger.Info("DTC Parsing Python Script:  Number of DTCs Possible = {0}", numberOfDtcsPossible)
        for x in range(0, numberOfDtcs):
            hold = rawCanDataResponse[10+(8*x):10+(8*x)+8]
            statusByte = hold[-2:]
            hold = hold[:-4]
            if (int(statusByte, 16) & 12 or ignoreStatus):
                dtcString = dtcString + "DTC: " + hold + " Status: " + statusByte + "\r\n"
                if (not dtcDictionary.ContainsKey(hold)):
                    dtcDictionary.Add(hold, statusByte)
                else:
                    TestAppLogger.Warn("DTC Parsing Python Script:  Duplicate DTC:  :{0}.  DTC won't be saved", hold)
            else:
                dtcString = dtcString + "DTC: " + hold + " Status: " + statusByte + "Bad Status not saved to DTC list" + "\r\n"
        isSuccess = True

    except Exception as inst:
        TestAppLogger.Warn("DTC Parsing Python Script:  Exception Occurred :{0}", inst)
        TestAppLogger.Warn("DTC Parsing Python Script:  Processing Failed.")
        isSuccess = False
else:
    try:
        TestAppLogger.Info("DTC Parsing Python Script:  Single Frame Response")
        if (int(rawCanDataResponse[0:2], 16) == 7):
            hold = rawCanDataResponse[8: 16]
            statusByte = hold[-2:]
            hold = hold[:-4]
            if (int(statusByte, 16) & 12 or ignoreStatus):
                dtcString = dtcString + "DTC: " + hold + " Status: " + statusByte + "\r\n"
                if (not dtcDictionary.ContainsKey(hold)):
                    dtcDictionary.Add(hold, statusByte)
                else:
                    TestAppLogger.Warn("DTC Parsing Python Script:  Duplicate DTC:  :{0}.  DTC won't be saved", hold)
            else:
                dtcString = dtcString + "DTC: " + hold + " Status: " + statusByte + "Bad Status not saved to DTC list" + "\r\n"
        else:
            TestAppLogger.Info("DTC Parsing Python Script:  No DTCs detected")
        isSuccess = True
    except Exception as inst:
        TestAppLogger.Warn("DTC Parsing Python Script:  Exception Occurred :{0}", inst)
        TestAppLogger.Warn("DTC Parsing Python Script:  Processing Failed.")
        isSuccess = False
TestAppLogger.Info("DTC Parsing Python Script:  DTC Summary: \r\n{0}", dtcString )
TestAppLogger.Info("DTC Parsing Python Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 10042021
#	Version: 2.0
#	Change: Fixed if Multiframe message and only having one DTC reported
#	Date: 01012019
#	Version: 1.0
#	Change: Initial Version
############################################################
