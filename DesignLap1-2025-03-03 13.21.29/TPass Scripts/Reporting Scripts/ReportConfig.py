import clr 

clr.AddReference("Tpi.TPass.Common")
clr.AddReference("Tpi.TPass.Config")

import Tpi.TPass.Common.LogSupport.LogSupport as LogSupport
import Tpi.TPass.Config.Models.Controls as Controls

def ReportConfig( ReportButtons ):
    
    ReportButtons.Clear()
    
    LogSupport.TPassLogger.Info( "Reporting: Loading in Report Configurations" )
    
    Top10TestFaults = Controls.TpassReportButton()
    Top10TestFaults.Enabled = True
    Top10TestFaults.ReportTitle = "Top 10 Test Faults"
    Top10TestFaults.ReportDescription = "Gets the Top 10 Test Faults based on the date range and chosen test fault"
    Top10TestFaults.Script = "Top 10 Test Faults.aes"
    
    ReportButtons.Add(Top10TestFaults)
    
    Top10GroupTestResults = Controls.TpassReportButton()
    Top10GroupTestResults.Enabled = True
    Top10GroupTestResults.ReportTitle = "Top 10 Group Test Results"
    Top10GroupTestResults.ReportDescription = "Gets the Top 10 Group Test Results based on the date range and chosen test fault"
    Top10GroupTestResults.Script = "Top 10 Group Test Results.aes"
    
    ReportButtons.Add(Top10GroupTestResults)
    
    Top10TestStepResults = Controls.TpassReportButton()
    Top10TestStepResults.Enabled = True
    Top10TestStepResults.ReportTitle = "Top 10 Test Step Results"
    Top10TestStepResults.ReportDescription = "Gets the Top 10 Test Step Results based on the date range and chosen test fault"
    Top10TestStepResults.Script = "Top 10 TestStep Results.aes"
    
    ReportButtons.Add(Top10TestStepResults)
    
    TestCycleDurationResults = Controls.TpassReportButton()
    TestCycleDurationResults.Enabled = True
    TestCycleDurationResults.ReportTitle = "Test Cycle Duration Results"
    TestCycleDurationResults.ReportDescription = "Returns the Test Cycle Durations for a given date range and test result"
    TestCycleDurationResults.Script = "TestCycleDurationResults.aes"
    
    ReportButtons.Add(TestCycleDurationResults)
    
    TestResultsPerDay = Controls.TpassReportButton()
    TestResultsPerDay.Enabled = True
    TestResultsPerDay.ReportTitle = "Test Results Per Day"
    TestResultsPerDay.ReportDescription = "Gets the total Test Results per day for a given date range and chosen test result"
    TestResultsPerDay.Script = "TestResultsPerDay.aes"
    
    ReportButtons.Add(TestResultsPerDay)
    
    AllFaultCodes = Controls.TpassReportButton()
    AllFaultCodes.Enabled = True
    AllFaultCodes.ReportTitle = "All Fault Codes"
    AllFaultCodes.ReportDescription = "Provides all the fault codes within a given date range"
    AllFaultCodes.Script = "AllFaultCodes.aes"
    ReportButtons.Add(AllFaultCodes)
    
    TestParameterResults = Controls.TpassReportButton()
    TestParameterResults.Enabled = True
    TestParameterResults.ReportTitle = "Test Parameter Results"
    TestParameterResults.ReportDescription = "Gets the test parameter results of the last test."
    TestParameterResults.Script = "TestParameterResults.aes"
    ReportButtons.Add(TestParameterResults)
    
    
############################################################
# Change History
############################################################
#   Date: 05162023
#   Version: 1.1
#   ChangeBy: LM
#   Change: Clear buttons before adding  
############################################################