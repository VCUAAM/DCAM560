from API.Vzense_api_560 import *

camera = VzenseTofCam()
device_info = camera.connect()
camera.open(device_info.uri,"URI")  
camera.start_stream()   
camera.set_data_mode("depRGB")
camera.set_mapper("Depth",True)   
frameready = camera.read_frame()

if frameready and frameready.mappedDepth:      
    frame = camera.get_frame("Depth")
    folder = os.getcwd() + "/save"
    filename = folder + "/mappeddepth.txt"

    if not os.path.exists(folder):
        print("Creating folder")
        os.makedirs(folder)
    
    file = open(filename,"w+")
    
    for i in range(frame.dataLen):
        file.write(str(frame.pFrameData[i]))
        
    print("Successfully saved")
camera.stop_stream()
camera.close()