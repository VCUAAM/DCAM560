from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info,Open.URI) 
camera.start_stream() 

WDRMode = PsWDROutputMode()
WDRMode.totalRange = 2
WDRMode.range1 = 0
WDRMode.range1Count = 1
WDRMode.range2 = 1
WDRMode.range2Count = 1
WDRMode.range3 = 5
WDRMode.range3Count = 1
    
camera.set_WDR_output_mode(WDRMode)
camera.set_data_mode(DataMode.WDR_Depth)
camera.set_WDR_style(WDR_Style.Alternation)

while True:
    frameready = camera.read_frame()
    if frameready:
        frame = camera.get_frame(Frame.WDRDepth)
        fh,fw = int(frame.height),int(frame.width)
        print(fh,fw)
        print(frame.dataLen)
        save_file = "save/wdralt.png"
        depth = camera.gen_image(frame,Frame.Depth)
        cv2.imwrite(save_file,depth)
        print("Successfully saved")
        break
       
camera.stop_stream()
camera.close()