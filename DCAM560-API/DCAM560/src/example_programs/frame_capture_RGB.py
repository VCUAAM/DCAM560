from API.Vzense_api_560 import *
import cv2, numpy as np

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri,Open.URI)
camera.start_stream()  
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_mapper(Sensor.RGB,True)
camera.set_RGB_distortion_correction(True)
frameready = camera.read_frame()

if frameready and frameready.rgb:      
    frame = camera.get_frame(Frame.RGB)
    rgb = camera.gen_image(frame,Frame.RGB)
    cv2.imwrite("save/rgb.png",rgb)
    print("Successfully saved")
camera.stop_stream() 
camera.close()