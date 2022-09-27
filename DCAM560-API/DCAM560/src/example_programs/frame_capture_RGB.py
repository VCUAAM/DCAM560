from API.Vzense_api_560 import *
import time

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri,"URI")
camera.start_stream()  
camera.set_data_mode("depRGB")
camera.set_mapper("RGB",True)
frameready = camera.read_frame()
 
if frameready and frameready.mappedRGB:      
    frame = camera.get_frame("RGB")
    folder = os.getcwd() + "/save"
    filename = folder + "/mappedrgb.bin"
    if not os.path.exists(folder):
        print("Creating save folder")
        os.makedirs(folder)
    
    file = open(filename,"wb+")
    for i in range(frame.dataLen):
        file.write(c_uint8(frame.pFrameData[i]))
            
    file.close()
    print("Successfully saved")
camera.stop_stream() 
camera.close()
           