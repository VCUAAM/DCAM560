from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info,Open.URI) 
camera.start_stream() 

WDRMode = PsWDROutputMode()
WDRMode.totalRange = 2
WDRMode.range1 = 0
WDRMode.range1Count = 1
WDRMode.range2 = 2
WDRMode.range2Count = 1
WDRMode.range3 = 5
WDRMode.range3Count = 1
    
camera.set_WDR_output_mode(WDRMode)
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_WDR_style(WDR_Style.Alternation)
       
for i in range(30):
    frameready = camera.read_frame()  
    
    if frameready and frameready.depth:      
        frame = camera.get_frame(Frame.Depth)
        print("Depth ID: ",frame.frameIndex,"Range: ",frame.depthRange)  
       
camera.stop_stream()
camera.close()