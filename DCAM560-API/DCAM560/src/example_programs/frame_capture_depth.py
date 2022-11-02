from API.Vzense_api_560 import *
import cv2

camera = VzenseTofCam()

device_info = camera.init()
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_depth_range(Range.Mid)
camera.set_depth_distortion_correction(False)
frames = []

while len(frames) < 10:
    frameready = camera.read_frame()

    if frameready and frameready.depth:      
        frame = camera.get_frame(Frame.Depth)
        depth = camera.gen_image(frame,Frame.Depth)
        frames.append(depth)

avg = np.mean(frames,axis=0)

cv2.imwrite('save/depth.png',avg)
print("Successfully saved")
    
camera.stop_stream()
camera.close()