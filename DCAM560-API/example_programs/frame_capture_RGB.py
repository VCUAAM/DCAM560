from dcam560.Vzense_api_560 import *
import cv2

camera = VzenseTofCam()

camera.init()
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_RGB_distortion_correction(False)
frameready = camera.read_frame()

if frameready and frameready.rgb:      
    frame = camera.get_frame(Frame.RGB)
    rgb = camera.gen_image(frame,Frame.RGB)
    cv2.imwrite("save/rgb.png",rgb)
    print("Successfully saved")

camera.stop_stream() 
camera.close()