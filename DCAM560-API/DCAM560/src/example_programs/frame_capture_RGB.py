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
    filename = folder + "/mappedrgb.txt"
    if not os.path.exists(folder):
        print("Creating save folder")
        os.makedirs(folder)
    
    file = open(filename,"w+")
    rgb = []
    for i in range(int(frame.dataLen/3)):
        r = int(frame.pFrameData[3*i])
        g = int(frame.pFrameData[3*i + 1])
        b = int(frame.pFrameData[3*i + 2])
        rgb.append([r,g,b])
    file.write(str(rgb))      
    file.close()
    print("Successfully saved")
camera.stop_stream() 
camera.close()
           