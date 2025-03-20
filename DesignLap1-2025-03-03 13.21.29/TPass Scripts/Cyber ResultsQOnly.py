#Main Button Triggered Script
#This Script can run any python logic and can also run a TPass Test Application
#TPass Objects Passed In/Returned
#   in  - object MainTPassScripting - Exposed all methods and properties for the scripts to use
#   in  - Method "TPassLogger" - This is the logging method to log to the main TPass log file
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#


import clr
clr.AddReferenceToFileAndPath('.\\IronPython.SQLite.dll')
import sys
from System import DateTime
version = "3.0"
production = False
from _sqlite3 import *

TPassLogger.Debug("Main Button Script Begin")

try:
        TPassLogger.Info("Main Button Script: Run a Quick Test Application with default options only and don't process results")
       
        # If required to parse the StartCycleInputData differently based on what input type triggered the script to run (Scan, Manual Entry, File Drop...)
        if str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Scan):
            TPassLogger.Debug("StartTestCycle - Trigger Type is Scan")
        elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.ManualEntry):
            TPassLogger.Debug("StartTestCycle - Trigger Type is ManualEntry")
        elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.FileDrop):
            TPassLogger.Debug("StartTestCycle - Trigger Type is FileDrop")
        elif str(MainTPassScripting.StartTestCycleTriggerType) == str(MainTPassScripting.TriggerType.Udp):
            TPassLogger.Debug("StartTestCycle - Trigger Type is UDP")
                    

        isSuccess = True
        # write headers
        f= open ("C:\\TPass\\Logs\\Test Result Detail.txt", "w")
        f.write ("PrimaryId ,GroupName ,TestResults ,DurationMsecTestCycle  ,DurationMsecTestGroup  ,BeginDateTimeTestCycle  ,BeginDateTimeTestGroup \n")
        f.close()
        TestResultfile= open ("C:\\TPass\\Logs\\Test Result.txt", "w")
        TestResultfile.write ("PrimaryId ,GroupName ,TestResults ,DurationMsecTestCycle  ,BeginDateTimeTestCycle   \n")
        TestResultfile.close()
 
        TestStepResultfile= open ("C:\\TPass\\Logs\\TestStep Result.txt", "w")
        TestStepResultfile.write ("PrimaryId ,TestStepName ,TestResults ,DurationMsecTestCycle  ,BeginDateTimeTestCycle   \n")
        TestStepResultfile.close()

        StartDateTime = "2022-06-30 11:38:00" 
#        db = Connection("C:\\TPass\\bin\\DataBase\\ManBTpiNoSoftware.Tpass.Db")
        db = Connection("C:\\Users\\rmueller\\Desktop\\Cyber Testing\\GM 24 TPI Lab new firmware\\Tpi.Tpass.Db")
        #db = Connection("C:\\Users\\rmueller\\Desktop\\Cyber Testing\\LabTool\\after removing invalidaterequery\\Tpi.Tpass.Db")
        #Query execution - CAN
        queryFailedTestSteps = """SELECT p.PrimaryId,
       s.Description AS StepName,
       r.Description AS TestResult,
       t.DurationMsec AS DurationMsecTestCycle, s.DurationMsec AS DurationMsecTestStep
       ,t.BeginDateTime, s.BeginDateTime
       FROM Product p
       LEFT JOIN
       TestCycle t ON p.Id = t.ProductId
       JOIN
       TestApplication a ON a.Id = t.TestApplicationId
       LEFT JOIN
       TestStep s ON t.Id = s.TestCycleId
       JOIN
       TestResult r ON r.Id = s.TestResultId
       WHERE NOT r.Description = 'OptionCodeNotTested' and 
       t.BeginDateTime >='""" + str(StartDateTime) + """' order by s.BeginDateTime"""
       
       
        queryString = """SELECT p.PrimaryId,
       g.Name AS GroupName,
       r.Description AS TestResult,
       t.DurationMsec AS DurationMsecTestCycle, g.DurationMsec AS DurationMsecTestGroup
       ,t.BeginDateTime, g.BeginDateTime
       FROM Product p
       LEFT JOIN
       TestCycle t ON p.Id = t.ProductId
       JOIN
       TestApplication a ON a.Id = t.TestApplicationId
       LEFT JOIN
       TestGroup g ON t.Id = g.TestCycleId
       JOIN
       TestResult r ON r.Id = g.TestResultId
       WHERE NOT r.Description = 'OptionCodeNotTested' and 
       t.BeginDateTime >='""" + str(StartDateTime) + """' order by g.BeginDateTime"""
        queryGroup = """SELECT p.PrimaryId,
       g.Name AS GroupName,
       r.Description AS TestResult,
       t.DurationMsec AS DurationMsecTestCycle
       ,t.BeginDateTime
       FROM Product p
       LEFT JOIN
       TestCycle t ON p.Id = t.ProductId
       JOIN
       TestApplication a ON a.Id = t.TestApplicationId
       LEFT JOIN
       TestGroup g ON t.Id = g.TestCycleId
       JOIN
       TestResult r ON r.Id = g.TestResultId
       WHERE NOT r.Description = 'OptionCodeNotTested' and g.Name = 'CAN' and 
       t.BeginDateTime >='""" + str(StartDateTime) + """' order by g.BeginDateTime"""
        cursorTestStep = db.execute(queryFailedTestSteps)
        cursor = db.execute(queryString)
        cursorCAN = db.execute(queryGroup)
        recordsTestStep = cursorTestStep.fetchall() 
        records = cursor.fetchall() 
        recordCAN = cursorCAN.fetchall()
        #returns results to file on desktop
        f= open ("C:\\TPass\\Logs\\TestStep Result.txt", "a")
        for row in recordsTestStep:
           items = TPassLogger.Info("Results: {0}",row)
           f.write(str(row)+"\n")
        f.close()
        
        f= open ("C:\\TPass\\Logs\\Test Result Detail.txt", "a")
        for row in records:
           items = TPassLogger.Info("Results: {0}",row)
           f.write(str(row)+"\n")
        f.close()
#                 db.close()
        TestResultfile= open ("C:\\TPass\\Logs\\Test Result.txt", "a")
        for row in recordCAN:
            item = TPassLogger.Info("Results: {0}",row)
            TestResultfile.write(str(row)+"\n")
#             db.close()
        TestResultfile.close()
    #Modbus 1
    
        queryString = """SELECT p.PrimaryId,
       g.Name AS GroupName,
       r.Description AS TestResult,
       t.DurationMsec AS DurationMsecTestCycle, g.DurationMsec AS DurationMsecTestGroup
       ,t.BeginDateTime, g.BeginDateTime
       FROM Product p
       LEFT JOIN
       TestCycle t ON p.Id = t.ProductId
       JOIN
       TestApplication a ON a.Id = t.TestApplicationId
       LEFT JOIN
       TestGroup g ON t.Id = g.TestCycleId
       JOIN
       TestResult r ON r.Id = g.TestResultId
       WHERE NOT r.Description = 'OptionCodeNotTested' and 
       t.BeginDateTime >='""" + str(StartDateTime) + """' order by g.BeginDateTime"""
        queryGroup = """SELECT p.PrimaryId,
       g.Name AS GroupName,
       r.Description AS TestResult,
       t.DurationMsec AS DurationMsecTestCycle
       ,t.BeginDateTime
       FROM Product p
       LEFT JOIN
       TestCycle t ON p.Id = t.ProductId
       JOIN
       TestApplication a ON a.Id = t.TestApplicationId
       LEFT JOIN
       TestGroup g ON t.Id = g.TestCycleId
       JOIN
       TestResult r ON r.Id = g.TestResultId
       WHERE NOT r.Description = 'OptionCodeNotTested' and g.Name = 'Modbus 1' and 
       t.BeginDateTime >='""" + str(StartDateTime) + """' order by g.BeginDateTime"""
        cursor = db.execute(queryString)
        cursorCAN = db.execute(queryGroup)
        records = cursor.fetchall() 
        recordCAN = cursorCAN.fetchall()
        #returns results to file on desktop
        f= open ("C:\\TPass\\Logs\\Test Result Detail.txt", "a")
        for row in records:
           items = TPassLogger.Info("Results: {0}",row)
           f.write(str(row)+"\n")
        f.close()
#                 db.close()
        TestResultfile= open ("C:\\TPass\\Logs\\Test Result.txt", "a")
        for row in recordCAN:
            item = TPassLogger.Info("Results: {0}",row)
            TestResultfile.write(str(row)+"\n")
#             db.close()
        TestResultfile.close()
        
    #Board 1 Voltage
    
        queryString = """SELECT p.PrimaryId,
       g.Name AS GroupName,
       r.Description AS TestResult,
       t.DurationMsec AS DurationMsecTestCycle, g.DurationMsec AS DurationMsecTestGroup
       ,t.BeginDateTime, g.BeginDateTime
       FROM Product p
       LEFT JOIN
       TestCycle t ON p.Id = t.ProductId
       JOIN
       TestApplication a ON a.Id = t.TestApplicationId
       LEFT JOIN
       TestGroup g ON t.Id = g.TestCycleId
       JOIN
       TestResult r ON r.Id = g.TestResultId
       WHERE NOT r.Description = 'OptionCodeNotTested' and 
       t.BeginDateTime >='""" + str(StartDateTime) + """' order by g.BeginDateTime"""
        queryGroup = """SELECT p.PrimaryId,
       g.Name AS GroupName,
       r.Description AS TestResult,
       t.DurationMsec AS DurationMsecTestCycle
       ,t.BeginDateTime
       FROM Product p
       LEFT JOIN
       TestCycle t ON p.Id = t.ProductId
       JOIN
       TestApplication a ON a.Id = t.TestApplicationId
       LEFT JOIN
       TestGroup g ON t.Id = g.TestCycleId
       JOIN
       TestResult r ON r.Id = g.TestResultId
       WHERE NOT r.Description = 'OptionCodeNotTested' and g.Name = 'Board 1 Voltage' and 
       t.BeginDateTime >='""" + str(StartDateTime) + """' order by g.BeginDateTime"""
        cursor = db.execute(queryString)
        cursorCAN = db.execute(queryGroup)
        records = cursor.fetchall() 
        recordCAN = cursorCAN.fetchall()
        #returns results to file on desktop
        f= open ("C:\\TPass\\Logs\\Test Result Detail.txt", "a")
        for row in records:
           items = TPassLogger.Info("Results: {0}",row)
           f.write(str(row)+"\n")
        f.close()
#                 db.close()
        TestResultfile= open ("C:\\TPass\\Logs\\Test Result.txt", "a")
        for row in recordCAN:
            item = TPassLogger.Info("Results: {0}",row)
            TestResultfile.write(str(row)+"\n")
#             db.close()
        TestResultfile.close()
        db.close()
        
except Exception as inst:
    TPassLogger.Warn("Main Button Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Main Button Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Main Button Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#   Date: 01172021
#   Version: 1.0
#   ChangeBy: RMM
#   Change: Initial Version
############################################################
