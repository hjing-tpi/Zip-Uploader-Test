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

import clr
from System import String
from System import Convert
from System.Collections.Generic import Dictionary
version = "0.1"
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
    processedTraceabilityData.Add("EmptyThreshold",  rawCanDataTraceDataHex[0:0+2])
    processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber",  Convert.ToChar(Convert.ToInt32(rawCanDataTraceDataHex[28:28+2], 16)))
# AllowThreshold
# AdultAllowThreshold
# Seat_Plant_EOL_Verification
# Vehicle_EOL_Cal_Status
# EOL_ChecksumMSB
# EOL_ChecksumLSB
# FTS_Process_Failure_Code
# Calculated_Failed_ValueByte1
# Calculated_Failed_ValueByte2
# ECU_Fault_CodeByte1
# ECU_Fault_CodeByte2
# ECU_Fault_CodeByte3
# ECU_Fault_CodeByte4
# ECU_Fault_CodeByte5
# ECU_Fault_CodeByte6
# Threshold1Pressure
# Threshold2Pressure
# EmptyPressure
# Config_Id
# HCSScaleFactor
# R_AVG_Temperature
# TempCounts
# BladderEOLverification
# BladderEmptyvalue
# BladderLoadedvalue
# EOLChecksum
# EOLChecksum
# DelphiBladderAssemblyPartNumber(Byte0)
# DelphiBladderAssemblyPartNumber(Byte1)
# DelphiBladderAssemblyPartNumber(Byte2)
# DelphiBladderAssemblyPartNumber(Byte3)
# DelphiBladderAssemblyPartNumber(Byte4)
# DelphiBladderAssemblyPartNumber(Byte5)
# DelphiBladderAssemblyPartNumber(Byte6)
# DelphiBladderAssemblyPartNumber(Byte7)
# DelphiBladderAssemblyPartNumberSuffix(Byte0)
# DelphiBladderAssemblyPartNumberSuffix(Byte1)
# ManufacturingSiteCode
# ManufacturingYear(Byte0)
# ManufacturingYear(Byte1)
# JulianDate(Byte0)
# JulianDate(Byte1)
# JulianDate(Byte2)
# ModelCode(Byte0)
# ModelCode(Byte1)
# SequenceNumber(Byte0)
# SequenceNumber(Byte1)
# SequenceNumber(Byte2)
# SequenceNumber(Byte3)
# SequenceNumber(Byte4)
# OEMAssemblyPartNumber(Byte0)
# OEMAssemblyPartNumber(Byte1)
# OEMAssemblyPartNumber(Byte2)
# OEMAssemblyPartNumber(Byte3)
# OEMAssemblyPartNumber(Byte4)
# OEMAssemblyPartNumber(Byte5)
# OEMAssemblyPartNumber(Byte6)
# OEMAssemblyPartNumber(Byte7)
# OEMAssemblyPartNumber(Byte8)
# OEMAssemblyPartNumber(Byte9)
# OEMAssemblyPartNumber(Byte10)
# OEMAssemblyPartNumber(Byte11)
# OEMAssemblyPartNumber(Byte12)
# OEMAssemblyPartNumber(Byte13)
# OEMAssemblyPartNumber(Byte14)
# OEMAssemblyPartNumber(Byte15)
# OEMAssemblyPartNumber(Byte16)
# OEMAssemblyPartNumber(Byte17)
# OEMAssemblyPartNumber(Byte18)
# OEMAssemblyPartNumber(Byte19)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
# OEMReserved(Unused)
#
    TPassLogger.Info("Traceability Python Script:  Processed Traceability Data = {0}", str(processedTraceabilityData))
except Exception as inst:
    TPassLogger.Warn("Traceability Python Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Traceability Python Script:  Invalid raw hex string")
    isSuccess = False
    
TPassLogger.Info("Traceability Python Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 02242023
#   Version: 0.1
#   Change: Initial Version
############################################################


