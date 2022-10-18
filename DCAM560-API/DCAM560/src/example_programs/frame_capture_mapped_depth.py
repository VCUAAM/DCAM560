from API.Vzense_api_560 import *
import cv2, numpy as np
camera = VzenseTofCam()
device_info = camera.connect()
camera.open(device_info.uri,"URI")  
camera.start_stream()   
camera.set_data_mode("depRGB")
camera.set_mapper("Depth",True)   
frameready = camera.read_frame()
            
if frameready and frameready.mappedDepth:      
    frame = camera.get_frame("Depth")
    fh,fw = int(frame.height),int(frame.width)
    save_file = "save/mappeddepth.png"
    img_arr = np.zeros((fh,fw),dtype=int)

    for i in range(fh):
        for j in range(fw):
                img_arr[i,j] = int(frame.pFrameData[3*len(img_arr[0])*i + 2*j])

    cv2.imwrite(save_file,img_arr)
    full_img = cv2.imread(save_file)
    lef = full_img[0:fh,0:int(fw/2)]
    rig = full_img[0:fh,int(fw/2):fw]
    blen = cv2.addWeighted(lef,.5,rig,.5,0.0)
    cv2.imwrite('save/blended.png',blen)
    print("Successfully saved")
    
camera.stop_stream()
camera.close()