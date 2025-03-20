## This implementation can query the SeatMatrix.xlsx file using an ODBC driver
## This connection driver requires a 32 bit connection string
## In order to use the given connection String the MS Access Database Engine 2010 Redistributable 
## https://www.microsoft.com/en-us/download/details.aspx?id=13255

## This script gets the Trim Parameters needed for testing.

import clr
clr.AddReference("System.Data")
from System.Data import *
from System.Data import DataSet
from System.Data.Odbc import * 

version = "1.0"
production = False

try:

    ##The Strings to perform a query on a row off the Seat.Matrix.xlsx

    filePath = "C:\\DelphiSeatMatrix\\SeatMatrix.xls"
    connectionString = "Driver={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)}; DBQ=" + filePath

    ##Modify to get specific columns using the Column Headers 
    queryString = "select * from [Sheet1$] where Trim = 'XLT Cloth'"

    ## Connects to the database and execute the query
    ## Return it as a list to the Logger on TPass 

    try: 
        excelConnection = OdbcConnection(connectionString)
        excelConnection.Open()

        objDa = OdbcDataAdapter(queryString, excelConnection)
        excelData = DataSet()
        objDa.Fill(excelData)

        data_list = []

        for row in excelData.Tables[0].Rows:
            for item in row.ItemArray:
                data_list.append(str(item))
        MainTPassScripting.InterfaceUiLogger("Magna Seat", str(data_list), True, False)

        excelConnection.Close()
        isSuccess = True


    except Exception as ex:
        MainTPassScripting.InterfaceUiLogger("Magna Seat", "Failed to Pull Row from Seat Matrix", True, False)



except Exception as inst:
    TPassLogger.Warn("Main Button Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Main Button Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Main Button Script:  Is Success = {0}", isSuccess)
