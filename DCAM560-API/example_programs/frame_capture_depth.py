from dcam560.Vzense_api_560 import *
import cv2

camera = VzenseTofCam()

device_info = camera.init()
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_depth_range(Range.Mid)
camera.set_depth_distortion_correction(False)
depth_max,value_min,max_range = camera.get_measuring_range(False)
frames = []

while True:
    frameready = camera.read_frame()

    if frameready and frameready.depth:
        frame = camera.get_frame(Frame.Depth)
        break

fw,fh = frame.width,frame.height
frametmp = np.ctypeslib.as_array(frame.pFrameData, (1, 2*fw*fh))
frametmp.dtype = np.uint16
frametmp.shape = (fh, fw)

img = np.int32(frametmp)*255/max_range
img = np.uint8(np.clip(img, 0, 255))
frametmp = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
bgr = frametmp.copy()
r,p = np.array([0,0,255]),np.array([255,0,170])
mask_r,mask_p = cv2.inRange(bgr,r,r),cv2.inRange(bgr,p,p)
frametmp[mask_r > 0] = (255,255,255)
frametmp[mask_p > 0] = (0,0,0)

depth = camera.gen_image(frame,Frame.Depth)
#cv2.namedWindow('Depth Image', cv2.WINDOW_KEEPRATIO)
#cv2.imshow("Depth Image", depth)

cv2.imwrite('save/depth.png',depth)
print("Successfully saved")
    
camera.stop_stream()
camera.close()