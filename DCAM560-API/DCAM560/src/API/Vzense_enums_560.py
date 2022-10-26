from ctypes import *
from enum import Enum
 
class Range(Enum):
    Near            = 0
    Mid             = 1
    Far             = 2
    XNear           = 3
    XMid            = 4
    XFar            = 5
    XXNear          = 6
    XXMid           = 7
    XXFar           = 8
    Unknown         = -1

class Open(Enum):
    URI     = 0
    alias   = 1
    IP      = 2
class DataMode(Enum):
    Depth_RGB        = 0
    IR_RGB           = 1
    Depth_IR_RGB     = 2
    WDR_Depth        = 11
    
class Frame(Enum):
    Depth            = 0     
    IR               = 1        
    RGB              = 3       
    MappedRGB        = 4                       
    MappedDepth      = 5                      
    WDRDepth         = 9     
        
class Sensor(Enum):
    Depth = 0x01
    RGB   = 0x02

class Pixel(Enum):
    DepthMM16 = 0
    Gray16    = 1 
    Gray8     = 2  
    RGB888    = 3  
    BGR888    = 4    

class Error(Enum):
    OK                                   =  0
    No_Device_Conntected                 = -1
    Invalid_Device_Index                 = -2
    Device_Pointer_Null                  = -3
    Invalid_Frame_Type                   = -4
    Frame_Pointer_Null                   = -5
    No_Value_Got                         = -6
    No_Value_Set                         = -7
    Property_Pointer_Null                = -8
    Property_Max_Size_Exceeded           = -9
    Invalid_Depth_Range                  = -10
    Read_Frame_Timed_Out                 = -11
    Input_Pointer_Null                   = -12
    Camera_Not_Opened                    = -13
    Invalid_Camera_Type                  = -14
    Invalid_Parameters                   = -15
    Current_Version_Not_Supported        = -16
    Upgrade_Image_Error                  = -17
    Upgrade_Image_Max_Length_Exceeded    = -18
    Upgrade_Callback_Not_Set	         = -19
    No_Adapter_Connected			     = -100
    SDK_Initialized				         = -101
    SDK_Not_Initialized				     = -102
    Camera_Opened				         = -103
    Commadn_Error					     = -104
    Command_Sync_Timed_Out				 = -105
    IP_Mismatch					         = -106
    Other                                = -255

class WDR_Range(Enum):
    Total_Range_Two   = 2
    Total_Range_Three = 3

class WDR_Style(Enum):
    Fusion      = 0
    Alternation = 1

class Reso(Enum):
    _640x480     = 2
    _1600x1200   = 4
    _800x600     = 5
    
class Status(Enum):
    Unknown          = 0
    Disconnected     = 1
    Connected        = 2
    Opened           = 3

class Device(Enum):
	NONE           = 0
	DCAM305        = 305
	DCAM500        = 500
	CSI100	       = 501
	DCAM510        = 510
	DCAM550U       = 550
	DCAM550P       = 551
	DCAM550E       = 552
	DCAM560        = 560
	DCAM560CPRO    = 561
	DCAM560CLITE   = 562
	DCAM710        = 710
	DCAM800        = 800
	DCAM_MIPI      = 801
	DCAM800LITE    = 802
	DCAM800LITEUSB = 803
	DCAM101        = 804
