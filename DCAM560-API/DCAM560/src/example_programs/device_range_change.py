from API.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri,"URI")
camera.start_stream()
camera.set_depth_range("Near")

for i in range(30):
    frameready = camera.read_frame()
    
    if frameready and frameready.depth:      
        frame = camera.get_frame("Depth")
        if frame.depthRange == PsDepthRange.PsNearRange.value:
            print("Depth ID:",frame.frameIndex)  
        else:   
            print("Depth range:",frame.depthRange)    

camera.set_depth_range("Mid")
    
for i in range(30):
    frameready = camera.read_frame()

    if frameready and frameready.depth:      
        frame = camera.get_frame("Depth")
        if frame.depthRange == PsDepthRange.PsMidRange.value:
            print("Depth ID:",frame.frameIndex)  
        else:   
            print("Depth range:",frame.depthRange)   
            
camera.stop_stream()
camera.close()