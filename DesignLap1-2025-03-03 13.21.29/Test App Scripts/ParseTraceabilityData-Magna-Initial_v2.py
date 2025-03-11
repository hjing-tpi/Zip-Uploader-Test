#Traceability Data.  Parse raw data HEX 
#
#TPass Objects Passed In/Returned
#   in - string "seatType"
#   in - string "rawCanDataResponse"
#   in - Function "TPassLogger"
#   out - string "traceFaultText"
#   out - string "rawCanDataTraceabilityHex"
#   out - dictionary<string key, string value> "processedTraceabilityData"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#


#System.Diagnostics.Debugger.Break();

#rawCanDataResponse = "105AFA7100FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF000000000000FF80397E560C32383735323139332020523232313636202030303132334E4C3742313442343232424220202020202020202020202020202020202020202020202020"
rawCanDataResponse = "105AFA714845FF800056E10000000000000000008C8C488498177A80397E560C32383735323139332020523232313636202030303132334E4C3742313442343232424220202020202020202020202020202020202020202020202020"
seatType = '22_54_30W_BL_LEATHER_MCS'

traceFaultText = ""

import clr
from System import String
from System import Convert
from System.Collections.Generic import Dictionary
version = "2.0"
production = False

# string offset starts with 0
traceDataHexByteOffset = 8
isSuccess = True
try:
    TPassLogger.Info("Traceability Python Script:  Raw Can Data Response = {0}", rawCanDataResponse)
    TPassLogger.Info("Traceability Python Script:  Seat Type = {0}", seatType)
    rawCanDataTraceDataHex = rawCanDataResponse[traceDataHexByteOffset::]
    TPassLogger.Info("Traceability Python Script:  Raw Can Data Traceability Data Hex = {0}", rawCanDataTraceDataHex)
    processedTraceabilityData = Dictionary[String,String]()
    processedTraceabilityData.Add("ECU","SDPS")
    rodbytearray = bytes.fromhex(rawCanDataTraceDataHex)

    TPassLogger.Info("Traceability Python Script:  byte array = {0}", rodbytearray)
    ## Checks if rawCanDataTraceDataHex is atleast 168 in length
    rawCanDataTraceLength = len(rawCanDataTraceDataHex)

    if rawCanDataTraceLength >= 168:

        # EmptyThreshold
        byteRange =  rawCanDataTraceDataHex[0:2]
        processedTraceabilityData.Add("EmptyThreshold", byteRange)   
        # AllowThreshold
        byteRange = rawCanDataTraceDataHex[2:4]
        processedTraceabilityData.Add("AllowThreshold", byteRange)
        # AdultAllowThreshold
        byteRange = rawCanDataTraceDataHex[4:6]
        processedTraceabilityData.Add("AdultAllowThreshold", byteRange)
        # Seat_Plant_EOL_Verification
        byteRange = rawCanDataTraceDataHex[6:8]
        processedTraceabilityData.Add("Seat_Plant_EOL_Verification", byteRange)
        # Vehicle_EOL_Cal_Status
        byteRange = rawCanDataTraceDataHex[8:10]
        processedTraceabilityData.Add("Vehicle_EOL_Cal_Status", byteRange)
        # EOL_ChecksumMSB
        byteRange = rawCanDataTraceDataHex[10:12]
        processedTraceabilityData.Add("EOL_ChecksumMSB", byteRange)
        # EOL_ChecksumLSB
        byteRange = rawCanDataTraceDataHex[12:14]
        processedTraceabilityData.Add("EOL_ChecksumLSB", byteRange)
        # FTS_Process_Failure_Code
        byteRange = rawCanDataTraceDataHex[14:16]
        processedTraceabilityData.Add("FTS_Process_Failure_Code", byteRange)
        # Calculated_Failed_ValueByte1
        byteRange = rawCanDataTraceDataHex[16:18]
        processedTraceabilityData.Add("Calculated_Failed_ValueByte1", byteRange)
        # Calculated_Failed_ValueByte2
        byteRange = rawCanDataTraceDataHex[18:20]
        processedTraceabilityData.Add("Calculated_Failed_ValueByte2", byteRange)
        # ECU_Fault_CodeByte1
        byteRange = rawCanDataTraceDataHex[20:22]
        processedTraceabilityData.Add("ECU_Fault_CodeByte1", byteRange)
        # ECU_Fault_CodeByte2
        byteRange = rawCanDataTraceDataHex[22:24]
        processedTraceabilityData.Add("ECU_Fault_CodeByte2", byteRange)
        # ECU_Fault_CodeByte3
        byteRange = rawCanDataTraceDataHex[24:26]
        processedTraceabilityData.Add("ECU_Fault_CodeByte3", byteRange)
        # ECU_Fault_CodeByte4
        byteRange = rawCanDataTraceDataHex[26:28]
        processedTraceabilityData.Add("ECU_Fault_CodeByte4", byteRange)
        # ECU_Fault_CodeByte5
        byteRange = rawCanDataTraceDataHex[28:30]
        processedTraceabilityData.Add("ECU_Fault_CodeByte5", byteRange)
        # ECU_Fault_CodeByte6
        byteRange = rawCanDataTraceDataHex[30:32]
        processedTraceabilityData.Add("ECU_Fault_CodeByte6", byteRange)
        # Threshold1Pressure
        byteRange = rawCanDataTraceDataHex[32:34]
        processedTraceabilityData.Add("Threshold1Pressure", byteRange)
        # Threshold2Pressure
        byteRange = rawCanDataTraceDataHex[34:36]
        processedTraceabilityData.Add("Threshold2Pressure", byteRange)
        # EmptyPressure
        byteRange = rawCanDataTraceDataHex[36:38]
        processedTraceabilityData.Add("EmptyPressure", byteRange)
        # Config_Id
        byteRange = rawCanDataTraceDataHex[38:40]
        processedTraceabilityData.Add("Config_Id", byteRange)
        # HCSScaleFactor
        byteRange = rawCanDataTraceDataHex[38:40]
        processedTraceabilityData.Add("HCSScaleFactor", byteRange)
        # R_AVG_Temperature
        byteRange = rawCanDataTraceDataHex[40:42]
        processedTraceabilityData.Add("R_AVG_Temperature", byteRange)
        # TempCounts
        byteRange = rawCanDataTraceDataHex[42:44]
        processedTraceabilityData.Add("TempCounts", byteRange)
        # BladderEOLverification
        byteRange = rawCanDataTraceDataHex[44:46]
        processedTraceabilityData.Add("BladderEOLverification", byteRange)
        # BladderEmptyvalue
        byteRange = rawCanDataTraceDataHex[46:48]
        processedTraceabilityData.Add("BladderEmptyvalue", byteRange)
        # BladderLoadedvalue
        byteRange = rawCanDataTraceDataHex[48:50]
        processedTraceabilityData.Add("BladderLoadedvalue", byteRange)
        # EOLChecksum1
        byteRange = rawCanDataTraceDataHex[50:52]
        processedTraceabilityData.Add("EOLChecksum1", byteRange)
        # EOLChecksum2
        byteRange = rawCanDataTraceDataHex[52:54]
        processedTraceabilityData.Add("EOLChecksum2", byteRange)

        # DelphiBladderAssemblyPartNumber0(Byte0)
        byteRange = rawCanDataTraceDataHex[54:56]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber0",  Convert.ToChar(Convert.ToInt32(byteRange, 16))) 
        # DelphiBladderAssemblyPartNumber1(Byte1)
        byteRange = rawCanDataTraceDataHex[56:58]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # DelphiBladderAssemblyPartNumber2(Byte2)
        byteRange = rawCanDataTraceDataHex[58:60]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber2",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # DelphiBladderAssemblyPartNumber3(Byte3)
        byteRange = rawCanDataTraceDataHex[60:62]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber3",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # DelphiBladderAssemblyPartNumber4(Byte4)
        byteRange = rawCanDataTraceDataHex[62:64]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber4",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # DelphiBladderAssemblyPartNumber5(Byte5)
        byteRange = rawCanDataTraceDataHex[64:66]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber5",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # DelphiBladderAssemblyPartNumber6(Byte6)
        byteRange = rawCanDataTraceDataHex[66:68]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber6",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # DelphiBladderAssemblyPartNumber7(Byte7)
        byteRange = rawCanDataTraceDataHex[66:68]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber7",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # DelphiBladderAssemblyPartNumberSuffix0(Byte0)
        byteRange = rawCanDataTraceDataHex[68:70]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumberSuffix0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # DelphiBladderAssemblyPartNumberSuffix1(Byte1)
        byteRange = rawCanDataTraceDataHex[70:72]
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumberSuffix1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # ManufacturingSiteCode
        byteRange = rawCanDataTraceDataHex[72:74]
        processedTraceabilityData.Add("ManufacturingSiteCode",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # ManufacturingYear0(Byte0)
        byteRange = rawCanDataTraceDataHex[74:76]
        processedTraceabilityData.Add("ManufacturingYear0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # ManufacturingYear1(Byte1)
        byteRange = rawCanDataTraceDataHex[76:78]
        processedTraceabilityData.Add("ManufacturingYear1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # JulianDate0(Byte0)
        byteRange = rawCanDataTraceDataHex[78:80]
        processedTraceabilityData.Add("JulianDate0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # JulianDate1(Byte1)
        byteRange = rawCanDataTraceDataHex[80:82]
        processedTraceabilityData.Add("JulianDate1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # JulianDate2(Byte2)
        byteRange = rawCanDataTraceDataHex[82:84]
        processedTraceabilityData.Add("JulianDate2",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # ModelCode0(Byte0)
        byteRange = rawCanDataTraceDataHex[82:84]
        processedTraceabilityData.Add("ModelCode0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # ModelCode1(Byte1)
        byteRange = rawCanDataTraceDataHex[84:86]
        processedTraceabilityData.Add("ModelCode1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # SequenceNumber0(Byte0)
        byteRange = rawCanDataTraceDataHex[86:88]
        processedTraceabilityData.Add("SequenceNumber0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # SequenceNumber1(Byte1)
        byteRange = rawCanDataTraceDataHex[88:90]
        processedTraceabilityData.Add("SequenceNumber1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # SequenceNumber2(Byte2)
        byteRange = rawCanDataTraceDataHex[90:92]
        processedTraceabilityData.Add("SequenceNumber2",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # SequenceNumber3(Byte3)
        byteRange = rawCanDataTraceDataHex[92:94]
        processedTraceabilityData.Add("SequenceNumber3",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # SequenceNumber4(Byte4)
        byteRange = rawCanDataTraceDataHex[94:96]
        processedTraceabilityData.Add("SequenceNumber4",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber0(Byte0)
        byteRange = rawCanDataTraceDataHex[94:96]
        processedTraceabilityData.Add("OEMAssemblyPartNumber0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber1(Byte1)
        byteRange = rawCanDataTraceDataHex[96:98]
        processedTraceabilityData.Add("OEMAssemblyPartNumber1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber2(Byte2)
        byteRange = rawCanDataTraceDataHex[98:100]
        processedTraceabilityData.Add("OEMAssemblyPartNumber2",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber3(Byte3)
        byteRange = rawCanDataTraceDataHex[100:102]
        processedTraceabilityData.Add("OEMAssemblyPartNumber3",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber4(Byte4)
        byteRange = rawCanDataTraceDataHex[102:104]
        processedTraceabilityData.Add("OEMAssemblyPartNumber4",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber5(Byte5)
        byteRange = rawCanDataTraceDataHex[104:106]
        processedTraceabilityData.Add("OEMAssemblyPartNumber5",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber6(Byte6)
        byteRange = rawCanDataTraceDataHex[106:108]
        processedTraceabilityData.Add("OEMAssemblyPartNumber6",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber7(Byte7)
        byteRange = rawCanDataTraceDataHex[108:110]
        processedTraceabilityData.Add("OEMAssemblyPartNumber7",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber8(Byte8)
        byteRange = rawCanDataTraceDataHex[110:112]
        processedTraceabilityData.Add("OEMAssemblyPartNumber8",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber9(Byte9)
        byteRange = rawCanDataTraceDataHex[112:114]
        processedTraceabilityData.Add("OEMAssemblyPartNumber9",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber10(Byte10)
        byteRange = rawCanDataTraceDataHex[114:116]
        processedTraceabilityData.Add("OEMAssemblyPartNumber10",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber11(Byte11)
        byteRange = rawCanDataTraceDataHex[116:118]
        processedTraceabilityData.Add("OEMAssemblyPartNumber11",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber12(Byte12)
        byteRange = rawCanDataTraceDataHex[118:120]
        processedTraceabilityData.Add("OEMAssemblyPartNumber12",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber13(Byte13)
        byteRange = rawCanDataTraceDataHex[120:122]
        processedTraceabilityData.Add("OEMAssemblyPartNumber13",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber14(Byte14)
        byteRange = rawCanDataTraceDataHex[122:124]
        processedTraceabilityData.Add("OEMAssemblyPartNumber14",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber15(Byte15)
        byteRange = rawCanDataTraceDataHex[124:126]
        processedTraceabilityData.Add("OEMAssemblyPartNumber15",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber16(Byte16)
        byteRange = rawCanDataTraceDataHex[126:128]
        processedTraceabilityData.Add("OEMAssemblyPartNumber16",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber17(Byte17)
        byteRange = rawCanDataTraceDataHex[128:130]
        processedTraceabilityData.Add("OEMAssemblyPartNumber17",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber18(Byte18)
        byteRange = rawCanDataTraceDataHex[130:132]
        processedTraceabilityData.Add("OEMAssemblyPartNumber18",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMAssemblyPartNumber19(Byte19)
        byteRange = rawCanDataTraceDataHex[132:134]
        processedTraceabilityData.Add("OEMAssemblyPartNumber19",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved0(Unused)
        byteRange = rawCanDataTraceDataHex[134:136]
        processedTraceabilityData.Add("OEMReserved0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved1(Unused)
        byteRange = rawCanDataTraceDataHex[136:138]
        processedTraceabilityData.Add("OEMReserved1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved2(Unused)
        byteRange = rawCanDataTraceDataHex[138:140]
        processedTraceabilityData.Add("OEMReserved2",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved3(Unused)
        byteRange = rawCanDataTraceDataHex[140:142]
        processedTraceabilityData.Add("OEMReserved3",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved4(Unused)
        byteRange = rawCanDataTraceDataHex[142:144]
        processedTraceabilityData.Add("OEMReserved4",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved5(Unused)
        byteRange = rawCanDataTraceDataHex[144:146]
        processedTraceabilityData.Add("OEMReserved5",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved6(Unused)
        byteRange = rawCanDataTraceDataHex[146:148]
        processedTraceabilityData.Add("OEMReserved6",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved7(Unused)
        byteRange = rawCanDataTraceDataHex[148:150]
        processedTraceabilityData.Add("OEMReserved7",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved8(Unused)
        byteRange = rawCanDataTraceDataHex[152:154]
        processedTraceabilityData.Add("OEMReserved8",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved9(Unused)
        byteRange = rawCanDataTraceDataHex[154:156]
        processedTraceabilityData.Add("OEMReserved9",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved10(Unused)
        byteRange = rawCanDataTraceDataHex[156:158]
        processedTraceabilityData.Add("OEMReserved10",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved11(Unused)
        byteRange = rawCanDataTraceDataHex[158:160]
        processedTraceabilityData.Add("OEMReserved11",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved12(Unused)
        byteRange = rawCanDataTraceDataHex[162:164]
        processedTraceabilityData.Add("OEMReserved12",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved13(Unused)
        byteRange = rawCanDataTraceDataHex[164:166]
        processedTraceabilityData.Add("OEMReserved13",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved14(Unused)
        byteRange = rawCanDataTraceDataHex[168:170]
        processedTraceabilityData.Add("OEMReserved14",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved15(Unused)
        byteRange = rawCanDataTraceDataHex[172:174]
        processedTraceabilityData.Add("OEMReserved15",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        # OEMReserved16(Unused)
        byteRange = rawCanDataTraceDataHex[174:176]
        processedTraceabilityData.Add("OEMReserved16",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        #

        # EmptyThreshold = processedTraceabilityData["EmptyThreshold"]
        # AllowThreshold = processedTraceabilityData["AllowThreshold"]
        # # AdultAllowThreshold = processedTraceabilityData["AdultAllowThreshold"]

        # Seat_Plant_EOL_Verification = int(processedTraceabilityData["Seat_Plant_EOL_Verification"], 16)
        # Vehicle_EOL_Cal_Status = processedTraceabilityData["Vehicle_EOL_Cal_Status"]

        # EOL_ChecksumMSB = processedTraceabilityData["EOL_ChecksumMSB"]
        # EOL_ChecksumLSB = processedTraceabilityData["EOL_ChecksumLSB"]

        # Calculated_Failed_ValueByte1 = processedTraceabilityData["Calculated_Failed_ValueByte1"]
        # Calculated_Failed_ValueByte2 = processedTraceabilityData["Calculated_Failed_ValueByte2"]

        # ECU_Fault_CodeByte1 = processedTraceabilityData["ECU_Fault_CodeByte1"]
        # ECU_Fault_CodeByte2 = processedTraceabilityData["ECU_Fault_CodeByte2"]
        # ECU_Fault_CodeByte3 = processedTraceabilityData["ECU_Fault_CodeByte3"]
        # ECU_Fault_CodeByte4 = processedTraceabilityData["ECU_Fault_CodeByte4"]
        # ECU_Fault_CodeByte5 = processedTraceabilityData["ECU_Fault_CodeByte5"]
        # ECU_Fault_CodeByte6 = processedTraceabilityData["ECU_Fault_CodeByte6"]

        # Threshold1Pressure = processedTraceabilityData["Threshold1Pressure"]
        # Threshold2Pressure = processedTraceabilityData["Threshold2Pressure"]
        # EmptyPressure = processedTraceabilityData["EmptyPressure"]

        # Config_Id = processedTraceabilityData["Config_Id"]
        # HCSScaleFactor = processedTraceabilityData["HCSScaleFactor"]
        # R_AVG_Temperature = processedTraceabilityData["R_AVG_Temperature"]
        # # TempCounts = processedTraceabilityData["TempCounts"]
        # BladderEOLverification = int( processedTraceabilityData["BladderEOLverification"], 16)
        # BladderEmptyvalue = processedTraceabilityData["BladderEmptyvalue"]
        # BladderLoadedvalue = processedTraceabilityData["BladderLoadedvalue"]
        
        # EOLChecksum1 = processedTraceabilityData["EOLChecksum1"]
        # EOLChecksum2 = processedTraceabilityData["EOLChecksum2"]

        # DelphiBladderAssemblyPartNumber0 = processedTraceabilityData["DelphiBladderAssemblyPartNumber0"]
        # DelphiBladderAssemblyPartNumber1 = processedTraceabilityData["DelphiBladderAssemblyPartNumber1"]
        # DelphiBladderAssemblyPartNumber2 = processedTraceabilityData["DelphiBladderAssemblyPartNumber2"]
        # DelphiBladderAssemblyPartNumber3 = processedTraceabilityData["DelphiBladderAssemblyPartNumber3"]
        # DelphiBladderAssemblyPartNumber4 = processedTraceabilityData["DelphiBladderAssemblyPartNumber4"]
        # DelphiBladderAssemblyPartNumber5 = processedTraceabilityData["DelphiBladderAssemblyPartNumber5"]
        # DelphiBladderAssemblyPartNumber6 = processedTraceabilityData["DelphiBladderAssemblyPartNumber6"]
        # DelphiBladderAssemblyPartNumber7 = processedTraceabilityData["DelphiBladderAssemblyPartNumber7"]

        # DelphiBladderAssemblyPartNumberSuffix0 = processedTraceabilityData["DelphiBladderAssemblyPartNumberSuffix0"]
        # DelphiBladderAssemblyPartNumberSuffix1 = processedTraceabilityData["DelphiBladderAssemblyPartNumberSuffix1"]

        # ManufacturingSiteCode = processedTraceabilityData["ManufacturingSiteCode"]
        
        # ManufacturingYear0 = processedTraceabilityData["ManufacturingYear0"]
        # ManufacturingYear1 = processedTraceabilityData["ManufacturingYear1"]

        # JulianDate0 = processedTraceabilityData["JulianDate0"]
        # JulianDate1 = processedTraceabilityData["JulianDate1"]
        # JulianDate2 = processedTraceabilityData["JulianDate2"]

        # ModelCode0 = processedTraceabilityData["ModelCode0"]
        # ModelCode1 = processedTraceabilityData["ModelCode1"]

        # SequenceNumber0 = processedTraceabilityData["SequenceNumber0"]
        # SequenceNumber0 = processedTraceabilityData["SequenceNumber1"]
        # SequenceNumber0 = processedTraceabilityData["SequenceNumber2"]
        # SequenceNumber0 = processedTraceabilityData["SequenceNumber3"]
        # SequenceNumber0 = processedTraceabilityData["SequenceNumber4"]

        # OEMAssemblyPartNumber0 = processedTraceabilityData["OEMAssemblyPartNumber0"]
        # OEMAssemblyPartNumber1 = processedTraceabilityData["OEMAssemblyPartNumber1"]
        # OEMAssemblyPartNumber2 = processedTraceabilityData["OEMAssemblyPartNumber2"]
        # OEMAssemblyPartNumber3 = processedTraceabilityData["OEMAssemblyPartNumber3"]
        # OEMAssemblyPartNumber4 = processedTraceabilityData["OEMAssemblyPartNumber4"]
        # OEMAssemblyPartNumber5 = processedTraceabilityData["OEMAssemblyPartNumber5"]
        # OEMAssemblyPartNumber6 = processedTraceabilityData["OEMAssemblyPartNumber6"]
        # OEMAssemblyPartNumber7 = processedTraceabilityData["OEMAssemblyPartNumber7"]
        # OEMAssemblyPartNumber8 = processedTraceabilityData["OEMAssemblyPartNumber8"]
        # OEMAssemblyPartNumber9 = processedTraceabilityData["OEMAssemblyPartNumber9"]
        # OEMAssemblyPartNumber10 = processedTraceabilityData["OEMAssemblyPartNumber10"]
        # OEMAssemblyPartNumber11 = processedTraceabilityData["OEMAssemblyPartNumber11"]
        # OEMAssemblyPartNumber12 = processedTraceabilityData["OEMAssemblyPartNumber12"]
        # OEMAssemblyPartNumber13 = processedTraceabilityData["OEMAssemblyPartNumber13"]
        # OEMAssemblyPartNumber14 = processedTraceabilityData["OEMAssemblyPartNumber14"]
        # OEMAssemblyPartNumber15 = processedTraceabilityData["OEMAssemblyPartNumber15"]
        # OEMAssemblyPartNumber16 = processedTraceabilityData["OEMAssemblyPartNumber16"]
        # OEMAssemblyPartNumber17 = processedTraceabilityData["OEMAssemblyPartNumber17"]
        # OEMAssemblyPartNumber18 = processedTraceabilityData["OEMAssemblyPartNumber18"]
        # OEMAssemblyPartNumber19 = processedTraceabilityData["OEMAssemblyPartNumber19"]

        # OEMReserved0 = processedTraceabilityData["OEMReserved0"]
        # OEMReserved1 = processedTraceabilityData["OEMReserved1"]
        # OEMReserved2 = processedTraceabilityData["OEMReserved2"]
        # OEMReserved3 = processedTraceabilityData["OEMReserved3"]
        # OEMReserved4 = processedTraceabilityData["OEMReserved4"]
        # OEMReserved5 = processedTraceabilityData["OEMReserved5"]
        # OEMReserved6 = processedTraceabilityData["OEMReserved6"]
        # OEMReserved7 = processedTraceabilityData["OEMReserved7"]
        # OEMReserved8 = processedTraceabilityData["OEMReserved8"]
        # OEMReserved9 = processedTraceabilityData["OEMReserved9"]
        # OEMReserved10 = processedTraceabilityData["OEMReserved10"]
        # OEMReserved11 = processedTraceabilityData["OEMReserved11"]
        # OEMReserved12 = processedTraceabilityData["OEMReserved12"]
        # OEMReserved13 = processedTraceabilityData["OEMReserved13"]
        # OEMReserved14 = processedTraceabilityData["OEMReserved14"]
        # OEMReserved15 = processedTraceabilityData["OEMReserved15"]
        # OEMReserved16 = processedTraceabilityData["OEMReserved16"]

        # if EmptyThreshold == 0:
        #     traceFaultText = "Failed to verify EmptyThreshold value"
        #     isSuccess = False
        # elif AllowThreshold == 0:
        #     traceFaultText = "Failed to verify AllowThreshold value"
        #     isSuccess = False
        # elif Seat_Plant_EOL_Verification != 128:
        #     traceFaultText = "Failed to verify Seat Plant EOl value"
        #     isSuccess = False
        # elif Vehicle_EOL_Cal_Status == 0:
        #     traceFaultText = "Failed to verify Vehicle_EOL_Cal_Status value"
        #     isSuccess = False
        # elif Threshold1Pressure == 0: 
        #     traceFaultText = "Threshold 1 Pressure value failed to be verified"
        #     isSuccess = False
        # elif Threshold2Pressure == 0: 
        #     traceFaultText = "Threshold 2 Pressure value failed to be verified"
        # elif EmptyPressure == 0: 
        #     traceFaultText = "Empty Pressure value failed to be verified"
        #     isSuccess = False
        # ##Current issue verifying this SDPS value     
        # # elif BladderEOLverification != 128:
        # #     traceFaultText = "Failed to verify BladderEOL"
        # #     isSuccess = False
        # elif BladderEmptyvalue == 0:
        #     traceFaultText = "Failed to verify Bladder Empty value"
        #     isSuccess = False
        # elif BladderLoadedvalue == 0:
        #     traceFaultText = "Failed to verify Bladder Loaded value"
        #     isSuccess = False
        # elif Config_Id == 0:
        #     traceFaultText = "Failed to read Config Id"
        #     isSuccess = False
        # elif HCSScaleFactor== 0:
        #     traceFaultText = "Failed to read HCS Scale Factor"
        #     isSuccess = False
        # elif HCSScaleFactor== 0:
        #     traceFaultText = "Failed to read HCS Scale Factor"
        #     isSuccess = False
        # elif R_AVG_Temperature == 0:
        #     traceFaultText = "Failed to read R Average Temperature"
        #     isSuccess = False

        TPassLogger.Info("Traceability Python Script:  Processed Traceability Data = {0}", str(processedTraceabilityData))

    else:
        TPassLogger.Info("Failed to Process Traceability Data")
        isSuccess = False

except Exception as inst:
    TPassLogger.Warn("Traceability Python Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Traceability Python Script:  Invalid raw hex string")
    isSuccess = False
    
TPassLogger.Info("Traceability Python Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 02242023
#   Version: 1.0
#   Change: Initial Version
############################################################


