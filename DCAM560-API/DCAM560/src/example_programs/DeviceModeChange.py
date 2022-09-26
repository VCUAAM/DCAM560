from pickle import FALSE, TRUE
import sys
sys.path.append('src/')
from API.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri) 
camera.start_stream()

ret = camera.Ps2_SetDataMode(PsDataMode.PsDepthAndRGB_30)
if ret != 0:  
    print("Ps2_SetDataMode failed:",ret)
    
for i in range(30):
    ret, frameready = camera.Ps2_ReadNextFrame()
    if  ret !=0:
        print("Ps2_ReadNextFrame failed:",ret)
        #time.sleep(1)
        continue       
    
    if  frameready.depth and frameready.rgb:      
        ret,frame = camera.Ps2_GetFrame(PsFrameType.PsDepthFrame)
        if  ret == 0:
            print("depth  id:",frame.frameIndex)  
        else:   
            print("depth  error:",ret)   
        ret,frame = camera.Ps2_GetFrame(PsFrameType.PsRGBFrame)
        if  ret == 0:
            print("rgb  id:",frame.frameIndex)  
        else:   
            print("rgb  error:",ret)

ret = camera.Ps2_SetDataMode(PsDataMode.PsDepthAndIRAndRGB_30)
if  ret != 0:  
    print("Ps2_SetDataMode failed:",ret)
    
for i in range(30):
    ret, frameready = camera.Ps2_ReadNextFrame()
    if  ret !=0:
        print("Ps2_ReadNextFrame failed:",ret)
        #time.sleep(1)
        continue       
    
    if  frameready.depth and frameready.ir and frameready.rgb:      
        ret,frame = camera.Ps2_GetFrame(PsFrameType.PsDepthFrame)
        if  ret == 0:
            print("depth  id:",frame.frameIndex)  
        else:   
            print("depth  error:",ret)   
        ret,frame = camera.Ps2_GetFrame(PsFrameType.PsIRFrame)
        if  ret == 0:
            print("ir  id:",frame.frameIndex)  
        else:   
            print("ir  error:",ret)
        ret,frame = camera.Ps2_GetFrame(PsFrameType.PsRGBFrame)
        if  ret == 0:
            print("rgb  id:",frame.frameIndex)  
        else:   
            print("rgb  error:",ret)
camera.stop_stream()
camera.close()
           