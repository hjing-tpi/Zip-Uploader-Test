#Magna PIP Line Release.  If antennas 1,2 and 3 are all in their cradle, set the tooling clear PLC tag to 1, otherwise set to 0
#This Script can run any python logic and can also run a TPass Test Application
#TPass Objects Passed In/Returned
#   in  - object MainTPassScripting - Exposed all methods and properties for the scripts to use
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - ushort "PipModbusStatus" - 8 or 16 bit status of the PIP Modbus inputs
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();

import clr
#clr.AddReference('TPI.PLCCommunication')
#from TPI.PLCommunication import LogixDriver
#import TPI.PLCommunication
#from TPI.PLCommunication import CIP, LogixDriver
from System.IO import File
from System import DateTime


version = "1.0"
production = False

TPassLogger.Debug("Magna PIP Line Release Script Begin")

#cip = CIP("10.66.48.130/0")
#plc = TPI.PLCommunication.LogixDriver("10.66.48.130/0", 1)
#cip = TPI.PLCommunication.CIP("10.66.48.130/0")
#plc = TPI.PLCommunication.LogixDriver("127.0.0.1/0", 1)
#plcTag = "WBS_Tester_1.Tooling_Clear"
#plcTagType = TPI.PLCommunication.Common.DataTypes.BOOL


lineRelease = "C:\TPass\Data Outgoing\PlcLineClear.txt"

try:
    TPassLogger.Debug("Magna PIP Line Release Script: Run Line Release.  PipModbusStatus = " + format(int(PipModbusStatus), "b"))
    antennaStatus = PipModbusStatus & 0x7
    TPassLogger.Info("Magna PIP Line Release Script: Run Line Release.  PipModbusStatus = " + format(int(PipModbusStatus), "b") + ", AntennaStatus = " + format(int(antennaStatus), "b"))
    
#    InterfaceErrorMessage.InterfaceUiLogger("Line Release", "PipModbusStatus = " + str(PipModbusStatus) + ", AntennaStatus = " + str(antennaStatus), False, False)

    # if antennaStatus == 0x7:
        # TPassLogger.Info("Magna PIP Line Release Script: Antennas are all in their nest")
# #        MainTPassScripting.InterfaceUiLogger("Line Release", "Antennas are all in their nest.  Writing 1 to " + plcTag, False, False)
        # plc.Write(plcTag, "1", plcTagType)
        # isSuccess = True
    # else:
        # TPassLogger.Info("Magna PIP Line Release Script: Antennas aren't all in their nest")
# #        InterfaceErrorMessage.InterfaceUiLogger("Line Release", "Antennas aren't all in their nest.  Writing 0 to " + plcTag, False, False)
        # plc.Write(plcTag, "0", plcTagType)
        # isSuccess = True

    if File.Exists(lineRelease):
        try:
            File.Delete(lineRelease)
        except Exception as inst:
            TPassLogger.Debug("Magna PIP Line Release Script:  File.Delete Exception Occurred :{0}", inst)            

            startDateTime = DateTime.Now
            while (DateTime.Now - startDateTime).TotalMilliseconds < 100:
                MainTPassScripting.UpdateEvents()
            try:
                File.Delete(lineRelease)
            except Exception as inst:
                TPassLogger.Debug("Magna PIP Line Release Script:  File.Delete Exception Occurred :{0}", inst)            
            
    if not File.Exists(lineRelease):
        if File.Exists(lineRelease + "TMP"):
            try:
                File.Delete(lineRelease + "TMP")
            except Exception as inst:
                TPassLogger.Debug("Magna PIP Line Release Script:  File.Delete Exception Occurred :{0}", inst)            
        if antennaStatus == 0x7:
            #MainTPassScripting.InterfaceUiLogger("Line Release", "Antennas are all in their nest.  Writing 1 to Line Clear File", False, False)
            TPassLogger.Info("Magna PIP Line Release Script: Writing status 1 to Interface to write to PLC tag")
            File.WriteAllText(lineRelease + "TMP", "1")
        else:
            #MainTPassScripting.InterfaceUiLogger("Line Release", "Antennas are not all in their nest.  Writing 0 to  Line Clear File", False, False)
            TPassLogger.Info("Magna PIP Line Release Script: Writing status 0 to Interface to write to PLC tag")
            File.WriteAllText(lineRelease + "TMP", "0")
        File.Move(lineRelease + "TMP", lineRelease)
        #MainTPassScripting.InterfaceUiLogger("Line Release", "Antennas are all in their nest.  Writing 1 to " + plcTag, False, False)
        TPassLogger.Info("Magna PIP Line Release Script: Creating Line Release File")
#        MainTPassScripting.InterfaceUiLogger("Line Release", "Created Line Release File", False, False)
        isSuccess = True
    else:
        TPassLogger.Info("Magna PIP Line Release Script: Line Release File Already Exists and can't delete it")
#        MainTPassScripting.InterfaceUiLogger("Line Release", "Line Release File Already Exists and can't delete it", True, True)
        isSuccess = False

except Exception as inst:
    TPassLogger.Warn("Magna PIP Line Release Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Magna PIP Line Release Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Magna PIP Line Release Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 11012023
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################

