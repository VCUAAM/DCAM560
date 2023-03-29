from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info)
camera.start_stream()    
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_RGB_resolution(Reso._1600x1200)

for i in range(30):
    frameready = camera.read_frame()
    if frameready and frameready.rgb:      
        frame = camera.get_frame(Frame.RGB)
        if frame.width == 640 and frame.height == 480:
            print("RGB ID:",frame.frameIndex)
        else:
            print("RGB width:",frame.width,"Height:",frame.height)      

camera.set_RGB_resolution(Reso._800x600)
 
for i in range(30):
    frameready = camera.read_frame()
    if frameready and frameready.rgb:      
        frame = camera.get_frame(Frame.RGB)
        if frame.width == 1600 and frame.height == 1200:
            print("RGB ID:",frame.frameIndex)
        else:
            print("RGB Width:",frame.width,"Height:",frame.height)

camera.stop_stream()
camera.close()