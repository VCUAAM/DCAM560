from API.Vzense_api_560 import *
import cv2

camera = VzenseTofCam()
device_info = camera.connect()
camera.open(device_info.uri,Open.URI) 
camera.start_stream()   
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_depth_range(Range.Mid)
camera.set_depth_distortion_correction(False)
deprange = Range((camera.get_depth_range()).value)
depth_max, value_min, value_max = camera.get_measuring_range(deprange)

frameready = camera.read_frame()

if frameready and frameready.depth:      
    frame = camera.get_frame(Frame.Depth)
    depth = camera.gen_image(frame,Frame.Depth,value_max)
    cv2.imwrite('save/depth.png',depth)
    print("Successfully saved")
    
camera.stop_stream()
camera.close()