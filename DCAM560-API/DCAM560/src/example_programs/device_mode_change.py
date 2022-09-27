from API.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri) 
camera.start_stream()
camera.set_data_mode("depRGB")
    
for i in range(30):
    frameready = camera.read_frame()   
    
    if frameready and frameready.depth and frameready.rgb:      
        frame = camera.get_frame("Depth")
        print("Depth ID:",frame.frameIndex)  
        frame = camera.get_frame("RGB")
        print("RGB ID:",frame.frameIndex)

camera.set_data_mode("IR")
    
for i in range(30):
    frameready = camera.read_frame()  
    
    if frameready and frameready.depth and frameready.ir and frameready.rgb:      
        frame = camera.get_frame("Depth")
        print("Depth ID:",frame.frameIndex)     
        frame = camera.get_frame("IR")
        print("IR ID:",frame.frameIndex)  
        frame = camera.get_frame("RGB")
        print("RGB ID:",frame.frameIndex)  

camera.stop_stream()
camera.close()
           