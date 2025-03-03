#Retrieve Build Data for Product Id
## This connection driver requires a 32 bit connection string
## In order to use the given connection String the MS Access Database Engine 2010 Redistributable 
## https://www.microsoft.com/en-us/download/details.aspx?id=13255
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - string "RunTestCycleId" - This is the data that was passed from the Start Test Cycle script via the RunTestCycle method.
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application Detail log file
#   in  - object "SystemConfigurationValue" - This is the object to get values set in the System Configuration file
#   out - string "productBuildData" - Build data retrieved to be processed by the Option Parsing script
#   out - bool "isSuccess" - Set to True if build data retrieval was successful.  Otherwise False
#   out - bool "production"
#   out - string "version"
#

import clr
clr.AddReference("System.Data")
from System.IO import File
from System import DateTime
from System.Data import *
from System.Data import DataSet
from System.Data.Odbc import * 

version = "0.1"
production = False
productBuildData = ""
isSuccess = False


#########################################################################################################################################
# Application Engineer:  Specific constant variables to maintain
#
filePath = "C:\\DelphiSeatMatrix\\SeatMatrix.xls"
connectionString = "Driver={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)}; DBQ=" + filePath
queryString = "select * from [Sheet1$] where Trim = "
#
#########################################################################################################################################


# Main Logic
try:

    seatType = RunTestCycleId
    productBuildData = ""
    queryString = queryString + "'" + seatType + "'"
    if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ManualEntry):
        TPassLogger.Info("StartTestCycle - Trigger Type is ManualEntry no Retrieval is necessary")
        productBuildData = RunTestCycleId
    else:
        TPassLogger.Info("Option Retrieval Script:  Data is received via Barcode scan so no Retrieval is necessary")

    # Get seat information from excel matrix file
    try: 
        MainTPassScripting.InterfaceUiLogger("Magna", "Option Retrieval Script:  Get SeatMatrix data using Seat Type = " + seatType, False, False)
        #MainTPassScripting.InterfaceUiLogger("Magna", "queryString = " + queryString, True, True)
        excelConnection = OdbcConnection(connectionString)
        excelConnection.Open()

        objDa = OdbcDataAdapter(queryString, excelConnection)
        excelData = DataSet()
        objDa.Fill(excelData)

        data_list = []

        for row in excelData.Tables[0].Rows:
            for item in row.ItemArray:
                data_list.append(str(item))
                productBuildData = productBuildData + str(item) + ","
        productBuildData = productBuildData.rstrip(',')
        MainTPassScripting.InterfaceUiLogger("Magna", "Option Retrieval Script:  Data = " + str(data_list), False, False)
        
        excelConnection.Close()
        isSuccess = True


    except Exception as ex:
        MainTPassScripting.InterfaceUiLogger("Magna", "Option Retrieval Script:  Failed to Pull Row from Seat MatrixException Occurred = " + str(ex), True, True)
        isSuccess = False


except Exception as inst:
    TPassLogger.Warn("Option Retrieval Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Retrieval Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Retrieval Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 02282023
#   Version: 0.1
#   Change: Initial Version
############################################################
