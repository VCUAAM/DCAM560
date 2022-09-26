from pickle import FALSE, TRUE
import sys
sys.path.append('src/')
from API.Vzense_api_560 import *

camera = VzenseTofCam()

def HotPlugStateCallback(type_struct,  state = c_int32(0)):
    global camera
    if state ==0:
        print(str(type_struct.contents.alias) + "   add")
        ret = camera.Ps2_OpenDevice(type_struct.contents.uri)
        if  ret == 0:
            print(str(type_struct.contents.alias) + " open success")
        else:
            print(str(type_struct.contents.alias) + " open failed",ret)
        ret = camera.Ps2_StartStream()
        if  ret == 0:
            print(str(type_struct.contents.alias) + " startstream success")
        else:
            print(str(type_struct.contents.alias) + " startstream failed",ret)
    else:
        print(str(type_struct.contents.alias) + "   remove")
        ret = camera.Ps2_StopStream()
        if  ret == 0:
            print(str(type_struct.contents.alias) + " stopstream success")
        else:
            print(str(type_struct.contents.alias) + " stopstream failed",ret)
        ret = camera.Ps2_CloseDevice()
        if  ret == 0:
            print(str(type_struct.contents.alias) + " close success")
        else:
            print(str(type_struct.contents.alias) + " close failed",ret)

camera.Ps2_SetHotPlugStatusCallback(HotPlugStateCallback)

device_info = camera.connect()
camera.open(device_info.uri)
camera.stop_stream()
camera.close()
