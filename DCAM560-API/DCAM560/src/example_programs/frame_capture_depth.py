from API.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri,"URI")
camera.start_stream()   
frameready = camera.read_frame()

if frameready and frameready.depth:
    frame = camera.get_frame("Depth")
    folder = os.getcwd() + "/save"

    if not os.path.exists(folder):
        print("Path does not exist")
        os.makedirs(folder)

    filename = folder + "/depth.bin"
    file = open(filename,"wb+")

    for i in range(frame.dataLen):
        file.write(c_uint8(frame.pFrameData[i]))

    file.close()
    print("Successfully saved")
camera.stop_stream()
camera.close()
           