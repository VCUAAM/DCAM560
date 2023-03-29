from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info)
camera.start_stream()
camera.set_depth_range(Range.Near)

for i in range(30):
    frameready = camera.read_frame()
    
    if frameready and frameready.depth:      
        frame = camera.get_frame(Frame.Depth)
        if frame.depthRange == Range.Near.value:
            print("Depth ID:",frame.frameIndex)  
        else:   
            print("Depth range:",frame.depthRange)    

camera.set_depth_range(Range.Mid)
    
for i in range(30):
    frameready = camera.read_frame()

    if frameready and frameready.depth:      
        frame = camera.get_frame(Frame.Depth)
        if frame.depthRange == Range.Mid.value:
            print("Depth ID:",frame.frameIndex)  
        else:   
            print("Depth range:",frame.depthRange)   
            
camera.stop_stream()
camera.close()