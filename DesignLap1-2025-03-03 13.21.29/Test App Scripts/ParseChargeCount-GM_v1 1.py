#Parse CAN Frames.  Parse raw data.
#
#TPass Objects Passed In/Returned
#   in - string "rawCanDataResponse"
#   in - bool "isMultiFrameMessage"
#   in - bool "ignoreStatus"
#   in - Function "TestAppLogger"
#   in - validateCanMessageScriptInputs
#   out - dictionary<string, string> "DpidDictionary"
#   out - string "DpidData" 
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

#System.Diagnostics.Debugger.Break();


############################################################################################################################################
# Software Engineer Debug / Simulate
# from System.Collections.Generic import Dictionary
# rawCanDataResponse = "1009625406010002000B3F"
# DpidDictionary = Dictionary[str,str]()

# ## Initial Charge Count Added Here as strings, we can convert them to Integers during a difference check.
# DpidDictionary.Add("ACFrame_1", "1")
# DpidDictionary.Add("DCFrame_1", "10")

# ## Charge Count for Post AC Simulation
# DpidDictionary.Add("ACFrame_2", "2")
# DpidDictionary.Add("DCFrame_2", "10")

# ## Charge Count for Post DC Simulation
# DpidDictionary.Add("ACFrame_3", "2")
# DpidDictionary.Add("DCFrame_3", "10")

############################################################################################################################################
import clr
version = "1.0"
production = False

try:
    
    TestAppLogger.Info("CAN Frame Parsing Python Script:  Raw Can Data Response = {0}", rawCanDataResponse)
 
    if len(rawCanDataResponse) >= 22 and validateCanMessageScriptInputs != None:
        
        acFrame = rawCanDataResponse[12:16]
        dcFrame = rawCanDataResponse[16:20]  
        
        ## First set of Charge Counts gets stored during the first CanSendReceiveValidate for Pre-AC.
        if len(validateCanMessageScriptInputs) > 0 and validateCanMessageScriptInputs[0] == "ACPRE":
            
            DpidDictionary.Add("ACPREACTEST", str(int(acFrame, 16)))
            DpidDictionary.Add("DCPREACTEST", str(int(dcFrame, 16)))
            DpidData = str(int(acFrame, 16))
            
            TestAppLogger.Info("Processed Dpid Data - Charge Count Pre-AC: " + DpidData)
            
            isSuccess = True
        
        ## Second set of Charge Counts gets stored during the second CanSendReceiveValidate for Post-AC.
        elif len(validateCanMessageScriptInputs) > 0 and validateCanMessageScriptInputs[0] == "ACPOST":
            DpidDictionary.Add("ACPOSTACTEST", str(int(acFrame, 16)))
            DpidDictionary.Add("DCPOSTACTEST", str(int(dcFrame, 16)))
            
            DpidData = str(int(acFrame, 16))
            
            TestAppLogger.Info("Processed Dpid Data - Charge Count Post-AC: " + DpidData)
            
            ## Take and log the difference, if the difference is greater than 0 then return True / pass, otherwise return false / fail.
            ## Difference = Final - Initial
            ACChargeCountDifference = int(DpidDictionary["ACPOSTACTEST"]) - int(DpidDictionary["ACPREACTEST"])
            TestAppLogger.Info("CAN Frame Parsing Python Script - Processed Dpid Data - AC Charge Count Difference: " + str(ACChargeCountDifference))
            if ACChargeCountDifference > 0:
                isSuccess = True
            else:
                isSuccess = False
                FaultDetail += "AC charge count did not increment"
                TestAppLogger.Info("CAN Frame Parsing Python Script - AC charge count did not increment")
        
        ## Third set of Charge Counts gets stored during the third CanSendReceiveValidate for Pre-DC.
        elif len(validateCanMessageScriptInputs) > 0 and validateCanMessageScriptInputs[0] == "DCPRE" :
            
            DpidDictionary.Add("ACPREDCTEST", str(int(acFrame,16)))
            DpidDictionary.Add("DCPREDCTEST", str(int(dcFrame,16)))

            DpidData = str(int(dcFrame, 16))
            TestAppLogger.Info("CAN Frame Parsing Python Script - Processed Dpid Data - Charge Count Pre-DC: " + DpidData)
            
            isSuccess = True
        
         ## Fourth set of Charge Counts gets stored during the fourth CanSendReceiveValidate for Post-DC.
        elif len(validateCanMessageScriptInputs) > 0 and validateCanMessageScriptInputs[0] == "DCPOST" :
            
            DpidDictionary.Add("ACPOSTDCTEST", str(int(acFrame,16)))
            DpidDictionary.Add("DCPOSTDCTEST", str(int(dcFrame,16)))
            
            DpidData = str(int(dcFrame, 16))
            
            TestAppLogger.Info("CAN Frame Parsing Python Script - Processed Dpid Data - Charge Count Post-DC: " + DpidData)
            
            ## Take and log the difference, if the difference is greater than 0 then return True / pass, otherwise return false / fail 
            ## Difference = Final - Initial
            DCChargeCountDifference = int( DpidDictionary["DCPOSTDCTEST"] ) - int(DpidDictionary["DCPREDCTEST"])
            TestAppLogger.Info("Processed Dpid Data - DC Charge Count Difference: " + str(DCChargeCountDifference))
            if(DCChargeCountDifference > 0):
                isSuccess = True
            else:
                isSuccess = False
                FaultDetail += "DC charge count did not increment"
                TestAppLogger.Info("CAN Frame Parsing Python Script - DC charge count did not increment")
        
    else:
        isSuccess = False
        FaultDetail += "No CAN Response from Module"
        TestAppLogger.Info("No CAN Response from Module.")
    
except Exception as inst:
    TestAppLogger.Warn("CAN Frame Parsing Python Script: Exception Occurred :{0}", inst)
    TestAppLogger.Warn("CAN Frame Parsing Python Script: Processing Failed.")
    isSuccess = False
TestAppLogger.Info("CAN Frame Parsing Python Script: Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 01012019
#	Version: 1.0
#	Change: Initial Version
############################################################