﻿#Parse build data passed in and populate IDs, options and part numbers
#This Script is expected to set the out parameters below
#
#TPass Objects Passed In/Returned
#   in - string "RunTestCycleId" - Id passed into the RunTestCycle() method
#   in - string "BuildData" - Build data sent from the option retrieval script
#   in  - object "MainTPassScripting" - Exposed methods and properties for the scripts to use
#   in  - method "TPassLogger" - This is the logging method to log to the main TPass log file
#   in  - method "TestAppLogger" - This is the logging method to log to the TPass Test Application log file
#   in  - method "GetConfigurationValue" - This is the method to get values set in the System Configuration file
#   out - string "primaryId"
#   out - string "secondaryId"
#   out - string "tertiaryId"
#   out - string "quaternaryId"
#   out - string "quinaryId"
#   out - list<string> "OptionCodesInBuildData"
#   out - dictionary<string,string> "PartNumbers"
#   out - bool "isSuccess"
#   out - bool "production"
#   out - string "version"
#

from System.Text.RegularExpressions import Regex


production = False
version = "4.1"

#########################################################################################################################################
# Application Engineer:  Set Part Number Tag Names required for Test Application and the Test Application Script File Name
#
#partNumberTags = set(["IPC","TCM","AMP","SDM","UPA","AOS","FCM","VPM","BCM","CGM","CSM","ONS","SIB","DTC","HFP","RAD","PEPS","HVAC"])
partNumberTags = set(["TCP","HFP","CSD","ECC","AMP","BCM","CGM","CSM","DMS","VCU","EBOOST","ELM","HUD","EOCM","FCM","HFPF","HFPR","HLDM","IPC","LRR","MSB","PAM","PFCM","PTM","SCL","SDM","SIB","ONS","VKM","VPM","WCM","UPA","ICS","IRC","HDLM","BCMOPSOFT","CSMOPSOFT"])
#
#########################################################################################################################################

try:

    primaryId = RunTestCycleId
    secondaryId = ""
    tertiaryId = ""
    quaternaryId = ""
    quinaryId = ""
    TPassLogger.Debug("Option Parsing Script:  Product Id = {0}", primaryId)
    TPassLogger.Debug("Option Parsing Script:  Product Build Data = {0}", BuildData)
    #BuildData = "PVIF=221000010,PVI=000010,VIN=1GT40FDA1NU000001,MDYR=N,CSN=1ZZ0100001 ,ASSM=1,PDYR=2022,MD=35743  ,RP01=0ST,RP02=1NF,RP03=1SD,RP04=1SZ,RP05=2NF,RP06=2ST,RP07=3ST,RP08=4FT,RP09=4ST,RP10=5A7,RP11=5C6,RP12=5FC,RP13=5GD,RP14=5KM,RP15=5ST,RP16=65C,RP17=6AM,RP18=7AM,RP19=8AM,RP20=9AM,RP21=9L3,RP22=A2X,RP23=A45,RP24=A50,RP25=A7K,RP26=AGJ,RP27=AHV,RP28=AJ7,RP29=AKO,RP30=AL0,RP31=ARU,RP32=AT8,RP33=ATH,RP34=AU3,RP35=AVI,RP36=AVK,RP37=AVU,RP38=AXK,RP39=B0S,RP40=BG9,RP41=BKA,RP42=BKD,RP43=BOY,RP44=BS1,RP45=BTM,RP46=BTT,RP47=BTV,RP48=BVZ,RP49=C49,RP50=C77,RP51=CC3,RP52=CE1,RP53=CGN,RP54=CJ4,RP55=CTT,RP56=DEA,RP57=DEH,RP58=DNS,RP59=DRZ,RP60=E63,RP61=EBI,RP62=EF7,RP63=EN0,RP64=EN5,RP65=EPH,RP66=ETN,RP67=F45,RP68=F47,RP69=FH1,RP70=FJP,RP71=FX3,RP72=G93,RP73=G94,RP74=GAZ,RP75=GQO,RP76=H9Z,RP77=HS1,RP78=IKP,RP79=IOK,RP80=J22,RP81=J77,RP82=JAD,RP83=JCF,RP84=JFI,RP85=JL1,RP86=JSZ,RP87=K12,RP88=K28,RP89=K4C,RP90=KA1,RP91=KA6,RP92=KC9,RP93=KI3,RP94=KI4,RP95=KQV,RP96=KRV,RP97=KSG,RP98=KTI,RP99=KWP,RP100=LHD,RP101=MAH,RP102=MF1,RP103=N38,RP104=NCG,RP105=NF6,RP106=NP5,RP107=NYS,RP108=NZZ,RP109=OAR,RP110=P79,RP111=PPW,RP112=PSC,RP113=PTT,RP114=PZ8,RP115=QK2,RP116=QMG,RP117=QT5,RP118=R6F,RP119=R7E,RP120=R9N,RP121=RCS,RP122=RSR,RP123=S6L,RP124=S8L,RP125=SDA,RP126=SLM,RP127=SNR,RP128=T4L,RP129=T8Z,RP130=TDM,RP131=THS,RP132=TQ5,RP133=TRJ,RP134=U2K,RP135=U91,RP136=UBD,RP137=UBI,RP138=UDV,RP139=UE1,RP140=UE4,VPRG=UF2UFBUG,VSFT=1UGNUITU,VENG=DXL8XRLY,VFUL=F5YM8Z6X,VSYS=Z       ,VSPD=        ,VTRN=        ,VMUP=        ,TBPN=        ,TPRG=        ,TACC=        ,TSTR=        ,TLGT=        ,TWRN=        ,TSEC=        , ,rp160=123"

    keyValuePairs = BuildData.Split(',')
    if keyValuePairs[0] != BuildData:
        for keyValuePair in keyValuePairs:
            keyarray = keyValuePair.Split('=')
            #TPassLogger.Debug("Option Parsing Script:  keyValuePair = {0}", keyValuePair)
            if len(keyarray) != 2:
                TPassLogger.Info("Option Parsing Script:  Not Key=Value format  Data = {0}", keyValuePair)
                continue
            key = keyarray[0].Trim().ToUpper()
            value = keyarray[1].ToUpper()

            # Example ways of setting different IDs
            if (key == "VIN"):
                secondaryId = value
            elif (key == "MD"):
                tertiaryId = value
                # Add options based on Model Designator
                if (tertiaryId.strip() == "2" or tertiaryId.strip() == "6NW26" or tertiaryId.strip() == "6NX26"):
                    OptionCodesInBuildData.Add("C1TL")
                    TPassLogger.Debug("Option Parsing Script: Added Option Code ({0}) based on MD in build data", "C1TL");

            #elif (key == "PDYR"):
            #    quaternaryId = value
            #elif (key == "CSN"):
            #    quinaryId = value


            # Populate Option Codes found in broadcasted build data
            if Regex.IsMatch(key, "\\ARP\\d") and value != "":
                TPassLogger.Debug("Option Parsing Script: RPO Found, RPO = {0}, Value = {1}", key, value)
                OptionCodesInBuildData.Add(value)
                TPassLogger.Debug("Option Parsing Script: Added Configured Option Code ({0}) found in build data", value);

            # Populate interested Part Numbers that are in the Broadcasted Build Data
            if key in partNumberTags:
                if PartNumbers.ContainsKey(key):
                    TPassLogger.Warn("Option Parsing Script: Part Tag ({0}, {1}) found twice in build data.  First occurrence will be used", key, value);
                else:
                    TPassLogger.Info("Option Parsing Script: Added Part ({0}, {1}) found in build data", key, value);
                    PartNumbers.Add(key, value)                

    TPassLogger.Info("Option Parsing Script:  Product Primary ID = {0}", primaryId)
    isSuccess = True

except Exception as inst:
    TPassLogger.Warn("Option Parsing Script:  Exception Occurred :{0}", inst)
    TPassLogger.Warn("Option Parsing Script:  Processing Failed.")
    isSuccess = False
TPassLogger.Info("Option Parsing Script:  Is Success = {0}", isSuccess)

############################################################
# Change History
############################################################
#	Date: 03302022
#	Version: 4.1
#   Change: Add option based on Model Designator
#	Date: 0809021
#	Version: 4.0
#	Change: If duplicate Part tag in build data, use first occurrence and log warning
#	Date: 08042021
#	Version: 3.0
#	Change: Set Secondary Id to the VIN
#	Date: 08032021
#	Version: 2.0
#	Change: Fixed issue with having trailing comma causing exception
#	Date: 04152021
#	Version: 1.0
#	Change: Initial Version
############################################################

