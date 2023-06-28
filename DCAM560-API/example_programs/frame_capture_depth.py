from dcam560.Vzense_api_560 import *
import cv2

camera = VzenseTofCam()

device_info = camera.init()
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_depth_range(Range.Mid)
camera.set_depth_distortion_correction(False)
camera.set_threshold(0)
depth_max,value_min,max_range = camera.get_measuring_range(False)

while True:
    frameready = camera.read_frame()

    if frameready and frameready.depth:
        frame = camera.get_frame(Frame.Depth)
        break

depth = camera.gen_image(frame,Frame.Depth)
#cv2.namedWindow('Depth Image', cv2.WINDOW_KEEPRATIO)
#cv2.imshow("Depth Image", depth)

cv2.imwrite('save/depth.png',depth)
print("Successfully saved")
    
camera.stop_stream()
camera.close()