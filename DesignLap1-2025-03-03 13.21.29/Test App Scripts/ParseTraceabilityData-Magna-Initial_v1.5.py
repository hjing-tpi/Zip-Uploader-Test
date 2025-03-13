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

rawCanDataResponse = "105AFA714845FF800056E10000000000000000008C8C488498177A80397E560C32383735323139332020523232313636202030303132334E4C3742313442343232424220202020202020202020202020202020202020202020202020"
seatType = '22_54_30W_BL_LEATHER_MCS'

traceFaultText = ""

import clr
import System.IO
from System import String
from System import Convert
from System.Collections.Generic import Dictionary
version = "1.0"
production = False

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
    
    ## FilePath which contains all the SDPS Traceability results
    fileName = "C:\TPass\Ford_Can_Messages\Ford_SDPS"
    filePathTemp = fileName + ".txt"

    f = open(filePathTemp, 'r')
    lines = f.readlines()

    digitCount = 0
    if rawCanDataTraceLength >= 168:
        for line in lines:

            ## Splits the comma seperate text file that holds all the Ford SDPS values 
            words = line.split(',')

            ##byteRange is renamed to digitRange 
            digitRange = rawCanDataTraceDataHex[digitCount : digitCount + 2]

            ## If it is a Hex type
            if words[1].strip() == "Hex":
                processedTraceabilityData.Add(words[0].strip(), digitRange)
            elif words[1].strip() == "ASCII":
                # If it is a ASCII type 
                processedTraceabilityData.Add(words[0].strip(), Convert.ToChar(Convert.ToInt32(digitRange, 16)))
            else: 
                TPassLogger.Warn("Failure to read SDPS Type:{0}", words[0].strip)
                break

            digitCount = digitCount + 2

        # EmptyThreshold = processedTraceabilityData["EmptyThreshold"]
        # AllowThreshold = processedTraceabilityData["AllowThreshold"]

        # Seat_Plant_EOL_Verification = int(processedTraceabilityData["Seat_Plant_EOL_Verification"], 16)
        # Vehicle_EOL_Cal_Status = processedTraceabilityData["Vehicle_EOL_Cal_Status"]

        # Threshold1Pressure = processedTraceabilityData["Threshold1Pressure"]
        # Threshold2Pressure = processedTraceabilityData["Threshold2Pressure"]
        # EmptyPressure = processedTraceabilityData["EmptyPressure"]

        # Config_Id = processedTraceabilityData["Config_Id"]
        # HCSScaleFactor = processedTraceabilityData["HCSScaleFactor"]
        # R_AVG_Temperature = processedTraceabilityData["R_AVG_Temperature"]
        # BladderEOLverification = int( processedTraceabilityData["BladderEOLverification"], 16)
        # BladderEmptyvalue = processedTraceabilityData["BladderEmptyvalue"]
        # BladderLoadedvalue = processedTraceabilityData["BladderLoadedvalue"]

        # if EmptyThreshold == 0:
        #     traceFaultText = "Failed to verify EmptyThreshold value"
        #     isSuccess = False
        # elif AllowThreshold == 0:
        #     traceFaultText = "Failed to verify AllowThreshold value"
        #     isSuccess = False
        # elif int(Seat_Plant_EOL_Verification) != 128:
        #     traceFaultText = "Failed to verify Seat Plant EOL value"
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
        # elif BladderEOLverification != 128:
        #     traceFaultText = "Failed to verify BladderEOL"
        #     isSuccess = False
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

        ## isSuccess can become false if the Traceability data is not valid, which logs to the file 
        # if isSuccess == False:
        #     TPassLogger.Info("Failed to Process Traceability Data Due to: {0}", traceFaultText)

    ## Logs to the file if the raw CAN response data isn't the proper length 
    else:
        TPassLogger.Info("Failed to Process Traceability Data")
        isSuccess = False



    # MainTPassScripting.InterfaceUiLogger("Result", str(processedTraceabilityData), True, False)
    TPassLogger.Info("Traceability Python Script:  Processed Traceability Data = {0}", str(processedTraceabilityData))


except: 
    TPassLogger.Info("Traceability Python Script: Failed to Process Traceability Data")
    isSuccess = False


############################################################
# Change History
############################################################
#   Date: 03012023
#   Version: 1.5
#   Change: Initial Version
############################################################