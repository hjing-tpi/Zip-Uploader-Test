#Parse DTCs.  Parse raw data Global B DoIP
#
#TPass Objects Passed In/Returned
#   in - string "rawDtcResponse"
#   in - bool "ignoreStatus"
#   in - Function "TestAppLogger"
#   out - dictionary<string, string> "dtcDictionary"
#   out - dictionary<string, string> "allDtcCollection"
#   out bool "isSuccess"
#   out - bool "production"
#   out - string "version"

#System.Diagnostics.Debugger.Break();

#Raw Data: 100F5902FF9595132F9A68922FF002512F
#Raw Data: 5902FFC211002EC246002EC18B002E
#Number of Calculated DTCs: 3
#Number of possible DTCs: 255
#DTC: 9595    FailByte: 13   Status: 2F
#DTC: 9A68    FailByte: 92   Status: 2F
#DTC: F002    FailByte: 51   Status: 2F

import clr
version = "1.0"
production = False

# string offset starts with 0
TestAppLogger.Info("DTC Parsing Python Script:  Raw DTC Data Response = {0}", rawDtcResponse)
TestAppLogger.Info("DTC Parsing Python Script:  Ignore Status = {0}", ignoreStatus)
dtcString = ""

try:
    numberOfDtcs = (len(rawDtcResponse) - 6)/8
    TestAppLogger.Info("DTC Parsing Python Script:  Number of Calculated DTCs = {0}", numberOfDtcs)
    numberOfDtcsPossible = int(rawDtcResponse[4:6], 16)
    TestAppLogger.Info("DTC Parsing Python Script:  Number of DTCs Possible = {0}", numberOfDtcsPossible)
    for x in range(0, numberOfDtcs):
        hold = rawDtcResponse[6+(8*x):6+(8*x)+8]
        statusByte = hold[-2:]
        failByte = hold[4:6]
        hold = hold[:-4]
        try:
            allDtcCollection.Add(hold + failByte, statusByte)
        except:
            TestAppLogger.Info("DTC Parsing Python Script:  Error adding DTC to allDtcCollection.  Either a duplicate DTC or not running TPass version 1.5.0.14 or greater.  {0}", hold + failByte)
        if (int(statusByte, 16) & 12 or ignoreStatus):
            dtcString = dtcString + "DTC: " + hold + ", Fail Byte: " + failByte + " Status: " + statusByte + "\r\n"
            if (not dtcDictionary.ContainsKey(hold + failByte)):
                dtcDictionary.Add(hold + failByte, statusByte)
            else:
                TestAppLogger.Warn("DTC Parsing Python Script:  Duplicate DTC:  :{0}.  DTC won't be saved", hold + failByte)
        else:
            dtcString = dtcString + "DTC: " + hold + ", Fail Byte: " + failByte + " Status: " + statusByte + "Bad Status not saved to DTC list" + "\r\n"
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
#	Date: 11242024
#	Version: 1.0
#	Change: Initial Version
############################################################
