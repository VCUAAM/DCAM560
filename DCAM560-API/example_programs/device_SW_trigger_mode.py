from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info)
camera.start_stream()
camera.set_slave_mode(True)

for i in range(30):
    camera.set_slave_trigger()
    frameready = camera.read_frame() 
    if frameready and frameready.depth:
        frame = camera.get_frame(Frame.Depth)
        print("Depth ID:",frame.frameIndex)  

camera.set_slave_mode(False)
camera.stop_stream()
camera.close()        