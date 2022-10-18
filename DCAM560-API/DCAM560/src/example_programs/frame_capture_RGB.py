from API.Vzense_api_560 import *
import cv2, numpy as np

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri,"URI")
camera.start_stream()  
camera.set_data_mode("depRGB")
camera.set_mapper("RGB",True)
frameready = camera.read_frame()

if frameready and frameready.mappedRGB:      
    frame = camera.get_frame("RGB")
    img_arr = np.zeros((frame.height,frame.width,3),dtype=int)
    for i in range(len(img_arr)):
        for j in range(len(img_arr[0])):
            for k in range(3):
                img_arr[i,j,k] = int(frame.pFrameData[3*len(img_arr[0])*i + 3*j + k])
      
    cv2.imwrite("save/mappedrgb.png",img_arr)
    print("Successfully saved")
camera.stop_stream() 
camera.close()