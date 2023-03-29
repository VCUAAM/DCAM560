from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info)
camera.start_stream()

for i in range(100):     
    print("Depth ID:",camera.get_frame(Frame.Depth).frameIndex)

camera.stop_stream()
camera.close()
           