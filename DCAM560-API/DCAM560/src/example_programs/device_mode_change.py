from API.Vzense_api_560 import *

camera = VzenseTofCam()

camera.init()
camera.set_data_mode(DataMode.Depth_RGB)
    
for i in range(30):
    frameready = camera.read_frame()   
    
    if frameready and frameready.depth and frameready.rgb:      
        frame = camera.get_frame(Frame.Depth)
        print("Depth ID:",frame.frameIndex)  
        frame = camera.get_frame(Frame.RGB)
        print("RGB ID:",frame.frameIndex)

camera.set_data_mode(DataMode.Depth_IR_RGB)
    
for i in range(30):
    frameready = camera.read_frame()  
    
    if frameready and frameready.depth and frameready.ir and frameready.rgb:      
        frame = camera.get_frame(Frame.Depth)
        print("Depth ID:",frame.frameIndex)     
        frame = camera.get_frame(Frame.IR)
        print("IR ID:",frame.frameIndex)  
        frame = camera.get_frame(Frame.RGB)
        print("RGB ID:",frame.frameIndex)  

camera.stop_stream()
camera.close()
           