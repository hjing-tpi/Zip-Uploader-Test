#Parse build data passed in and populate IDs, options and part numbers
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in  - string "RunTestCycleId" - This is the data that was passed from the Start Test Cycle script via the RunTestCycle method.
#   in  - string "BuildData" - Build data sent from the option retrieval script which was set in the productBuildData out variable
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application Detail log file
#   in  - object "SystemConfigurationValue" - This is the object to get values set in the System Configuration file
#   out - string "primaryId"
#   out - string "secondaryId"
#   out - string "tertiaryId"
#   out - string "quaternaryId"
#   out - string "quinaryId"
#   out - list<string> "OptionCodesInBuildData"
#   out - dictionary<string,string> "PartNumbers"
#   out - bool "isSuccess" - Set to True if build data parsing was successful.  Otherwise False
#   out - bool "production"
#   out - string "version"
#

from System import String
from System.Collections.Generic import Dictionary, List
from System.IO import File

production = False
version = "1.0"
isSuccess = True
recipeInfo = Dictionary[String, List[String]]()

#########################################################################################################################################
# Application Engineer:  Set Recipes that are required for Test Application 
#
# recipeFileName full path 
recipeFileName = "C:\TPass\Support Files\SeatRecipe.txt"
numberOfFieldsRequired = 8
#
#
#########################################################################################################################################

# Internal Functions
def ReadRecipeFile():
    #Read recipes from file
    global recipeInfo
    global recipeFileName
    global numberOfFieldsRequired
    try:
       recipeLines = File.ReadAllLines(recipeFileName)
       for recipeLine in recipeLines:
            recipeFields = recipeLine.split(",")
            #MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Recipe Line - " +  recipeLine , True, True)
            if len(recipeFields) >= numberOfFieldsRequired:
                try:
                    recipeData = List[String]()
                    recipeData.Clear()
                    recipeData.Add(recipeFields[1])
                    recipeData.Add(recipeFields[2])
                    recipeData.Add(recipeFields[3])
                    recipeData.Add(recipeFields[4])
                    recipeData.Add(recipeFields[5])
                    recipeData.Add(recipeFields[6])
                    recipeData.Add(recipeFields[7])
                    if not recipeInfo.ContainsKey(recipeFields[0]):
                        recipeInfo.Add(recipeFields[0], recipeData)
                    else:
                        MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Duplicate Recipe=" + recipeFields[0] + " in file - " + recipeFileName, True, True)
                        TPassLogger.Error("Option Parsing Script:  Duplicate Recipe=" + recipeFields[0] + " in file - " + recipeFileName )          

                except Exception as inst:
                   MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Error Reading Recipe File - " +  recipeFileName + "Exception Occurred = " + str(inst), True, True)
                   TPassLogger.Error("Option Parsing Script:  Error Reading Recipe File - " +  recipeFileName + "Exception Occurred = {0}", inst)            
            else:
                TPassLogger.Info("Option Parsing Script:  Invalid number of fields for Recipe.  Must be at least " + str(numberOfFieldsRequired))
                # InterfaceUiLogger(string mesSystem, string detail, bool isError = false, bool alarm = false)
                MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Invalid number of fields for Product Build Data.  Must be at least " + str(numberOfFieldsRequired) + " fields.  Recipe = " + recipeLine, True, True)
                isSuccess = False
    except Exception as inst:
       MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Error Reading Recipe File - " +  recipeFileName + "Exception Occurred = " + str(inst), True, True)
       TPassLogger.Error("Option Parsing Script:  Error Reading Recipe File - " +  recipeFileName + "Exception Occurred = {0}", inst)            
 
def AddOptionsAndPart(ktb, buckles):

    global RunTestCycleId
    #MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "ktb= " + ktb + "buckels = " + buckles, False, False)
    if buckles != "0":
        optionName = "KTB" + ktb + "S" + ktb + "B" + buckles
        partName = "KTB" + ktb + "BUCKLES"
        MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Added " + optionName, False, False)
        OptionCodesInBuildData.Add(optionName)
        MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Added Part " + partName + " = " + buckles, False, False)
        PartNumbers.Add(partName, buckles)

try:

    #Debug
    #BuildData = "??????"

    primaryId = ""
    secondaryId = ""
    tertiaryId = ""
    quaternaryId = ""
    quinaryId = ""
    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)

    primaryId = RunTestCycleId
    ReadRecipeFile()
    
    if (BuildData == ""):
        TPassLogger.Info("Option Parsing Script:  No Product Build Data")
        # InterfaceUiLogger(string mesSystem, string detail, bool isError = False, bool alarm = False)
        MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Empty build data", True, True)
        isSuccess = False
    else:
        if (MainTPassScripting.StartTestCycleTriggerType == str(MainTPassScripting.TriggerType.ManualEntry)):
            primaryId = "NO BCM ID"
        secondaryId = RunTestCycleId
        
        # for keys in recipeInfo:
            # MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Key = " + keys.Key, False, False)
            # #recipe = keys.Value
            # for values in keys.Value:
                # MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Value = " + values, False, False)
        
        if recipeInfo.ContainsKey(RunTestCycleId):
            MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Recipe " + RunTestCycleId, False, False)
            recipe = List[String]()
            recipe = recipeInfo[RunTestCycleId]
            tertiaryId = recipe[0]   #Row Type
            # MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  key count: " + recipeInfo.Count(), True, True)
            # MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  key: " + RunTestCycleId, True, True)
            # MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Recipe0: " + recipe[0], True, True)
            # MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Recipe4: " + recipe[4], True, True)
            # MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Recipe5: " + recipe[5], True, True)
            # MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Recipe6: " + recipe[6], True, True)
            
            AddOptionsAndPart("1", recipe[4])
            AddOptionsAndPart("2", recipe[5])
            AddOptionsAndPart("3", recipe[6])
        else:
            # InterfaceUiLogger(string mesSystem, string detail, bool isError = False, bool alarm = False)
            MainTPassScripting.InterfaceUiLogger("Magna-ESSS", "Option Parsing Script:  Invalid Recipe: " + RunTestCycleId, True, True)
            #isSuccess = False

        TPassLogger.Info("Option Parsing Script:  Product Primary ID = {0}", primaryId)
        TPassLogger.Info("Option Parsing Script:  Secondary ID = {0}", secondaryId)
        TPassLogger.Info("Option Parsing Script:  Tertiary ID = {0}", tertiaryId)

except Exception as inst:
    TPassLogger.Warn("Option Parsing Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Parsing Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Parsing Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 04172023
#	Version: 1.0
#	Change: Initial Version
############################################################

