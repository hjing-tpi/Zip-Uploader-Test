#Traceability Data.  Parse raw data HEX 
#
#TPass Objects Passed In/Returned
#   in - string "rawCanDataResponse"
#   in - Function "TPassLogger"
#   in - dictionary<string,string> "PartNumbers"
#   out - string "traceFaultText"
#   out - string "rawCanDataTraceabilityHex"
#   out - dictionary<string key, string value> "processedTraceabilityData"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#


#System.Diagnostics.Debugger.Break();

#rawCanDataResponse = "105AFA7100FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF000000000000FF80397E560C32383735323139332020523232313636202030303132334E4C3742313442343232424220202020202020202020202020202020202020202020202020"
#rawCanDataResponse = "105AFA714845FF800056E10000000000000000008C8C488498177A80397E560C32383735323139332020523232313636202030303132334E4C3742313442343232424220202020202020202020202020202020202020202020202020"
#seatType = '22_54_30W_BL_LEATHER_MCS'

import clr
from System import String
from System import Convert
from System.Collections.Generic import Dictionary
traceFaultText = ""
rawCanDataTraceabilityHex = ""
version = "1.0"
production = False

# string offset starts with 0
traceDataHexByteOffset = 8
isSuccess = True
try:
    TPassLogger.Info("Traceability Python Script:  Raw Can Data Response = {0}", rawCanDataResponse)
    rawCanDataTraceabilityHex = rawCanDataResponse[traceDataHexByteOffset::]
    TPassLogger.Info("Traceability Python Script:  Raw Can Data Traceability Data Hex = {0}", rawCanDataTraceabilityHex)
    processedTraceabilityData = Dictionary[String,String]()
    processedTraceabilityData.Add("ECU","SDPS")
    delphiPNSeatTrace = ""
    
    ## Checks if rawCanDataTraceabilityHex is atleast 168 in length
    rawCanDataTraceLength = len(rawCanDataTraceabilityHex)
    if rawCanDataTraceLength >= 168:
    
        start = 0
        end = 2

        # EmptyThreshold
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("EmptyThreshold", byteRange)   
        start += 2
        end += 2
        # AllowThreshold
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("AllowThreshold", byteRange)
        start += 2
        end += 2
        # AdultAllowThreshold
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("AdultAllowThreshold", byteRange)
        start += 2
        end += 2
        # Seat_Plant_EOL_Verification
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("Seat_Plant_EOL_Verification", byteRange)
        start += 2
        end += 2
        # Vehicle_EOL_Cal_Status
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("Vehicle_EOL_Cal_Status", byteRange)
        start += 2
        end += 2
        # EOL_ChecksumMSB
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("EOL_ChecksumMSB", byteRange)
        start += 2
        end += 2
        # EOL_ChecksumLSB
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("EOL_ChecksumLSB", byteRange)
        start += 2
        end += 2
        # FTS_Process_Failure_Code
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("FTS_Process_Failure_Code", byteRange)
        start += 2
        end += 2
        # Calculated_Failed_ValueByte1
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("Calculated_Failed_ValueByte1", byteRange)
        start += 2
        end += 2
        # Calculated_Failed_ValueByte2
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("Calculated_Failed_ValueByte2", byteRange)
        start += 2
        end += 2
        # ECU_Fault_CodeByte1
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ECU_Fault_CodeByte1", byteRange)
        start += 2
        end += 2
        # ECU_Fault_CodeByte2
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ECU_Fault_CodeByte2", byteRange)
        start += 2
        end += 2
        # ECU_Fault_CodeByte3
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ECU_Fault_CodeByte3", byteRange)
        start += 2
        end += 2
        # ECU_Fault_CodeByte4
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ECU_Fault_CodeByte4", byteRange)
        start += 2
        end += 2
        # ECU_Fault_CodeByte5
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ECU_Fault_CodeByte5", byteRange)
        start += 2
        end += 2
        # ECU_Fault_CodeByte6
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ECU_Fault_CodeByte6", byteRange)
        start += 2
        end += 2
        # Threshold1Pressure
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("Threshold1Pressure", byteRange)
        start += 2
        end += 2
        # Threshold2Pressure
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("Threshold2Pressure", byteRange)
        start += 2
        end += 2
        # EmptyPressure
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("EmptyPressure", byteRange)
        start += 2
        end += 2
        # Config_Id
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("Config_Id", byteRange)
        start += 2
        end += 2
        # HCSScaleFactor
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("HCSScaleFactor", byteRange)
        start += 2
        end += 2
        # R_AVG_Temperature
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("R_AVG_Temperature", byteRange)
        start += 2
        end += 2
        # TempCounts
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("TempCounts", byteRange)
        start += 2
        end += 2
        # BladderEOLverification
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("BladderEOLverification", byteRange)
        start += 2
        end += 2
        # BladderEmptyvalue
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("BladderEmptyvalue", byteRange)
        start += 2
        end += 2
        # BladderLoadedvalue
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("BladderLoadedvalue", byteRange)
        start += 2
        end += 2
        # EOLChecksum1
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("EOLChecksum1", byteRange)
        start += 2
        end += 2
        # EOLChecksum2
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("EOLChecksum2", byteRange)
        start += 2
        end += 2

        # DelphiBladderAssemblyPartNumber0(Byte0)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber0", asciiByte) 
        start += 2
        end += 2
        # DelphiBladderAssemblyPartNumber1(Byte1)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber1", asciiByte)
        start += 2
        end += 2
        # DelphiBladderAssemblyPartNumber2(Byte2)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber2", asciiByte)
        start += 2
        end += 2
        # DelphiBladderAssemblyPartNumber3(Byte3)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber3", asciiByte)
        start += 2
        end += 2
        # DelphiBladderAssemblyPartNumber4(Byte4)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber4", asciiByte)
        start += 2
        end += 2
        # DelphiBladderAssemblyPartNumber5(Byte5)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber5", asciiByte)
        start += 2
        end += 2
        # DelphiBladderAssemblyPartNumber6(Byte6)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber6", asciiByte)
        start += 2
        end += 2
        # DelphiBladderAssemblyPartNumber7(Byte7)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumber7", asciiByte)
        start += 2
        end += 2
        # DelphiBladderAssemblyPartNumberSuffix0(Byte0)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumberSuffix0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # DelphiBladderAssemblyPartNumberSuffix1(Byte1)
        byteRange = rawCanDataTraceabilityHex[start:end]
        asciiByte = Convert.ToChar(Convert.ToInt32(byteRange, 16))
        delphiPNSeatTrace += asciiByte
        processedTraceabilityData.Add("DelphiBladderAssemblyPartNumberSuffix1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # ManufacturingSiteCode
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ManufacturingSiteCode",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # ManufacturingYear0(Byte0)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ManufacturingYear0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # ManufacturingYear1(Byte1)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ManufacturingYear1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # JulianDate0(Byte0)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("JulianDate0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # JulianDate1(Byte1)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("JulianDate1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # JulianDate2(Byte2)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("JulianDate2",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # ModelCode0(Byte0)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ModelCode0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # ModelCode1(Byte1)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("ModelCode1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # SequenceNumber0(Byte0)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("SequenceNumber0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # SequenceNumber1(Byte1)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("SequenceNumber1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # SequenceNumber2(Byte2)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("SequenceNumber2",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # SequenceNumber3(Byte3)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("SequenceNumber3",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # SequenceNumber4(Byte4)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("SequenceNumber4",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber0(Byte0)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber1(Byte1)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber2(Byte2)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber2",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber3(Byte3)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber3",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber4(Byte4)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber4",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber5(Byte5)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber5",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber6(Byte6)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber6",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber7(Byte7)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber7",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber8(Byte8)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber8",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber9(Byte9)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber9",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber10(Byte10)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber10",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber11(Byte11)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber11",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber12(Byte12)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber12",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber13(Byte13)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber13",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber14(Byte14)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber14",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber15(Byte15)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber15",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber16(Byte16)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber16",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber17(Byte17)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber17",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber18(Byte18)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber18",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMAssemblyPartNumber19(Byte19)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMAssemblyPartNumber19",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved0(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved0",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved1(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved1",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved2(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved2",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved3(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved3",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved4(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved4",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved5(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved5",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved6(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved6",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved7(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved7",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved8(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved8",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved9(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved9",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved10(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved10",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved11(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved11",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved12(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved12",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved13(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved13",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved14(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved14",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved15(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved15",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))
        start += 2
        end += 2
        # OEMReserved16(Unused)
        byteRange = rawCanDataTraceabilityHex[start:end]
        processedTraceabilityData.Add("OEMReserved16",  Convert.ToChar(Convert.ToInt32(byteRange, 16)))

        TPassLogger.Info("Traceability Python Script:  Processed Traceability Data = {0}", str(processedTraceabilityData))

        # Verify DelphiPN 
        if PartNumbers.ContainsKey("DelphiPN"):
            delphiPNSeatMatrix = PartNumbers["DelphiPN"] + PartNumbers["Suffix"]
            delphiPNSeatMatrix = delphiPNSeatMatrix.PadRight(10)
            if not delphiPNSeatTrace == delphiPNSeatMatrix:
                traceFaultText = "Delphi Bladder Assembly Part Number mismatch.  Trace=" + delphiPNSeatTrace + ", Recipe=" + delphiPNSeatMatrix
                TPassLogger.Info(traceFaultText)
                isSuccess = False
        else:
            traceFaultText = "DelphiPN not in SeatMatrix build data"
            TPassLogger.Info(traceFaultText)
            isSuccess = False
    else:
        traceFaultText = "Trace Data Length not >= to 168 from Controller"
        TPassLogger.Info(traceFaultText)
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


