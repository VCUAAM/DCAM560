from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

camera.init()

params = camera.get_camera_parameters(Sensor.Depth)
print("Depth Camera Parameters:",
params.fx,
params.fy,
params.cx,
params.cy, 
params.k1,
params.k2,
params.p1,
params.p2,
params.k3,
params.k4,
params.k5,
params.k6)
    
params = camera.get_camera_parameters(Sensor.RGB)
print("RGB Camera Parameters:",
params.fx,
params.fy,
params.cx,
params.cy, 
params.k1,
params.k2,
params.p1,
params.p2,
params.k3,
params.k4,
params.k5,
params.k6)

extrparams = camera.get_camera_extrinsic_parameters()
print("Camera Extrinsic Parameters:")
print("Rotation:")
for i in range(9):
    print(extrparams.rotation[i])
print("Translation:")
for i in range(3):
    print(extrparams.translation[i])  

threshold = camera.get_threshold()
pulsecnt = camera.get_pulse_count()
gmmgain = camera.get_GMM_gain()
camera.stop_stream()        
camera.close()