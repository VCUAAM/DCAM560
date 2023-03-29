from dcam560.Vzense_api_560 import *
import cv2

camera = VzenseTofCam()
device_info = camera.connect()
camera.open(device_info,Open.URI) 
camera.start_stream()   
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_depth_range(Range.Far)
camera.set_mapper(Sensor.Depth,True)
camera.set_depth_distortion_correction(True)
deprange = Range((camera.get_depth_range()).value)
depth_max, value_min, value_max = camera.get_measuring_range(deprange)

frameready = camera.read_frame()

if frameready and frameready.mappedDepth:      
    frame = camera.get_frame(Frame.MappedDepth)
    depth = camera.gen_image(frame,Frame.Depth)
    cv2.imwrite('save/mappeddepth.png',depth)
    print("Successfully saved")
    
camera.stop_stream()
camera.close()