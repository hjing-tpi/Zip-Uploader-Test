#Ktb Buckle Data.  Parse raw data HEX 
#
#TPass Objects Passed In/Returned
#   in - string "buckleStatusMessageHex"
#   in - Function "TPassLogger"
#   out - bool "buckle1Status"
#   out - bool "buckle2Status"
#   out - bool "buckle3Status"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#


#System.Diagnostics.Debugger.Break();

#buckleStatusMessageHex = "40FFFC03FC03FC03FFFF30C8070030C8070030C80700"

import clr
from System import String
from System import Convert

version = "1.0"
production = False

buckle1 = 0x10
buckle2 = 0x20
buckle3 = 0x40
buckle1Status = False
buckle2Status = False
buckle3Status = False
buckleDataHexByteOffset = 0

isSuccess = True
try:
    TestAppLogger.Info("KtbBuckle Python Script:  Buckle Status Message Hex = {0}", buckleStatusMessageHex)
    buckleByte = Convert.ToByte(buckleStatusMessageHex[buckleDataHexByteOffset:2], 16)
    TestAppLogger.Info("KtbBuckle Python Script:  Buckle 1 Byte = {0}", str(buckle1))
    TestAppLogger.Info("KtbBuckle Python Script:  Buckle 2 Byte = {0}", str(buckle2))
    TestAppLogger.Info("KtbBuckle Python Script:  Buckle 3 Byte = {0}", str(buckle3))
    TestAppLogger.Info("KtbBuckle Python Script:  Buckle Status Byte = {0}", str(buckleByte))
    if ((buckleByte&buckle1) == buckle1):
        buckle1Status = True
    if ((buckleByte&buckle2) == buckle2):
        buckle2Status = True
    if ((buckleByte&buckle3) == buckle3):
        buckle3Status = True


    TestAppLogger.Info("KtbBuckle Python Script:  Buckle1 = {0}", buckle1Status)
    TestAppLogger.Info("KtbBuckle Python Script:  Buckle2 = {0}", buckle2Status)
    TestAppLogger.Info("KtbBuckle Python Script:  Buckle3 = {0}", buckle3Status)

except Exception as inst:
    TestAppLogger.Warn("KtbBuckle Python Script:  Exception Occurred :{0}", inst)
    TestAppLogger.Warn("KtbBuckle Python Script:  Invalid raw hex string")
    isSuccess = False
    
TestAppLogger.Info("KtbBuckle Python Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 04162023
#   Version: 1.0
#   Change: Initial Version
############################################################


