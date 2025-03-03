import clr
## Note this reference is required in order to access the Colors for the Background
clr.AddReferenceByPartialName("PresentationCore")
from System.Windows.Media import Brushes

production = False
version = "1"

try:
    ## MainTPassScripting.Alert(string alertTitle, string alertMessage, double alertFontsize, Brush alertBackgroundcolor)
    MainTPassScripting.Alert("Static Hold or Flash Hold",'<fontsize:32> >: Static Hold or Flash Hold </fontsize>', 35.0, Brushes.Red )
    isSuccess = True
except Exception as inst:
    TPassLogger.Warn("Alert Page Failed to Load:  Exception Occurred :{0}", inst)
    isSuccess = False